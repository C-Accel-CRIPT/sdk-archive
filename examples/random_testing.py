from cript import *


db_username = "DW_cript"
db_password = "YXMaoE1"
db_project = "cript_testing"
db_database = "test"
user = "dylanwal@mit.edu"
db = CriptDB(db_username, db_password, db_project, db_database, user)

expt_doc = db.view(Experiment)

expt = load(expt_doc[0])

inv_doc = db.view(Inventory)

inv = load(inv_doc[0])



e = export(db.user, depth=4)


print("hi")

