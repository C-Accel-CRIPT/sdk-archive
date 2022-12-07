# Collection

## Definition

A collection node can be thought as a folder/bucket that can hold either an 
<a href="../experiment" target="_blank">Experiment</a> or 
<a href="../inventory" target="_blank">Inventory</a> node.

## Navigating to Collection
`Collections` can be easily found on <a href="https://criptapp.org" target="_blank">CRIPT</a> home screen in the 
<a href="https://criptapp.org/collection/" target="_blank">Collections link</a>

<br/>

!!! warning "Collection names"
    Collection names Must be unique within a <a href="../project" target="_blank">Project</a>

---

## Collection Attributes

```json

{
    "url": "https://criptapp.org/api/collection/336d0584-04f9-49fe-9c0d-78772e2f1ead/",
    "uid": "336d0584-04f9-49fe-9c0d-78772e2f1ead",
    "group": "https://criptapp.org/api/group/68ed4c57-d1ca-4708-89b2-cb1c1609ace2/",
    "project": "https://criptapp.org/api/project/910445b2-88ca-43ac-88cf-f6424e85b1ba/",
    "name": "Navid's Collecton",
    "notes": null,
    "experiments": "https://criptapp.org/api/collection/336d0584-04f9-49fe-9c0d-78772e2f1ead/experiments/",
    "inventories": "https://criptapp.org/api/collection/336d0584-04f9-49fe-9c0d-78772e2f1ead/inventories/",
    "citations": [],
    "created_at": "2022-11-23T00:59:01.453731Z",
    "updated_at": "2022-11-23T00:59:01.453756Z",
    "public": false
}

```

---
## Methods

### Create Collection

**Definition**

The `.create()` method can be used to create a new Collection and save it in one line.

`cript.Collection.create(get_level=0, update_existing=False, **kwargs)`

**Example**

Creating a `Collection` called *"My Collection"*

```python
my_collection = cript.Collection.create(name="My collection")
```

**Returns**

Created Collection node of type `cript.data_model.nodes.BaseNode`

---

### Save Collection

**Definition**

By saving a node it will be committed to the CRIPT database and saved there
`cript.Collection.create()`


**Example**

Creating a Collection node named _"My Collection"_ and saving it to CRIPT

```python
my_collection = cript.Collection.create(name="My collection")
my_collection.save()
```

**Returns**

None

**Parameters**

| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `get_level`       | int     | Level to recursively get nested nodes                          | 0       |
| `update_existing` | boolean | Indicates whether to update an existing node in CRIPT database | False   |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |


---
### Get Collection

**Definition**

Get a Collection that has already been saved into CRIPT

`cript.Collection.get(get_level=0, **kwargs)`

<div style="margin-bottom: 2rem"></div>

**Get Collection Node via Name**
``` python
my_collection = cript.Collection.get(name="My collection")
```

**Get Collection Node via UID**
``` python
my_collection = cript.Collection.get(uid="015fc459-ea9f-4c37-80aa-f51d509095df")
```

**Get Collection Node via URL**
``` python
my_collection = cript.Collection.get(url="https://criptapp.org/collection/015fc459-ea9f-4c37-80aa-f51d509095df/")
```

**Returns**

CRIPT Collection node of type `cript.data_model.nodes.BaseNode`


**Parameters**


| Name        | Type   | Description                           | Default |
|-------------|--------|---------------------------------------|---------|
| `name`      | string | name of the Collection to get         | ""      |
| `uid`       | string | UID of the specific Collection to get | ""      |
| `url`       | string | URL of the specific Collection to get | ""      |
| `get_level` | int    | Level to recursively get nested nodes | 0       |
| `**kwargs`  |        | Arguments for the constructor.        | `{}`    |


---

### Update Collection

**Definition**

Update a saved Collection node with new values

`cript.Collection.update(get_level=0, **kwargs)`

**Example**

```python
my_collection.update(name="My new collection name")
```

**Returns**

None

**Parameters**


| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `get_level`       | int     | Level to recursively get nested nodes                          | 0       |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |

---
### Refresh Collection

**Definition**

Refresh a node to get the latest saved values from CRIPT

`cript.Collection.refresh(get_level=0)`

**Example**

```python
my_collection.refresh(name="My new collection name")
```

**Returns**

None

**Parameters**


| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `get_level`       | int     | Level to recursively get nested nodes                          | 0       |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |


---

### Delete Collection

**Definition**

Delete a Collection node from CRIPT database

`cript.Collection.delete()`

**Example**

```python
my_collection.delete()
```

**Returns**

None

**Parameters**


| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `get_level`       | int     | Level to recursively get nested nodes                          | 0       |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |



---

### Search Collection

**Definition**

Search for a Collection within CRIPT. This method returns a paginator object

`cript.Collection.search(limit=None, offset=None, get_level=0, **kwargs)`

**Example**


```python

```

**Returns**

A Paginator object of type `cript.data_model.paginator.Paginator`

**Parameters**


| Name        | Type             | Description                           | Default |
|-------------|------------------|---------------------------------------|---------|
| `limit`     | Union[int, None] | The max number of items to return     | None    |
| `offset`    | Union[int, None] | The starting position of the query    | None    |
| `get_level` | int              | Level to recursively get nested nodes | 0       |
| `**kwargs`  |                  | Arguments for the constructor.        | `{}`    |