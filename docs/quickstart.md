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
api = cript.API(host, token)
```
!!! note
    Your API token can be found in the UI under Account Settings.

---

# Example Tasks

## Create a node
For example, create a Group:
``` py
group = cript.Group(name="MyGroup")
api.save(group)
```
... then a Project:
``` py
project = cript.Project(group=group, name="MyProject")
api.save(project)
```
... then a Collection:
``` py
collection = cript.Collection(project=project, name="MyCollection")
api.save(collection)
```
!!! note
    By default, all nodes are private. You can make them public with the `public=True` argument.

## Update a node
For example, update the Collection node created above:
``` py
collection.name = "OurCollection"
api.save(collection)
```

## Delete a node
For example, delete the Collection node created above:
``` py
api.delete(collection)
```

## Get an existing node
For example, get the official CRIPT Project node:
``` py
project = api.get(cript.Project, {"name": "CRIPT"})
```
... then get the official styrene Material node via CAS number:
``` py
query = {
    "project": project.uid,
    "identifiers": [
        {
            "key": "cas",
            "value": "100-42-5"
        }
    ]
}
styrene =  api.get(cript.Material, query)
```
... or get it via URL:
``` py
url = "https://criptapp.org/api/material/8edbde8a-edce-4ad8-bf52-bd1ef81ba399/"
styrene =  api.get(url)
```


## Run a search query
For example, search for Material nodes with a molar mass less than 10 g/mol:
``` py
query = {
    "properties": [
        {
            "key": "molar_mass",
            "value__lt": 10,
            "unit": "g/mol"
        }
    ]
}
results =  api.search(cript.Material, query)
```

... then paginate through the results.
``` py
results.next         # Flip to the next page
results.previous     # Flip to the previous page
results.to_page(10)  # Flip to page 10 (or any other)
```

## Upload a file
First, you'll need a Project and Data node:
``` py
project = api.get("<project_url>")
data = api.get("<data_url>")
```
Next, create a File node that points to your local file:
``` py
path = "path/to/local/file"
f = cript.File(project=project, data=[data], source=path)
api.save(file)
```

## Download a file
For example, download the file you uploaded above.
``` py
path = "path/to/local/file"
api.download_file(f, path=path)
```
!!! note
    The default path for a download is your current directory.
