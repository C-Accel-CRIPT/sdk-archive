This quick start tutorial will guide you through some common commands of the CRIPT Python SDK. For more information please visit the [full tutorial](../tutorials/full_tutorial/) or reference the documentation for individual [CRIPT nodes](../nodes/all/).

---

## Install CRIPT
As described by the [Installation tutorial](../tutorials/installation/), it is recommended to install the <a href="https://pypi.org/project/cript/" target="_blank">CRIPT package</a> inside a Python virtual environment.
   ```bash
    pip install cript
   ```
---

## Connect to CRIPT

Create a new Python script. At the top of the script, import the `cript` package and populate the host and API Token. Your API token can be found on the <a href="https://criptapp.org/security/" target="_blank">CRIPT security settings page</a>. It is *highly* recommended that you store your API token as an environment variable, as explained in the [API token tutorial](../tutorials/api_token/). Here, we assume that your API key is stored as an environment variable called `CRIPT_API_KEY`, so it can be read using the built-in Python `os` module.

``` py
import cript
import os

host = "https://criptapp.org/"  # or any host
token = os.environ.get("CRIPT_API_KEY")
cript.API(host, token, tls=True)
```

!!! warning
    Use the `tls` parameter to specify whether to use TLS encryption (`https`) for the API connection. This paramet defaults to `True`. In some cases, such as when running the CRIPT server locally, you may want to disable https and instead run the server on `http`. In this case, set `tls=False`.

---

## Create a Node

Use the `.create()` method to create a CRIPT node.

``` python
# create a project and saves it to CRIPT
proj = cript.Project.create(name="My project") 
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
