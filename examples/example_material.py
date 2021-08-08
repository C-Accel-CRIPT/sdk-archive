import cript as C


# Connect to database
db_username = "DW_cript"
db_password = "YXMaoE1"
db_project = "cript_testing"
db_database = "test"
user = "johndoe13@cript.edu"
db = C.CriptDB(db_username, db_password, db_project, db_database, user)

iden = [C.Identifiers(
    preferred_name="styrene",
    names=["vinylbenzene", "phenylethylene", "ethenylbenzene"],
    chem_formula="C8H8",
    smiles="C=Cc1ccccc1",
    cas="100-42-5",
    pubchem_cid="7501",
    inchi_key="PPBRXRYQALVLMV-UHFFFAOYSA-N"
)]

# Generate node
node = C.Material(
    identifier=iden,
    keywords=["styrene"],
    storage=[
        C.Cond(key="temp", value=-20, unit=Unit("degC")),
        C.Cond(key="atm", value="argon")
    ]
    )

# add properties
prop = [C.Prop(mat_id=0, key="phase", value="liquid"),
        C.Prop(mat_id=0, key="color", value="colorless"),
        C.Prop(mat_id=0, key="mw", value=104.15, unit=Unit("g/mol"), method="prescribed"),
        C.Prop(mat_id=0, key="density", value=0.906, unit=Unit("g/ml"),
                   conditions=[C.Cond(key="temp", value=25, unit=Unit("degC"))]
                   ),
        C.Prop(mat_id=0, key="bp", value=145, unit=Unit("degC"),
                   conditions=[C.Cond(key="pressure", value=1, unit=Unit("atm"))]
                   ),
        C.Prop(mat_id=0, key="mp", value=-30, unit=Unit("degC"),
                   conditions=[C.Cond(key="pressure", value=1, unit=Unit("bar"))]
                   ),
        C.Prop(mat_id=0, key="solubility", value=0.3, unit=Unit("g/mol"),
                   conditions=[
                             C.Cond(key="temp", value=25, unit=Unit("degC")),
                             C.Cond(key="solvent", value="water", unit=Unit("bar"))
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
