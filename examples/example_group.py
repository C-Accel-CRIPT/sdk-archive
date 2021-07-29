import cript

# Connect to database
username = "DW_cript"
password = "YXMaoE1"
project = "cript_testing"
database = "test"
user = "60f87e2d7f47c4a26b8c5bab"
db = cript.CriptDB(username, password, project, database, user)

# Generate node
node = cript.Group(
    name="tutorial",
)

print(node)

# save
db.save(node)
