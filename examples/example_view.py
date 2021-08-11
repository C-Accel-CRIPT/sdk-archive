import cript as C


# Connect to database
db_username = "DW_cript"
db_password = "YXMaoE1"
db_project = "cript_testing"
db_database = "test"
user = "johndoe13@cript.edu"
db = C.CriptDB(db_username, db_password, db_project, db_database, user)


# current_groups = db.view(C.Group, {"scope": "all"})
current_groups = db.view(C.Collection)