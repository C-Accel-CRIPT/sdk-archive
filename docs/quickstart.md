# Crash Course

## Install CRIPT
Install <a href="https://pypi.org/project/cript/" target="_blank">CRIPT</a>
   ```bash
    pip install cript
   ```
---

## Connect to CRIPT

`import cript` into your python file, fill in the host and API Token, run the python file to connect to CRIPT

``` py
import cript

host = "criptapp.org"  # or any host
token = "<Your API Token>" # eg. token = "Token 4abc478b25e30766652f76103b978349c4c4b214"
cript.API(host, token)
```

!!! info
    Your API token can be found in the <a href="https://criptapp.org/security/" target="_blank">Security Settings</a> under the profile icon dropdown on the top right

---

## Create a Node

``` python
proj = cript.Project.create(name="My project")
proj.save()
```

??? note
    `.create()` instantiates and saves the object in one go

---
## Get a Node

### Get Node via Name
```python
proj = cript.Project.get(name="My project")
```

### Get Node via UID
```python
styrene = cript.Material.get(uid="015fc459-ea9f-4c37-80aa-f51d509095df")
```

### Get Node via URL
```python
styrene = cript.Material.get(url="https://criptapp.org/material/015fc459-ea9f-4c37-80aa-f51d509095df/")
```


---

## Update a Node

1. Get the node you want to update
2. Make the desired changes
3. Update it

```python
proj = cript.Project.get(name="My project")
proj.update(name="My new project name")
```

---

## Delete a Node
1. Get the node you want to delete
2. Delete the node

``` py
coll = cript.Collection.get(name="My collection")
coll.delete()
```

---

## Run a Search Query

For example, search for Material nodes with a molar mass less than 10 g/mol

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

??? Info "Pagination"
    Then you can paginate through the results

    ``` python
    res.json()              # View the raw JSON for the query
    res.objects()           # Generate objects for the current page
    res.next_page()         # Flip to the next page
    res.previous_page()     # Flip to the previous page
    ```

---

## Upload a File

1. Create a <a href="../node/project" target="_blank">Project</a> node
2. Create a <a href="../node/data" target="_blank">Data</a> node
3. Create a <a href="../node/data" target="_blank">File</a> node 
    1. Specify the path of the local file on your computer that you want to upload to CRIPT

``` python
path = "path/to/local/file"
file = cript.File(project=proj, source=path)
file.save()
```

---

## Download a File

1. Create a Create a <a href="../node/data" target="_blank">File</a> nod 
    1. Specify the source you want to download from
2. Specify the path you want the file to be downloaded to on your computer
3. Download the file from CRIPT

<!-- TODO what is "path" is that the path you want to download from within CRIPT? -->
``` python
file = cript.File(project=proj, source=path)
path = "path/to/local/file"
file.download_file(path=path)
```

!!! info "Default Path" 
    The default path for a download is your current directory
