# Collection

## Definition

A `Collection` is nested inside of a <a href="../experiment" target="_blank">`Project`</a> node.
A `Collection` node can be thought as a folder/bucket that can hold either an 
<a href="../experiment" target="_blank">`Experiment`</a> or 
<a href="../inventory" target="_blank">`Inventory`</a> node.

## Attributes

| Attribute             | Type                                                | Example                  | Description                                                                             | Required |
|-----------------------|-----------------------------------------------------|--------------------------|-----------------------------------------------------------------------------------------|----------|
| url                   | str                                                 | "https://criptapp.org/api/collection/336d0584-04f9-49fe-9c0d-78772e2f1ead/" | Unique URL for the node              | True     |
| uid                   | str                                                 | "336d0584-04f9-49fe-9c0d-78772e2f1ead" | Unique ID for the node                                                    | True     |
| group                 | [Group](../supporting_nodes/group.md)               |                          | Group that owns the `Collection` node                                                   | True     |
| project                 | [Project](../project.md)                          |                          | Project associated with the `Collection` node                                           | True     |
| name                  | str                                                 | "Navid's collection"     | Name of the `Collection`  node                                                          | True     |
| experiments           | list[[Experiment](experiment.md)]                   | [exp_1, exp_2, exp_3]    | Experiments that relate to the `Collection` node                                        | False    |
| inventories           | list[[Inventory](inventory.md)]                     | [inv_1, inv_2, inv_3]    | Inventories owned by the `Collection` node                                              | False    |
| citations             | list[[Citation](../subobjects/citation.md)]         |                          | Reference to a book, paper, or scholarly work                                           | False    |
| created_at            | datetime                                            | "2022-11-23T00:59:01.453731Z" | Date and time the `Collection` node was created (UTC time)                         | True     |
| updated_at            | datetime                                            | "2022-11-23T00:59:01.453756Z" | Date and time the `Collection` node was last modified (UTC time)                   | True     |
| public                | bool                                                | False                    | Boolean indicating whether the node is publicly viewable | True     |

## Example
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

## Navigating to Collection
`Collections` can be easily found on <a href="https://criptapp.org" target="_blank">CRIPT</a> home screen in the 
<a href="https://criptapp.org/collection/" target="_blank">Collections link</a>

<br/>

!!! warning "Collection names"
    Collection names Must be unique within a <a href="../project" target="_blank">Project</a>

## Methods

### Create Collection

_Definition:_

The `.create()` method can be used to create a new Collection and save it in one line.

`cript.Collection.create(get_level=0, update_existing=False, **kwargs)`

_Example:_

Creating a `Collection` called *"My Collection"*

```python
my_collection = cript.Collection.create(name="My collection")
```

_Returns:_

Created Collection node of type `cript.data_model.nodes.BaseNode`

---

### Save Collection

_Definition:_

By saving a node it will be committed to the CRIPT database and saved there
`cript.Collection.create()`


_Example:_

Creating a Collection node named _"My Collection"_ and saving it to CRIPT

```python
my_collection = cript.Collection.create(name="My collection")
my_collection.save()
```

_Returns:_

None

_Parameters:_

| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `get_level`       | int     | Level to recursively get nested nodes                          | 0       |
| `update_existing` | boolean | Indicates whether to update an existing node in CRIPT database | False   |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |


---
### Get Collection

_Definition:_

Get a Collection that has already been saved into CRIPT

`cript.Collection.get(get_level=0, **kwargs)`

<div style="margin-bottom: 2rem"></div>

_Get Collection Node via UID:_
``` python
my_collection = cript.Collection.get(uid="015fc459-ea9f-4c37-80aa-f51d509095df")
```

_Get Collection Node via URL:_
``` python
my_collection = cript.Collection.get(url="https://criptapp.org/collection/015fc459-ea9f-4c37-80aa-f51d509095df/")
```

_Get Collection Node via Name:_

``` python
project = cript.Project.get(name="My project")
collection = cript.Collection.get(name="My collection", project=project)
```

??? info "Why Project is needed"
    When getting a Collection via name, the project must also be specified since collection is nested under project and the collection name is only unique among other collections within the project.

_Returns:_

CRIPT Collection node of type `cript.data_model.nodes.BaseNode`


_Parameters:_


| Name        | Type   | Description                                          | Default |
|-------------|--------|------------------------------------------------------|---------|
| `name`      | string | Name of the Collection to get                        | " "     |
| `project`   | string | Project name that the Collection is nested inside of | " "     |
| `uid`       | string | UID of the specific Collection to get                | " "     |
| `url`       | string | URL of the specific Collection to get                | " "     |
| `get_level` | int    | Level to recursively get nested nodes                | 0       |
| `**kwargs`  |        | Arguments for the constructor.                       | `{}`    |


---

### Update Collection

_Definition:_

Update a saved Collection node with new values

`cript.Collection.update(get_level=0, **kwargs)`

_Example:_

```python
my_collection.update(name="My new collection name")
```

_Returns:_

None

_Parameters:_


| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `get_level`       | int     | Level to recursively get nested nodes                          | 0       |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |

---
### Refresh Collection

_Definition:_

Refresh a node to get the latest saved values from CRIPT

`cript.Collection.refresh(get_level=0)`

_Example:_

```python
my_collection.refresh(name="My new collection name")
```

_Returns:_

None

_Parameters:_


| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `get_level`       | int     | Level to recursively get nested nodes                          | 0       |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |


---

### Delete Collection

_Definition:_

Delete a Collection node from CRIPT database

`cript.Collection.delete()`

_Example:_

```python
my_collection.delete()
```

_Returns:_

None

_Parameters:_


| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `get_level`       | int     | Level to recursively get nested nodes                          | 0       |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |



---

### Search Collection

_Definition:_

Search for a Collection within CRIPT. This method returns a paginator object

`cript.Collection.search(limit=None, offset=None, get_level=0, **kwargs)`

_Example:_


```python

```

_Returns:_

A Paginator object of type `cript.data_model.paginator.Paginator`

_Parameters:_


| Name        | Type             | Description                           | Default |
|-------------|------------------|---------------------------------------|---------|
| `limit`     | Union[int, None] | The max number of items to return     | None    |
| `offset`    | Union[int, None] | The starting position of the query    | None    |
| `get_level` | int              | Level to recursively get nested nodes | 0       |
| `**kwargs`  |                  | Arguments for the constructor.        | `{}`    |
