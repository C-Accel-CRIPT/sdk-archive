import pytest
import requests
import psycopg2

import cript

from requests.exceptions import ConnectionError
from tempfile import NamedTemporaryFile
from unittest import mock

MY_GROUP = "MyGroup"
MY_PROJECT = "MyProject"
MY_COLLECTION = "Test"
MY_EXPERIMENT = "Anionic Polymerization of Styrene with SecBuLi"
MY_INVENTORY = "Test"
MY_PROCESS = "Test"


def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@pytest.fixture(scope="session")
def http_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""

    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("web", 8000)
    url = "http://{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url


@pytest.fixture(scope="session")
def db_connection(docker_ip, docker_services):
    port = docker_services.port_for("db", 5432)
    conn = psycopg2.connect(
        database="postgres", user='postgres', password='postgres', host=docker_ip, port=port
    )
    return conn


@pytest.fixture(scope="session")
def web_token(docker_ip, docker_services, db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                t.key
            FROM authtoken_token t
            JOIN accounts_user a ON a.id=t.user_id
            WHERE a.email='test@test.com'
        """)

        data = cursor.fetchone()
        return data[0]


@pytest.fixture(scope="session")
def criptapp_api(http_service, web_token):
    return cript.API(http_service, f"Token {web_token}", tls=False)


def test_status_code(http_service):
    status = 200
    response = requests.get(http_service + "/")

    assert response.status_code == status


def pytest_configure():
    pytest.group = None
    pytest.project = None
    pytest.collection = None
    pytest.experiment = None
    pytest.process = None
    pytest.polystyrene = None
    pytest.sec = None

    pytest.solution = None
    pytest.toluene = None
    pytest.styrene = None
    pytest.butanol = None
    pytest.methanol = None


@pytest.mark.filterwarnings("error::UserWarning")
def test_create_group_success(criptapp_api):
    pytest.group = cript.Group(name=MY_GROUP)
    criptapp_api.save(pytest.group)


def test_create_project_success(criptapp_api):
    pytest.project = cript.Project(group=pytest.group, name=MY_PROJECT)
    criptapp_api.save(pytest.project)


def test_create_collection_success(criptapp_api):
    pytest.collection = cript.Collection(project=pytest.project, name=MY_COLLECTION)
    criptapp_api.save(pytest.collection)


def test_create_experiment_success(criptapp_api):
    pytest.experiment = cript.Experiment(
        collection=pytest.collection,
        name=MY_EXPERIMENT
    )
    criptapp_api.save(pytest.experiment)


def test_create_process_success(criptapp_api):
    pytest.process = cript.Process(
        experiment=pytest.experiment,
        name=MY_PROCESS,
        type="multistep",
        description="In an argon filled glovebox, a round bottom flask was filled with 216 ml of dried toluene. The "
                    "solution of secBuLi (3 ml, 3.9 mmol) was added next, followed by styrene (22.3 g, 176 mmol) to "
                    "initiate the polymerization. The reaction mixture immediately turned orange. After 30 min, "
                    "the reaction was quenched with the addition of 3 ml of methanol. The polymer was isolated by "
                    "precipitation in methanol 3 times and dried under vacuum."
    )
    criptapp_api.save(pytest.process)


def test_create_material(criptapp_api):
    pytest.solution = cript.Material(project=pytest.project, name="SecBuLi solution 1.4M cHex")
    criptapp_api.save(pytest.solution)

    pytest.toluene = cript.Material(project=pytest.project, name="toluene")
    criptapp_api.save(pytest.toluene)

    pytest.styrene = cript.Material(project=pytest.project, name="styrene")
    criptapp_api.save(pytest.styrene)

    pytest.butanol = cript.Material(project=pytest.project, name="1-butanol")
    criptapp_api.save(pytest.butanol)

    pytest.methanol = cript.Material(project=pytest.project, name="methanol")
    criptapp_api.save(pytest.methanol)


def test_create_inventory(criptapp_api):
    inv = cript.Inventory(collection=pytest.collection, name=MY_INVENTORY, materials=[
        pytest.solution, pytest.toluene, pytest.styrene, pytest.butanol, pytest.methanol
    ])
    criptapp_api.save(inv)


def test_get_material(criptapp_api, http_service, db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT uid from core_inventory WHERE name='{MY_INVENTORY}'
        """)
        inventory_uid = cursor.fetchone()[0]
        url = f"{http_service}/inventory/{inventory_uid}/"
        inv = criptapp_api.get(url)
        assert type(inv.materials[0]) is cript.nodes.Material


def test_add_ingredient_to_process_node(criptapp_api, http_service, db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT uid from core_inventory WHERE name='{MY_INVENTORY}'
        """)
        inventory_uid = cursor.fetchone()[0]
        url = f"{http_service}/inventory/{inventory_uid}/"
        inv = criptapp_api.get(url)

    solution = next((mat for mat in inv.materials if mat.name == 'SecBuLi solution 1.4M cHex'), None)
    toluene = next((mat for mat in inv.materials if mat.name == 'toluene'), None)
    styrene = next((mat for mat in inv.materials if mat.name == 'styrene'), None)
    butanol = next((mat for mat in inv.materials if mat.name == '1-butanol'), None)
    methanol = next((mat for mat in inv.materials if mat.name == 'methanol'), None)

    # define Quantity nodes indicating the amount of each Ingredient.
    initiator_qty = cript.Quantity(key="volume", value=0.017, unit="ml")
    solvent_qty = cript.Quantity(key="volume", value=10, unit="ml")
    monomer_qty = cript.Quantity(key="mass", value=0.455, unit="g")
    quench_qty = cript.Quantity(key="volume", value=5, unit="ml")
    workup_qty = cript.Quantity(key="volume", value=100, unit="ml")

    # create Ingredient nodes for each.
    initiator = cript.Ingredient(
        keyword="initiator",
        material=solution,
        quantities=[initiator_qty]
    )
    solvent = cript.Ingredient(
        keyword="solvent",
        material=toluene,
        quantities=[solvent_qty]
    )
    monomer = cript.Ingredient(
        keyword="monomer",
        material=styrene,
        quantities=[monomer_qty]
    )
    quench = cript.Ingredient(
        keyword="quench",
        material=butanol,
        quantities=[quench_qty]
    )
    workup = cript.Ingredient(
        keyword="workup",
        material=methanol,
        quantities=[workup_qty]
    )

    pytest.process.add_ingredient(initiator)
    pytest.process.add_ingredient(solvent)
    pytest.process.add_ingredient(monomer)
    pytest.process.add_ingredient(quench)
    pytest.process.add_ingredient(workup)

    # add the Ingredient nodes to the Process node.
    pytest.process.add_ingredient(initiator)
    pytest.process.add_ingredient(solvent)
    pytest.process.add_ingredient(monomer)
    pytest.process.add_ingredient(quench)
    pytest.process.add_ingredient(workup)


def test_add_condition_nodes_to_process_nodes(criptapp_api):
    temp = cript.Condition(key="temperature", value=25, unit="celsius")
    time = cript.Condition(key="time_duration", value=60, unit="min")
    pytest.process.add_condition(temp)
    pytest.process.add_condition(time)


def test_add_property_node_to_process_node(criptapp_api):
    yield_mass = cript.Property(
        key="yield_mass",
        value=0.47,
        unit="g",
        method="scale"
    )
    pytest.process.add_property(yield_mass)


def test_create_material_process_product(criptapp_api):
    pytest.polystyrene = cript.Material(project=pytest.project, name="polystyrene")

    names = cript.Identifier(
        key="names",
        value=["poly(styrene)", "poly(vinylbenzene)"]
    )
    bigsmiles = cript.Identifier(
        key="bigsmiles",
        value="[H]{[>][<]C(C[>])c1ccccc1[<]}C(C)CC"
    )
    chem_repeat = cript.Identifier(key="chem_repeat", value="C8H8")
    cas = cript.Identifier(key="cas", value="100-42-5")

    pytest.polystyrene.add_identifier(names)
    pytest.polystyrene.add_identifier(chem_repeat)
    pytest.polystyrene.add_identifier(bigsmiles)
    pytest.polystyrene.add_identifier(cas)

    phase = cript.Property(key="phase", value="solid")
    color = cript.Property(key="color", value="white")

    pytest.polystyrene.add_property(phase)
    pytest.polystyrene.add_property(color)

    criptapp_api.save(pytest.polystyrene)
    pytest.process.add_product(pytest.polystyrene)
    criptapp_api.save(pytest.process)


def test_create_data_node(criptapp_api):
    pytest.sec = cript.Data(
        experiment=pytest.experiment,
        name="Crude SEC of polystyrene",
        type="sec_trace",
    )
    criptapp_api.save(pytest.sec)

    # Associate a Data node with a Property node
    mw_n = cript.Property(key="mw_n", value=5200, unit="g/mol")
    mw_n.data = pytest.sec
    pytest.polystyrene.add_property(mw_n)
    criptapp_api.save(pytest.polystyrene)


def test_create_file_node_and_upload(criptapp_api):
    with mock.patch.object(cript.API, 'save', new=lambda *args: None):
        with NamedTemporaryFile(suffix='.csv') as tmp:
            f = cript.File(project=pytest.project, data=[pytest.sec], source=tmp.name)
            criptapp_api.save(f)
