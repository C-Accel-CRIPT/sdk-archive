import pint

import cript
from criptdb import criptdb

u = pint.UnitRegistry()

# Connect to database
username = "DW_cript"
password = "YXMaoE1"
project = "cript_testing"
database = "test"
#db = criptdb(username, password, project, database)

iden = []
iden.append(cript.Identifiers(
    preferred_name="styrene",
    names=["styrene","vinylbenzene", "phenylethylene", "ethenylbenzene"],
    chem_formula="C8H8",
    smiles="C=Cc1ccccc1",
    cas="100-42-5",
    pubchem_cid="7501",
    inchi_key="PPBRXRYQALVLMV-UHFFFAOYSA-N"
)
)

# Generate node
node = cript.Material(
    name="Dylan's Notebook",
    identifier=iden,
)

print(node)

prop = []
prop.append(cript.Properties(mat_id=0, key="phase", value="liquid"))
prop.append(cript.Properties(mat_id=0, key="color", value="colorless"))
prop.append(cript.Properties(mat_id=0, key="mw", value=104.15, method="prescribed"))
prop.append(cript.Properties(mat_id=0, key="density", value=0.906,
                             conditions=[cript.Conditions(temp=25, unit=u.degC)]
                             ))


node.properties = prop

print(node)

# save
#db.save(node)
