from cript import *

db_username = "DW_cript"
db_password = "YXMaoE1"
db_project = "cript_testing"
db_database = "test"
user = "dylanwal@mit.edu"
db = CriptDB(db_username, db_password, db_project, db_database, user)


# mat_cHex = Material(
#     iden=Iden(
#         name="Cyclohexane",
#         chem_formula="C6H12",
#         smiles="C1CCCCC1",
#         cas="110-82-7",
#         pubchem_cid="8078",
#         inchi_key="XDTMQSROBMDMFD-UHFFFAOYSA-N"
#     ),
#     prop=[Prop(key="phase", value="liquid"),
#           Prop(key="color", value="colorless"),
#           Prop(key="molar_mass", value=84.162 * Unit("g/mol"), method="prescribed"),
#           Prop(key="density", value=0.7739 * Unit("g/ml"),
#                cond=[Cond(key="temp", value=20 * Unit("degC"))]
#                ),
#           Prop(key="bp", value=80.74 * Unit("degC"),
#                cond=[Cond(key="pres", value=1 * Unit("atm"))]
#                ),
#           Prop(key="mp", value=6.47 * Unit("degC"),
#                cond=[Cond(key="pres", value=1 * Unit("bar"))]
#                )
#           ])
#
# db.save(mat_cHex)
# print(mat_cHex)

ddict = db.view("611db07f3cdaf1d53cdb3b2a")
a = load(ddict)
print(a)
print("hi")

