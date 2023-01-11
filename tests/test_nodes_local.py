# This file is created to test the SDK locally

from tempfile import NamedTemporaryFile
from unittest import mock

import pytest

import cript

MY_GROUP = "MyGroup"
MY_PROJECT = "MyProject"
MY_COLLECTION = "MyCollection"
MY_EXPERIMENT = "MyExperiment"
MY_INVENTORY = "MyInventory"
MY_PROCESS = "MyProcess"


@pytest.fixture(scope="session")
def criptapp_api():
    """
    create api for the rest of the tests to use
    """
    host = "127.0.0.1:8000"
    token = ""

    return cript.API(host, token, tls=False)


# warnings are failures
@pytest.mark.filterwarnings("error::UserWarning")
def test_create_group(criptapp_api):
    """
    test creating a group
    """
    group = cript.Group(name=MY_GROUP)
    group.save()


def test_create_project(criptapp_api):
    """
    create project and save it
    """
    project = cript.Project(name=MY_PROJECT)
    project.save()


def test_create_collection(criptapp_api):
    """
    test creating a collection
    """
    proj = cript.Project.get(name=MY_PROJECT)
    coll = cript.Collection(project=proj, name=MY_COLLECTION)
    coll.save()


def test_create_experiment(criptapp_api):
    """
    create an experiment

    tests getting collection too
    """
    coll = cript.Collection.get(name=MY_COLLECTION)
    expt = cript.Experiment(collection=coll, name=MY_EXPERIMENT)

    expt.save()


def test_create_process(criptapp_api):
    """
    get an experiment
    create and save process node
    """
    expt = cript.Experiment.get(name=MY_EXPERIMENT)

    process = cript.Process(
        experiment=expt,
        type="multistep",
        name=MY_PROCESS,
        description="this is my description",
    )
    process.save()


def test_create_material(criptapp_api):
    """
    create materials
    """
    proj = cript.Project.get(name=MY_PROJECT)

    cript.Material.create(project=proj, name="SecBuLi solution 1.4M cHex")
    cript.Material.create(project=proj, name="toluene")
    cript.Material.create(project=proj, name="styrene")
    cript.Material.create(project=proj, name="1-butanol")
    cript.Material.create(project=proj, name="methanol")


def test_create_inventory(criptapp_api):
    """
    puts materials in inventory

    tests both getting a material and inputting them into inventory as well
    """
    coll = cript.Collection.get(name=MY_COLLECTION)

    solution = cript.Material.get(name="SecBuLi solution 1.4M cHex")
    toluene = cript.Material.get(name="toluene")
    styrene = cript.Material.get(name="styrene")
    butanol = cript.Material.get(name="1-butanol")
    methanol = cript.Material.get(name="methanol")

    inv = cript.Inventory(
        collection=coll,
        name=MY_INVENTORY,
        materials=[solution, toluene, styrene, butanol, methanol],
    )

    inv.save()


# works without specifying collection
def test_get_inventory(criptapp_api):
    # get collection
    coll = cript.Collection.get(name=MY_COLLECTION)

    # get inventory
    inventory = cript.Inventory.get(name=MY_INVENTORY)


def test_create_quantity_nodes(criptapp_api):
    # get collection
    coll = cript.Collection.get(name=MY_COLLECTION)

    # get inventory
    inventory = cript.Inventory.get(name=MY_INVENTORY, )

    # get materials from inventory
    solution = inventory['SecBuLi solution 1.4M cHex']
    toluene = inventory['toluene']
    styrene = inventory['styrene']
    butanol = inventory['1-butanol']
    methanol = inventory['methanol']

    # create quantity nodes
    initiator_qty = cript.Quantity(key="volume", value=0.017, unit="ml")
    solvent_qty = cript.Quantity(key="volume", value=10, unit="ml")
    monomer_qty = cript.Quantity(key="mass", value=0.455, unit="g")
    quench_qty = cript.Quantity(key="volume", value=5, unit="ml")
    workup_qty = cript.Quantity(key="volume", value=100, unit="ml")


def test_add_ingredients_to_process(criptapp_api):
    """
    get inventory
    get materials from inventory
    create quantity nodes
    add materials to process
    """
    # get collection
    coll = cript.Collection.get(name=MY_COLLECTION)

    # get inventory
    inventory = cript.Inventory.get(name=MY_INVENTORY)

    # get process
    prcs = cript.Process.get(name=MY_PROCESS)

    # get materials from inventory
    solution = inventory['SecBuLi solution 1.4M cHex']
    toluene = inventory['toluene']
    styrene = inventory['styrene']
    butanol = inventory['1-butanol']
    methanol = inventory['methanol']

    # create quantity nodes
    initiator_qty = cript.Quantity(key="volume", value=0.017, unit="ml")
    solvent_qty = cript.Quantity(key="volume", value=10, unit="ml")
    monomer_qty = cript.Quantity(key="mass", value=0.455, unit="g")
    quench_qty = cript.Quantity(key="volume", value=5, unit="ml")
    workup_qty = cript.Quantity(key="volume", value=100, unit="ml")

    # create ingredient nodes
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

    prcs.add_ingredient(initiator)
    prcs.add_ingredient(solvent)
    prcs.add_ingredient(monomer)
    prcs.add_ingredient(quench)
    prcs.add_ingredient(workup)


# TODO this needs a remove conditions from process
def test_add_condition_nodes_to_process_nodes(criptapp_api):
    """
    get process
    create conditions
    add conditions to process
    """
    prcs = cript.Process.get(name=MY_PROCESS)

    temp = cript.Condition(key="temperature", value=25, unit="celsius")
    time = cript.Condition(key="time_duration", value=60, unit="min")

    prcs.add_condition(temp)
    prcs.add_condition(time)


def test_add_property_node_to_process_node(criptapp_api):
    """
    get process
    create property
    add property to process
    """
    prcs = cript.Process.get(name=MY_PROCESS)
    yield_mass = cript.Property(key="yield_mass", value=0.47, unit="g", method="scale")
    prcs.add_property(yield_mass)


def test_create_material_process_product(criptapp_api):
    proj = cript.Project.get(name=MY_PROJECT)
    prcs = cript.Process.get(name=MY_PROCESS)
    polystyrene = cript.Material(project=proj, name="polystyrene")

    names = cript.Identifier(key="alternative_names", value=["poly(styrene)", "poly(vinylbenzene)"])
    bigsmiles = cript.Identifier(
        key="bigsmiles", value="[H]{[>][<]C(C[>])c1ccccc1[<]}C(C)CC"
    )
    chem_repeat = cript.Identifier(key="chem_repeat", value="C8H8")
    cas = cript.Identifier(key="cas", value="100-42-5")

    polystyrene.add_identifier(names)
    polystyrene.add_identifier(chem_repeat)
    polystyrene.add_identifier(bigsmiles)
    polystyrene.add_identifier(cas)

    phase = cript.Property(key="phase", value="solid")
    color = cript.Property(key="color", value="white")

    polystyrene.add_property(phase)
    polystyrene.add_property(color)
    polystyrene.save()

    prcs.add_product(polystyrene)
    prcs.save()


def test_create_data_node(criptapp_api):
    expt = cript.Experiment.get(name=MY_EXPERIMENT)
    polystyrene = cript.Material.get(name="polystyrene")

    sec = cript.Data(experiment=expt, name="Crude SEC of polystyrene", type="sec_trace")
    sec.save()

    # Associate a Data node with a Property node
    mw_n = cript.Property(key="mw_n", value=5200, unit="g/mol")
    mw_n.data = sec
    polystyrene.add_property(mw_n)
    polystyrene.save()


def test_create_file_node_and_upload(criptapp_api):
    proj = cript.Project.get(name=MY_PROJECT)
    # path = "C:\\Users\\navid\\OneDrive\\Desktop\\CRIPT Excel Templates\\Example_CRIPT_template.xlsx"
    path = "https://google.com"
    f = cript.File(project=proj, source=path)
    f.save()


# delete
def test_delete_collection(criptapp_api):
    """
    test creating a collection
    """
    proj = cript.Project.get(name=MY_PROJECT)
    coll = cript.Collection.get(name=MY_COLLECTION, project=proj.uid)
    coll.delete()


def test_delete_experiment(criptapp_api):
    coll = cript.Collection.get(name=MY_COLLECTION)
    expt = cript.Experiment.get(collection=coll.uid, name=MY_EXPERIMENT)
    expt.delete()


def test_delete_project(criptapp_api):
    """
    create project and save it
    """
    project = cript.Project.get(name=MY_PROJECT)
    project.delete()


def test_delete_group(criptapp_api):
    """
    test creating a group
    """
    group = cript.Group.get(name=MY_GROUP)
    group.delete()
