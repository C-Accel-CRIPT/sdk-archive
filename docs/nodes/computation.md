# Computation

<!-- TODO needs to be converted from material to computation -->
## Definition


## Navigating to Computation

## Available Sub-Objects for Computation

* <a href="../subobjects/identifiers" target="_blank">Identifier</a>
* <a href="../subobjects/property" target="_blank">Property</a>
* <a href="../subobjects/computational_forcefield" target="_blank">Computational_forcefield</a>


<br/>

!!! warning "Computation names"
    Computation names Must be unique within a <a href="../project" target="_blank">Project</a>

---

## Computation Attributes

```json



```

---
## Methods

### Create Computation

_Definition:_

The `.create()` method can be used to create a new Computation and save it in one line.

`cript.Computation.create(get_level=0, update_existing=False, **kwargs)`

_Example:_

Creating a `Computation` called *"My Computation"*

```python
my_Computation = cript.Computation.create(name="My Computation")
```

_Returns:_

Created Computation node of type `cript.data_model.nodes.BaseNode`

---

### Save Computation

_Definition:_

By saving a node it will be committed to the CRIPT database and saved there
`cript.Computation.create()`


_Example:_

Creating a Computation node named _"My Computation"_ and saving it to CRIPT

```python
my_Computation = cript.Computation.create(name="My Computation")
my_Computation.save()
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
### Get Computation

_Definition:_

Get a Computation that has already been saved into CRIPT

`cript.Computation.get(get_level=0, **kwargs)`

<div style="margin-bottom: 2rem"></div>

_Get Computation Node via UID:_
``` python
my_Computation = cript.Computation.get(uid="015fc459-ea9f-4c37-80aa-f51d509095df")
```

_Get Computation Node via URL:_
``` python
my_Computation = cript.Computation.get(url="https://criptapp.org/Computation/015fc459-ea9f-4c37-80aa-f51d509095df/")
```

_Get Computation Node via Name:_

``` python
project = cript.Project.get(name="My project")
Computation = cript.Computation.get(name="My Computation", project=project)
```

??? info "Why Project is needed"
    When getting a Computation via name, the project must also be specified since Computation is nested under project and the Computation name is only unique among other Computations within the project.

_Returns:_

CRIPT Computation node of type `cript.data_model.nodes.BaseNode`


_Parameters:_


| Name        | Type   | Description                                          | Default |
|-------------|--------|------------------------------------------------------|---------|
| `name`      | string | Name of the Computation to get                        | " "     |
| `project`   | string | Project name that the Computation is nested inside of | " "     |
| `uid`       | string | UID of the specific Computation to get                | " "     |
| `url`       | string | URL of the specific Computation to get                | " "     |
| `get_level` | int    | Level to recursively get nested nodes                | 0       |
| `**kwargs`  |        | Arguments for the constructor.                       | `{}`    |


---

### Update Computation

_Definition:_

Update a saved Computation node with new values

`cript.Computation.update(get_level=0, **kwargs)`

_Example:_

```python
my_Computation.update(name="My new Computation name")
```

_Returns:_

None

_Parameters:_


| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `get_level`       | int     | Level to recursively get nested nodes                          | 0       |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |

---
### Refresh Computation

_Definition:_

Refresh a node to get the latest saved values from CRIPT

`cript.Computation.refresh(get_level=0)`

_Example:_

```python
my_Computation.refresh(name="My new Computation name")
```

_Returns:_

None

_Parameters:_


| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `get_level`       | int     | Level to recursively get nested nodes                          | 0       |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |


---

### Delete Computation

_Definition:_

Delete a Computation node from CRIPT database

`cript.Computation.delete()`

_Example:_

```python
my_Computation.delete()
```

_Returns:_

None

_Parameters:_


| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `get_level`       | int     | Level to recursively get nested nodes                          | 0       |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |



---

### Search Computation

_Definition:_

Search for a Computation within CRIPT. This method returns a paginator object

`cript.Computation.search(limit=None, offset=None, get_level=0, **kwargs)`

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