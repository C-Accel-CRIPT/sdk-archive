## Installation

Prerequisites:
> - *Python 3.9+*
> - *Outbound Internet access*

Install with pip:
```
python3 -m pip install cript
```

## Connect to CRIPT

Establish a connection with an API endpoint:
```python
url = "https://criptapp.org"  # Public instance of CRIPT
token = "Token 123456789"  
api = cript.API(base_url=url, api_token=token)
```
<sup>**Note**: Your API token can be found in the UI under Account Settings.</sup>

---

# Example Tasks

## Create a node
For example, create a Group node:
```python
group = cript.Group(name="MyGroup")
api.save(group)
```
... then a Collection:
```python
collection = cript.Collection(group=group, name="MyCollection")
```

## Update a node
For example, update the Collection node created above:
```python
collection.name = "OurCollection"
api.save(collection)
```

## Delete a node
For example, delete the Collection node created above:
```python
api.delete(collection)
```

## Get an existing node
For example, get the official CRIPT Group node:
```python
group = api.get(cript.Group, {"name": "CRIPT"})
```
... then get the official styrene Material node via CAS number:
```python
query = {
    "group": group.uid,
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
```python
url = "https://criptapp.org/api/material/8edbde8a-edce-4ad8-bf52-bd1ef81ba399/"
styrene =  api.get(url)
```


## Run a search query
For example, search for all Material nodes that contain benzene:
```python
query = {
    "identifiers": [
        {
            "key": "bigsmiles",
            "value": "c1ccccc1"
        }
    ]
}
results =  api.search(cript.Material, query)
```

## Upload a file
First, you'll need a Group and Data node:
```python
group = data = api.get("<group_url>")
data = api.get("<data_url>")
```
Next, create a File node that points to your local file:
```python
path = "path/to/local/file"
file = cript.File(group=group, data=[data], type="data", source=path)
api.save(file)
```

## Download a file
For example, download the file you uploaded above.
```python
path = path/on/local/filesystem
api.download(file, path=path)
```
<sup>**Note**: The default path for a download parameter is your current directory.</sup>
