import cript

# Connect to database
username = "DW_cript"
password = "YXMaoE1"
project = "cript_testing"
database = "test"
db = cript.CriptDB(username, password, project, database)

# Generate node
node = cript.Publication(
    title="Engineering of Molecular Geometry in Bottlebrush Polymers",
    authors=["Walsh, Dylan J.", "Dutta, Sarit", "Sing, Charles E.", "Guironnet, Damien"],
    journal="Macromolecules",
    publisher="American Chemical Society",
    year=2019,
    volume=52,
    issue=13,
    pages="4847-4857",
    doi="10.1021/acs.macromol.9b00845",
    issn="0024-9297",
    website="http://pubs.acs.org/doi/10.1021/acs.macromol.9b00845"
)

print(node)

# save
db.save(node)
