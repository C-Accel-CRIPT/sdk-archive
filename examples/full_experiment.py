"""
Anionic Polymerization of styrene


"""

import cript as c


def create_nodes(api, project):
    ########################################
    # Organization nodes

    collection = c.Collection(project=project, name="Tutorial Examples")
    api.save(collection)
    expt = c.Experiment(
        name="Anionic Polymerization of Styrene with SecBuLi", collection=collection
    )
    api.save(expt)
    collection.experiments = [expt]
    api.save(collection)

    ##############################################
    # load materials from other example
    from create_materials import define_materials

    materials = define_materials(project)
    for material in materials:
        api.save(material)

    inventory = c.Inventory(
        collection=collection, name="Tutorial Materials", materials=materials
    )
    api.save(inventory)
    collection.experiments = [inventory]
    api.save(collection)

    ###########################################################
    # reference

    reference_node = c.Reference(
        group=project.group,
        title="Kinetics of Anionic Polymerization of Styrene in Tetrahydrofuran",
        authors=["Geacintov, C.", "Smid, J.", "Szwarc, M."],
        journal="Journal of the American Chemical Society",
        year=1962,
        issue=13,
        volume=84,
        pages=[2508],
        doi="10.1021/ja00872a012",
    )
    api.save(reference_node)

    ###########################################################
    # process
    ingr_tol = c.Ingredient(
        material=inventory["toluene"],
        keyword="solvent",
        quantities=[c.Quantity(key="volume", value=10, unit="ml")],
    )
    ingr_st = c.Ingredient(
        material=inventory["styrene"],
        quantities=[c.Quantity(key="mass", value=0.455, unit="g")],
        keyword="monomer",
    )
    ingr_meoh = c.Ingredient(
        material=inventory["methanol"],
        quantities=[c.Quantity(key="volume", value=0.1, unit="ml")],
        keyword="workup",
    )
    ingr_meoh2 = c.Ingredient(
        material=inventory["methanol"],
        quantities=[c.Quantity(key="volume", value=100, unit="ml")],
        keyword="quench",
    )
    ingr_secBuLi = c.Ingredient(
        material=inventory["SecBuLi solution 1.4M cHex"],
        quantities=[c.Quantity(key="volume", value=1, unit="ml")],
        keyword="initiator",
    )  # {"mat_id": "secBuLi"}

    process = c.Process(
        experiment=expt,
        name="Anionic of Styrene",
        type="multistep",
        ingredients=[ingr_secBuLi, ingr_tol, ingr_st, ingr_meoh, ingr_meoh, ingr_meoh2],
        description="In an argon filled glovebox, a round bottom flask was filled with 216 ml of dried toluene. The "
        "solution of secBuLi (3 ml, 3.9 mmol) was added next, followed by styrene (22.3 g, 176 mmol) to "
        "initiate the polymerization. The reaction mixture immediately turned orange. After 30 min, "
        "the reaction was quenched with the addition of 3 ml of methanol. The polymer was isolated by "
        "precipitation in methanol 3 times and dried under vacuum.",
        conditions=[
            c.Condition(key="temperature", value=25, unit="degC"),
            c.Condition(key="time_duration", value=60, unit="min"),
            c.Condition(key="atm", value="none", material=inventory["argon"]),
        ],
        properties=[
            c.Property(
                key="yield_mass",
                value=0.47,
                unit="g",
                uncertainty=0.02,
                uncertainty_type="stdev",
                method="scale",
            )
        ],
        keywords=["polymerization", "living_poly", "anionic", "solution"],
        citations=[c.Citation(type="reference", reference=reference_node)],
    )
    api.save(process)

    ###########################################################
    # data/file node
    import os

    file_path = os.getcwd() + "\\test_data"

    sec_data = c.Data(
        experiment=expt,
        name="Crude SEC of polystyrene",
        type="sec_trace",
    )

    api.save(sec_data)
    file = c.File(
        project=project,
        data=[sec_data],
        name="sec_data",
        source=file_path + "\\sec.txt",
    )
    api.save(file)
    sec_data.file = [file]
    api.save(sec_data)

    nmr_data = c.Data(
        experiment=expt,
        name="Crude 1H NMR of polystyrene",
        type="nmr_h1",
    )

    api.save(nmr_data)
    file = c.File(
        project=project,
        data=[nmr_data],
        name="nmr_data",
        source=file_path + "\\nmr.txt",
    )
    api.save(file)
    sec_data.file = [file]
    api.save(sec_data)

    ###########################################################
    # final material

    mat_poly = c.Material(
        project=project,
        name="polystyrene",
        identifiers=[
            c.Identifier(key="preferred_name", value="polystyrene"),
            c.Identifier(key="names", value=["poly(styrene)", "poly(vinylbenzene)"]),
            c.Identifier(key="chem_repeat", value="C8H8"),
            c.Identifier(key="bigsmiles", value="[H]{[>][<]C(C[>])c1ccccc1[<]}C(C)CC"),
            c.Identifier(key="cas", value="100-42-5"),
        ],
        process=process,
        properties=[
            c.Property(key="phase", value="solid"),
            c.Property(key="color", value="white"),
            c.Property(
                key="mw_n",
                method="nmr",
                value=4800,
                unit="g/mol",
                uncertainty=400,
                data=nmr_data,
            ),
            c.Property(
                key="mw_n",
                method="sec",
                value=5200,
                unit="g/mol",
                uncertainty=100,
                data=sec_data,
            ),
            c.Property(
                key="mw_d", method="sec", value=1.03, uncertainty=0.02, data=sec_data
            ),
        ],
    )
    api.save(mat_poly)


def main_local_api():
    api = c.APILocal(folder="database")

    user = c.User(username="Dylan Walsh", email="dylanwal@cript.edu", orcid_id="")
    api.save(user)
    group = c.Group(name="SDK test group")
    api.save(group)
    project = c.Project(name="SDK test project", group=group)
    api.save(project)

    create_nodes(api, project)


def main_web_api():
    import pathlib

    host = "criptapp.org"
    with open(str(pathlib.Path(__file__).parent.parent) + "\\api_key.txt", "r") as f:
        token = f.read()
    api = c.API(host, token)

    project = c.Project(name="SDK test project")
    api.save(project)

    create_nodes(api, project)


if __name__ == "__main__":
    main_local_api()
    # main_web_api()
