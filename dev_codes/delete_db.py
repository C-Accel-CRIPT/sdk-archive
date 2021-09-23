from cript import *

db_username = "DW_cript"
db_password = "YXMaoE1"
db_project = "cript_testing"
db_database = "test"
user = "dylanwal@mit.edu"
db = CriptDB(db_username, db_password, db_project, db_database, user)

for i in db.db_collections:
   ### db.db[i].drop()  ## Danger deletes whole database!!!!!!!!!!!!!!!!!!!

print("done")
