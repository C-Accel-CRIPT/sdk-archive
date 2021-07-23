import cript

# Connect to database
username = "DW_cript"
password = "YXMaoE1"
project = "cript_testing"
database = "test"
db = cript.CriptDB(username, password, project, database)

# Generate node
node = cript.Collection(
    name="Dylan's Notebook"
)

print(node)

# save
db.save(node)
