import cript
from criptdb import criptdb

# Connect to database
username = "DW_cript"
password = "YXMaoE1"
project = "cript_testing"
database = "test"
db = criptdb(username, password, project, database)

# Generate initial user node
Dylan = cript.User(
    name="Dylan W",
    email="dylan@cript.edu",
    orcid="0000-0000-0000-0001",
    organization="Mass. Institute of Technology",
    position="Research Assistant"
)

# save group
db.save(Dylan)


# ... example continues in groups
