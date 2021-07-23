from pint.unit import Unit

import cript

# Connect to database
username = "DW_cript"
password = "YXMaoE1"
project = "cript_testing"
database = "test"
# db = cript.CriptDB(username, password, project, database)


ingredients = [
    cript.Ingredient(mat_id="secBuLi", type_="initiator", qty=[cript.Qty(0.17, Unit("ml"))]),
    cript.Ingredient(mat_id="toluene", type_="solvent", qty=[cript.Qty(10, Unit("ml"))]),
    cript.Ingredient(mat_id="styrene", type_="monomer", qty=[cript.Qty(0.455, Unit("g"))]),
    cript.Ingredient(mat_id="butanol", type_="quench", qty=[cript.Qty(5, "Eq", mat_id="secBuLi")]),
    cript.Ingredient(mat_id="methanol", type_="workup", qty=[cript.Qty(100, Unit("ml"))])
]

# Generate node
node = cript.Process(
    name="Anionic of Styrene",
    ingredients=ingredients,
    procedure="In an argon filled glovebox, a round bottom flask was filled with 216 ml of dried toluene. The "
              "solution of secBuLi (3 ml, 3.9 mmol) was added next, followed by styrene (22.3 g, 176 mmol) to "
              "initiate the polymerization. The reaction mixture immediately turned orange. After 30 min, "
              "the reaction was quenched with the addition of 3 ml of methanol. The polymer was isolated by "
              "precipitation in methanol 3 times and dried under vacuum.",
    conditions=[
        cript.Cond("temp", 25, Unit("degC")),
        cript.Cond("time", 60, Unit("min"))
    ],
    properties=[
        cript.Prop("yield_mass", 0.47, Unit("g"), 0.02, method="scale")
    ],
    keywords=["polymerization", "living_poly", "anionic", "solution"]
)


print(node)

# save
#db.save(node)
