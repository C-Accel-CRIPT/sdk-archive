import cript as C

# Connect to database
db_username = "DW_cript"
db_password = "YXMaoE1"
db_project = "cript_testing"
db_database = "test"
user = "johndoe13@cript.edu"
db = C.CriptDB(db_username, db_password, db_project, db_database, user)

# Generate node
node = C.Collection(
    name="Dylan's Notebook"
)


group_id = "61059603562d9b1ae64b57a1"
group = db.view(group_id)
group_node = C.load(group)

print(group_node)
print(node)

# save
db.save(node, group_node)

print(node)
print(group_node)
