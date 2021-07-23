from pint.unit import Unit

import cript


# Connect to database
username = "DW_cript"
password = "YXMaoE1"
project = "cript_testing"
database = "test"
user = "60f87e2d7f47c4a26b8c5bab"
db = cript.CriptDB(username, password, project, database, user)

db.view_all("group")

iden = [cript.Identifiers(
    preferred_name="styrene",
    names=["vinylbenzene", "phenylethylene", "ethenylbenzene"],
    chem_formula="C8H8",
    smiles="C=Cc1ccccc1",
    cas="100-42-5",
    pubchem_cid="7501",
    inchi_key="PPBRXRYQALVLMV-UHFFFAOYSA-N"
)]

# Generate node
node = cript.Material(
    identifier=iden,
    keywords=["styrene"],
    storage=[
        cript.Cond(key="temp", value=-20, unit=Unit("degC")),
        cript.Cond(key="atm", value="argon")
    ]
    )

# add properties
prop = [cript.Prop(mat_id=0, key="phase", value="liquid"),
        cript.Prop(mat_id=0, key="color", value="colorless"),
        cript.Prop(mat_id=0, key="mw", value=104.15, unit=Unit("g/mol"), method="prescribed"),
        cript.Prop(mat_id=0, key="density", value=0.906, unit=Unit("g/ml"),
                   conditions=[cript.Cond(key="temp", value=25, unit=Unit("degC"))]
                   ),
        cript.Prop(mat_id=0, key="bp", value=145, unit=Unit("degC"),
                   conditions=[cript.Cond(key="pressure", value=1, unit=Unit("atm"))]
                   ),
        cript.Prop(mat_id=0, key="mp", value=-30, unit=Unit("degC"),
                   conditions=[cript.Cond(key="pressure", value=1, unit=Unit("bar"))]
                   ),
        cript.Prop(mat_id=0, key="solubility", value=0.3, unit=Unit("g/mol"),
                   conditions=[
                             cript.Cond(key="temp", value=25, unit=Unit("degC")),
                             cript.Cond(key="solvent", value="water", unit=Unit("bar"))
                         ]
                   ),
        ]

node.properties = prop

#print(node)
#print("%" * 25)
#print(repr(node))

# save
db.save(node)

print(node)
