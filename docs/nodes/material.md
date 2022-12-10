# Material

## Definition

A `Material` is nested inside of a `Project` node.

A `Material` is just the materials used within an experiment.

## Navigating to Material
`Materials` can be easily found on <a href="https://criptapp.org" target="_blank">CRIPT</a> home screen in the 
<a href="https://criptapp.org/material/" target="_blank">Materials link</a>

## Available Sub-Objects for Material

* <a href="../subobjects/identifiers" target="_blank">Identifier</a>
* <a href="../subobjects/property" target="_blank">Property</a>
* <a href="../subobjects/computational_forcefield" target="_blank">Computational_forcefield</a>


<br/>

!!! warning "Material names"
    Material names Must be unique within a <a href="../project" target="_blank">Project</a>

---

## Material Attributes

```json



```

---
## Methods

### Create Material

_Definition:_

The `.create()` method can be used to create a new Material and save it in one line.

`cript.Material.create(get_level=0, update_existing=False, **kwargs)`

_Example:_

Creating a `Material` called *"My Material"*

```python
my_Material = cript.Material.create(name="My Material")
```

_Returns:_

Created Material node of type `cript.data_model.nodes.BaseNode`

---

### Save Material

_Definition:_

By saving a node it will be committed to the CRIPT database and saved there
`cript.Material.create()`


_Example:_

Creating a Material node named _"My Material"_ and saving it to CRIPT

```python
my_Material = cript.Material.create(name="My Material")
my_Material.save()
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
### Get Material

_Definition:_

Get a Material that has already been saved into CRIPT

`cript.Material.get(get_level=0, **kwargs)`

<div style="margin-bottom: 2rem"></div>

_Get Material Node via UID:_
``` python
my_Material = cript.Material.get(uid="015fc459-ea9f-4c37-80aa-f51d509095df")
```

_Get Material Node via URL:_
``` python
my_Material = cript.Material.get(url="https://criptapp.org/Material/015fc459-ea9f-4c37-80aa-f51d509095df/")
```

_Get Material Node via Name:_

``` python
project = cript.Project.get(name="My project")
Material = cript.Material.get(name="My Material", project=project)
```

??? info "Why Project is needed"
    When getting a Material via name, the project must also be specified since Material is nested under project and the Material name is only unique among other Materials within the project.

_Returns:_

CRIPT Material node of type `cript.data_model.nodes.BaseNode`


_Parameters:_


| Name        | Type   | Description                                          | Default |
|-------------|--------|------------------------------------------------------|---------|
| `name`      | string | Name of the Material to get                        | " "     |
| `project`   | string | Project name that the Material is nested inside of | " "     |
| `uid`       | string | UID of the specific Material to get                | " "     |
| `url`       | string | URL of the specific Material to get                | " "     |
| `get_level` | int    | Level to recursively get nested nodes                | 0       |
| `**kwargs`  |        | Arguments for the constructor.                       | `{}`    |


---

### Update Material

_Definition:_

Update a saved Material node with new values

`cript.Material.update(get_level=0, **kwargs)`

_Example:_

```python
my_Material.update(name="My new Material name")
```

_Returns:_

None

_Parameters:_


| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `get_level`       | int     | Level to recursively get nested nodes                          | 0       |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |

---
### Refresh Material

_Definition:_

Refresh a node to get the latest saved values from CRIPT

`cript.Material.refresh(get_level=0)`

_Example:_

```python
my_Material.refresh(name="My new Material name")
```

_Returns:_

None

_Parameters:_


| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `get_level`       | int     | Level to recursively get nested nodes                          | 0       |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |


---

### Delete Material

_Definition:_

Delete a Material node from CRIPT database

`cript.Material.delete()`

_Example:_

```python
my_Material.delete()
```

_Returns:_

None

_Parameters:_


| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `get_level`       | int     | Level to recursively get nested nodes                          | 0       |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |



---

### Search Material

_Definition:_

Search for a Material within CRIPT. This method returns a paginator object

`cript.Material.search(limit=None, offset=None, get_level=0, **kwargs)`

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