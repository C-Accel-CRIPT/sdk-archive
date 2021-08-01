import cript

# Connect to database
username = "DW_cript"
password = "YXMaoE1"
project = "cript_testing"
database = "test"
user = "61058db26cfbd79a33216d30"
db = cript.CriptDB(username, password, project, database, user)

# Generate node
node = cript.Group(
    name="tutorial2",
    website="www.test.com"
)

# save
db.save(node)

me = db.view("61058db26cfbd79a33216d30")
node2 = cript.load(me)
node2.c_group = node

print(node2)


