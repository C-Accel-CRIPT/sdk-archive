import cript

# Connect to database
username = "DW_cript"
password = "YXMaoE1"
project = "cript_testing"
database = "test"
db = cript.CriptDB(username, password, project, database)

# Generate node
node = cript.User(
    name="Dylan",
    email="Dylan6@cript.edu",
    orcid="0000-0000-0000-0001",
    organization="MIT",
    position="Research Assistant"
)

print(node)

# save
db.save(node)


# ... example continues in groups
