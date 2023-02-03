This quick start tutorial will guide you through some common commands of the CRIPT Python SDK. For more information please visit the [full tutorial](../tutorials/full_tutorial/) or reference the documentation for individual [CRIPT nodes](../nodes/all/).

---

## Install CRIPT
```bash
pip install cript
```


> It is recommended to install the <a href="https://pypi.org/project/cript/" target="_blank">CRIPT package</a> inside a [Python virtual environment](https://docs.python.org/3/library/venv.html). 

For more please refer to [CRIPT installation guide](https://docs.python.org/3/library/venv.html).

---

## Connect to CRIPT

Your API token can be found on the <a href="https://criptapp.org/security/" target="_blank">CRIPT security settings page</a>. 

!!! warning "Security Warning"
    It is **highly** recommended that you store your API token as an environment variable, as explained in the [API token tutorial](../tutorials/api_token/).

``` py
import cript
import os

host = "criptapp.org"  # or any host eg. myPrivateWebsite.come
token = os.environ.get("CRIPT_API_KEY") # getting token via environment variable
cript.API(host, token)
```

---

## Create a Node

The CRIPT data model is graph-like, which means we can think of each CRIPT object as a node which is linked to other nodes. 

All primary nodes inherit from the <a href="../nodes/bas_node/" target="_blank">BaseNode</a> class, which provides basic methods such as `create`, `save`, `get`, `search`, and `delete`.

``` python
# Instantiate a new project node and save it to CRIPT
my_project = cript.Project(name="My project")

my_project.save()

# create a new material and save it to CRIPT
my_material = cript.Material(
    project=my_project,  # the project that this material belongs to
    name="my new material",  # the material name
)

my_material.save()
```

??? info "Node.create( )"
    The `.create()` method instantiates (i.e., creates a Python object) and saves (i.e., uploads it to CRIPT) the object in one go

    Alternatively, you can instantiate the node and save it to CRIPT in one line with the `.create()` method:

    ``` python
    # create a project node and save it in one line
    proj = cript.Project.create(name="My project") 
    ```

---
## Get an existing Node

When a node is saved to the CRIPT database, it gets a unique identifier (UID), and a URL. 

The node `name`, `UID`, or `URL` can all be used to get a reference to the node using the `.get()` method.

### Get Node using its UID

```python
# get a material by its UID
my_material = cript.Material.get(uid="015fc459-ea9f-4c37-80aa-f51d509095df")
```

### Get Node using its URL
```python
# get a material by its URL
my_material = cript.Material.get(url="https://criptapp.org/material/015fc459-ea9f-4c37-80aa-f51d509095df/")
```

### Get Node using its Name
```python
my_material = cript.Material.get(
    project=my_project,  # specify which project the material is in
    name="my new material",  # specify the material name to get
)
```

!!! note "Getting objects by their UID or URL"
    Getting a node using its UID or URL is preferred over getting a node by its name, because UID and URL attributes are unique across the entire CRIPT database. 

    When getting nested nodes via `name`, you must also pass the node it belongs to (i.e., is nested under).

    For example, `Collection` is nested under `Project`:
    ```python
    proj = cript.Project.get(name="My project")
    coll = cript.Collection.get(name="My collection", project=proj.uid)
    ```

    Project does not need any other parameters because a project is the highest level node.

---

## Update a Node

The `.update()` method can be used to change the value of a specific attribute of an existing node.

```python
# change the name of an existing project
my_project.update(name="My new project name")
```

---

## Delete a Node

The `delete()` method removes an object from the CRIPT database and from memory. In some cases, deleting an object may fail when the object is linked to other nodes. In these cases, the `delete()` method produces an appropriate error message.

``` py
# delete an existing project
proj.delete()
```

---

## Run a Search Query

Existing nodes can be searched by their attributes. In contrast to the `get()` method, the `search()` method returns a `Paginator` object which may contain any number of results. For example, to search for all `Material` nodes with a molar mass less than 10 g/mol:

``` py
results = cript.Material.search(
    properties = [
        {
            "key": "molar_mass",
            "value__lt": 10,
            "unit": "g/mol"
        }
    ]
)
```

!!! Info "Pagination"
    The `search()` method returns a `Paginator` object, which allows you to paginate through the results using a special set of paginator methods:

    ``` python
    results.json()              # View the raw JSON results
    results.objects()           # Generate objects for the current page
    results.next_page()         # Flip to the next page of results (if it exists)
    results.previous_page()     # Flip to the previous page of results (if it exists)
    ```

---

## Upload a File

You may upload a file to the CRIPT database and link it to a specific project, `Data` node object, or material.
``` python
path = "path/to/local/file.txt" # set path to local file
file = cript.File(project=proj, source=path) # create the file node
file.save() # save file to CRIPT
```

---

## Download a File
Once a file is uploaded to CRIPT, it can also be downloaded again.

``` python
# local file path you want to download the file to
path = "downloaded.txt" 
file.download_file(path=path)
```

!!! info 
    The default path for a download is your current directory.
