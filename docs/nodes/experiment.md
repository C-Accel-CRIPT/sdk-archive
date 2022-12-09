# Experiment

## Definition

A `Experiment` is nested inside of a `Collection` node.
A `Experiment` node can be thought as a folder/bucket that can hold:

* <a href="../data" target="_blank">Data node</a>
* <a href="../process" target="_blank">Process node</a>
* <a href="../computation" target="_blank">Computations node</a>
* <a href="../computational_process" target="_blank">Computational Process node</a>

## Navigating to Experiment
`Experiments` can be easily found on <a href="https://criptapp.org" target="_blank">CRIPT</a> home screen in the 
<a href="https://criptapp.org/experiment/" target="_blank">Experiments link</a>

<br/>

!!! warning "Experiment names"
    Experiment names Must be unique within a <a href="../project" target="_blank">Collection</a>

---

## Experiment Attributes

```json



```

---
## Methods

### Create Experiment

_Definition:_

The `.create()` method can be used to create a new Experiment and save it in one line.

`cript.Experiment.create(get_level=0, update_existing=False, **kwargs)`

_Example:_

Creating a `Experiment` called *"My experiment"*

```python
my_experiment = cript.Experiment.create(name="My experiment")
```

_Returns:_

Created Experiment node of type `cript.data_model.nodes.BaseNode`

---

### Save Experiment

_Definition:_

By saving a node it will be committed to the CRIPT database and saved there
`cript.Experiment.create()`


_Example:_

Creating a Experiment node named _"My experiment"_ and saving it to CRIPT

```python
my_Experiment = cript.Experiment.create(name="My experiment")
my_Experiment.save()
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
### Get Experiment

_Definition:_

Get an Experiment that has already been saved into CRIPT

`cript.Experiment.get(get_level=0, **kwargs)`

<div style="margin-bottom: 2rem"></div>

_Get Experiment Node via UID:_
``` python
my_Experiment = cript.Experiment.get(uid="015fc459-ea9f-4c37-80aa-f51d509095df")
```

_Get Experiment Node via URL:_
``` python
my_Experiment = cript.Experiment.get(url="https://criptapp.org/Experiment/015fc459-ea9f-4c37-80aa-f51d509095df/")
```

_Get Experiment Node via Name:_

``` python
project = cript.Project.get(name="My project")
collection = cript.Collection.get(name="My collection", project=project)
Experiment = cript.Experiment.get(name="My experiment", collection=collection)
```

??? info "Why Collection is needed"
    When getting a Experiment via name, the collection must also be specified since Experiment is nested under collections and the Experiment name is only unique among other Experiments within the collection.

_Returns:_

CRIPT Experiment node of type `cript.data_model.nodes.BaseNode`


_Parameters:_


| Name         | Type   | Description                                             | Default |
|--------------|--------|---------------------------------------------------------|---------|
| `name`       | string | Name of the Experiment to get                           | " "     |
| `collection` | string | collection name that the Experiment is nested inside of | " "     |
| `uid`        | string | UID of the specific Experiment to get                   | " "     |
| `url`        | string | URL of the specific Experiment to get                   | " "     |
| `get_level`  | int    | Level to recursively get nested nodes                   | 0       |
| `**kwargs`   |        | Arguments for the constructor.                          | `{}`    |


---

### Update Experiment

_Definition:_

Update a saved Experiment node with new values

`cript.Experiment.update(get_level=0, **kwargs)`

_Example:_

```python
my_Experiment.update(name="My new Experiment name")
```

_Returns:_

None

_Parameters:_


| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `get_level`       | int     | Level to recursively get nested nodes                          | 0       |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |

---
### Refresh Experiment

_Definition:_

Refresh a node to get the latest saved values from CRIPT

`cript.Experiment.refresh(get_level=0)`

_Example:_

```python
my_Experiment.refresh(name="My new Experiment name")
```

_Returns:_

None

_Parameters:_


| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `get_level`       | int     | Level to recursively get nested nodes                          | 0       |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |


---

### Delete Experiment

_Definition:_

Delete a Experiment node from CRIPT database

`cript.Experiment.delete()`

_Example:_

```python
my_Experiment.delete()
```

_Returns:_

None

_Parameters:_


| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `get_level`       | int     | Level to recursively get nested nodes                          | 0       |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |



---

### Search Experiment

_Definition:_

Search for a Experiment within CRIPT. This method returns a paginator object

`cript.Experiment.search(limit=None, offset=None, get_level=0, **kwargs)`

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