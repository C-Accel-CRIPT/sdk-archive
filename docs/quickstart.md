!!! abstract "Objective"
    This quick start guide will take you through some common commands of the CRIPT Python SDK. For more information please visit each node or the full tutorial.

---

## Install CRIPT
Install <a href="https://pypi.org/project/cript/" target="_blank">CRIPT</a> from Pypi
   ```bash
    pip install cript
   ```
---

## Connect to CRIPT

`import cript` into your python file, fill in the host and API Token, run the python file to connect to CRIPT. It is *highly* recommended that you store your API token in a safe location and read it into your code, rather than have it hard-coded. One way to do this is to store
it in an environmental variable (e.g., `CRIPT_API_KEY`) and then read it in via the `os` module.

``` py
import cript
import os

host = "criptapp.org"  # or any host
token = os.environ.get("CRIPT_API_KEY")
cript.API(host, token)
```

!!! info
    Your API token can be found in the <a href="https://criptapp.org/security/" target="_blank">Security Settings</a> under the profile icon dropdown on the top right

---

## Create a Node

``` python
proj = cript.Project.create(name="My project") # creates a Project and saves it to CRIPT
```

!!! info
    `create()` instantiates (i.e., creates a Python object) and saves (i.e., uploads to CRIPT) the object in one go

Alternatively, you can instantiate the node and then save it:

``` python
proj = cript.Project(name="My project") # instantiates Project object
proj.save() # saves the Project to CRIPT 
```

---
## Get a Node

### Get Node via UID
```python
styrene = cript.Material.get(uid="015fc459-ea9f-4c37-80aa-f51d509095df")
```

### Get Node via URL
```python
styrene = cript.Material.get(url="https://criptapp.org/material/015fc459-ea9f-4c37-80aa-f51d509095df/")
```

### Get Node via Name
```python
styrene = cript.Material.get(name="polystyrene_1")
```

!!! note "UID and URL are preferable"
    Getting a node via UID and URL are preferred methods because they are unique across the entire CRIPT database. 

    When getting nested nodes via `name`, you must pass the node it belongs to (i.e., is nested under).

    For example `Collection` is nested under `Project`:
    ```python
    proj = cript.Project.get(name="My project")
    coll = cript.Collection.get(name="My collection", project=proj.uid)
    ```

    Project does not need any other parameters because a project is the highest level node.

---

## Update a Node

```python
proj.update(name="My new project name")
```

---

## Delete a Node

``` py
coll.delete()
```

---

## Run a Search Query

For example, to search for `Material` nodes with a molar mass less than 10 g/mol:

``` py
results =  cript.Material.search(
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
    Search returns a `Paginator` object. You can paginate through the results

    ``` python
    results.json()              # View the raw JSON for the query
    results.objects()           # Generate objects for the current page
    results.next_page()         # Flip to the next page (if exists)
    results.previous_page()     # Flip to the previous page (if exists)
    ```

---

## Upload a File

``` python
path = "path/to/local/file" # path to local file
file = cript.File(project=proj, source=path) 
file.save()
```

---

## Download a File

``` python
path = "downloaded.csv" #local file path you want to save to
file.download_file(path=path)
```

!!! info 
    The default path for a download is your current directory
