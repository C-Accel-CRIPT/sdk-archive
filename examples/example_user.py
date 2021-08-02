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
    email="Dylan17@cript.edu",
    orcid="0000-0000-0000-0001",
    organization="MIT",
    position="Research Assistant"
)

print(node)

# save
db.save(node)


node.c_group = "6105a7d87be87f0d370dcfb6"
node.website = "dsfs@fisdfds.com"
node.name = "Dylan W"

db.update(node)

# ... example continues in groups
