## Installation

Prerequisites:
> - *Python 3.9+*
> - *Internet access*

Install with pip:
```
pip install cript
```

## Connect to CRIPT

Establish a connection with an API endpoint:
``` py
import cript

host = "<endpoint_hostname>"  # e.g., criptapp.org
token = "<your_api_token>"
cript.API(host, token)
```
!!! note
    Your API token can be found in the UI under Account Settings.

---

# Example Tasks

## Create a node
For example, create a Project:
``` py
proj = cript.Project(name="MyProject")
proj.save()
```
... then a Collection:
``` py
coll = cript.Collection.create(project=proj, name="MyCollection")
```
!!! note
    Notice the use of `create()` here, which instantiates and saves the object in one go.

## Update a node
For example, update the Project node created above:
``` py
proj.name = "OurProject"
proj.save()
```
... then the Collection:
```python
coll.update(name="OurCollection")
```
!!! note
    Notice the use of `update()` here, which updates and saves a node in one go.

## Delete a node
For example, delete the Collection node created above:
``` py
coll.delete()
```

## Get an existing node
For example, get the official CRIPT Project node:
``` py
proj = cript.Project.get(name="CRIPT")
```
... then get the official styrene Material node via name:
``` py
styrene =  cript.Material.get(project=proj.uid, name="Styrene")
```
... or via UID
``` py
styrene =  cript.Material.get(uid="<material_uid>")
```
... or via URL
```python
styrene =  cript.Material.get(url="<material_url>")
```


## Run a search query
For example, search for Material nodes with a molar mass less than 10 g/mol:
``` py
res =  cript.Material.search(
    properties = [
        {
            "key": "molar_mass",
            "value__lt": 10,
            "unit": "g/mol"
        }
    ]
)
```

... then paginate through the results.
``` py
res.json()              # View the raw JSON for the query
res.objects()           # Generate objects for the current page
res.next_page()         # Flip to the next page
res.previous_page()     # Flip to the previous page
```

## Upload a file
First, you'll need a Project and Data node:
``` py
proj = cript.Project.get(uid="<project_uid>")
data = cript.Data.get(uid="<data_uid>")
```
Next, create a File node that points to your local file:
``` py
path = "path/to/local/file"
f = cript.File(project=proj, source=path)
file.save()
```

## Download a file
For example, download the file you uploaded above.
``` py
path = "path/to/local/file"
f.download_file(path=path)
```
!!! note
    The default path for a download is your current directory.
