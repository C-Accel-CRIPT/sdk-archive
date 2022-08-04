"""
Anionic Polymerization of styrene


"""
import cript as c


api = c.APILocal(folder="database")

# Permission and Organization nodes
user = c.User(
    username="Dylan Walsh",
    email="dylanwal@cript.edu",
    orcid_id=""
)
api.save(user)

group = c.Group(name="example 1 group", users=[user])
api.save(group)
project = c.Project(group=group, name="Tutorial Examples")
api.save(project)
collection = c.Collection(group=group, project=project, name="Tutorial Examples")
api.save(collection)
expt = c.Experiment(group=group, name="Anionic Polymerization of Styrene with SecBuLi", collection=collection)
api.save(expt)
collection.experiments = [expt]
api.save(collection)

from create_materials import define_materials
materials = define_materials(project)
for material in materials:
    api.save(material)

inventory = c.Inventory(group=group, collection=collection, name="Tutorial Materials", materials=materials)
api.save(inventory)
###########################################################

ingr_tol = c.Ingredient(material=inventory["toluene"], keyword="solvent",
                        quantities=[c.Quantity(key="volume", value=10, unit="ml")])
ingr_st = c.Ingredient(material=inventory["styrene"], quantities=[c.Quantity(key="mass", value=0.455, unit="g")],
                       keyword="monomer")
ingr_meoh = c.Ingredient(material=inventory["methanol"], quantities=[c.Quantity(key="volume", value=0.1, unit="ml")],
                       keyword="workup")
ingr_meoh2 = c.Ingredient(material=inventory["methanol"], quantities=[c.Quantity(key="volume", value=100, unit="ml")],
                       keyword="quench")
ingr_secBuLi = c.Ingredient(material=inventory["SecBuLi solution 1.4M cHex"], quantities=[c.Quantity(key="volume", value=1, unit="ml")], keyword="initiator")  # {"mat_id": "secBuLi"}

process = c.Process(
    group=group,
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
        c.Condition(key="atm", value="none", material=inventory["argon"])
    ],
    properties=[
        c.Property(key="yield_mass", value=0.47, unit="g", uncertainty=0.02, uncertainty_type="stdev", method="scale")
    ],
    keywords=["polymerization", "living_poly", "anionic", "solution"]
)
api.save(process)

###########################################################

import os

file_path = os.getcwd() + "\\test_data"

sec_data = c.Data(
    group=group,
    experiment=expt,
    name="Crude SEC of polystyrene",
    type="sec_trace",
)

api.save(sec_data)
file = c.File(group=group, project=project, data=[sec_data], name="sec_data", source=file_path + "\\sec.txt")
api.save(file)
sec_data.file = [file]
api.save(sec_data)

nmr_data = c.Data(
    group=group,
    experiment=expt,
    name="Crude 1H NMR of polystyrene",
    type="nmr_h1",
)

api.save(nmr_data)
file = c.File(group=group, project=project, data=[nmr_data], name="sec_data", source=file_path + "\\nmr.txt")
api.save(file)
sec_data.file = [file]
api.save(sec_data)

###########################################################

mat_poly = c.Material(
    group =group,
    project = project,
    name = "polystyrene",
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
        c.Property(key="mw_n", method="nmr", value=4800, unit="g/mol", uncertainty=400, data=nmr_data),
        c.Property(key="mw_n", method="sec", value=5200, unit="g/mol", uncertainty=100, data=sec_data),
        c.Property(key="mw_d", method="sec", value=1.03, uncertainty=0.02, data=sec_data)
    ]
)
api.save(mat_poly)
