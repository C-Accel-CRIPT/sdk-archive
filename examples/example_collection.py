import cript
from criptdb import criptdb

# Connect to database
username = "DW_cript"
password = "YXMaoE1"
project = "cript_testing"
database = "test"
db = criptdb(username, password, project, database)

# Generate node
node = cript.Collection(
    name="Dylan's Notebook"
)

print(node)

# save
db.save(node)
