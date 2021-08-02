import cript

# Connect to database
username = "DW_cript"
password = "YXMaoE1"
project = "cript_testing"
database = "test"
db = cript.CriptDB(username, password, project, database)

db.user = "6106d299f703a7528e030562"
node = db.view("6106d299f703a7528e030562")
obj = cript.load(node)
obj.c_group = "6105a9c288bfcadea0a1de22"
db.update(obj)
