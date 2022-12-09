# Project

## Definition

A `Project` is the highest level node that is **Not** nested inside of any other node.
A `Project` can be thought of as a folder that can contain 
<a href="../collection" target="_blank">`Collections`</a>, 
<a href="../material" target="_blank">`Materials`</a>, and
<a href="../file" target="_blank">`Files`</a>.

## Navigating to Projects
`Projects` can be easily found on <a href="https://criptapp.org" target="_blank">CRIPT</a> home screen in the 
<a href="https://criptapp.org/project/" target="_blank">Projects link</a>

Each [`Collection`](collection.md) belongs inside of a single `Project`

<br/>

!!! warning "Project Name"
    _Project names Must be globally unique_, meaning no 2 projects on the entire system can have the same name

---

## Project Attribute
`print(cript.Project.get(name="TEST project"))`

``` json
{
    "url": "https://criptapp.org/api/project/8fe0e506-0e8e-424e-b4e2-1687909f6ea2/",
    "uid": "8fe0e506-0e8e-424e-b4e2-1687909f6ea2",
    "public": false,
    "created_at": "2022-09-13T20:14:02.729710Z",
    "updated_at": "2022-09-13T20:14:02.729726Z",
    "name": "TEST project",
    "collections": "https://criptapp.org/api/project/8fe0e506-0e8e-424e-b4e2-1687909f6ea2/collections/",
    "materials": "https://criptapp.org/api/project/8fe0e506-0e8e-424e-b4e2-1687909f6ea2/materials/",
    "files": "https://criptapp.org/api/project/8fe0e506-0e8e-424e-b4e2-1687909f6ea2/files/",
    "notes": "",
    "group": "https://criptapp.org/api/group/ac0415e5-e8d2-485e-ad7d-5029b73dc3c1/"
}
```

---
## Methods

### Create Project

_Definition:_

Creates a new Project node and saves it in one line

`cript.Project.create(get_level=0, update_existing=False, **kwargs)`

_Example:_
``` python
my_project = cript.Project.create(name="My project")
```

_Returns:_

Created node of type `cript.data_model.nodes.BaseNode`

_Parameters:_

| Name   | Type   | Description                  | Default |
|--------|--------|------------------------------|---------|
| `name` | string | name of the new Project node | " "     |

---

### Save Project

_Definition:_

Save a Project node to CRIPT

_Example:_
``` python
cript.Project.save()
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

### Get Project

_Definition:_


_Get Project Node via UID:_
``` python
my_project = cript.Project.get(uid="015fc459-ea9f-4c37-80aa-f51d509095df")
```

_Get Project Node via URL:_
``` python
my_project = cript.Project.get(url="https://criptapp.org/project/015fc459-ea9f-4c37-80aa-f51d509095df/")
```

_Get Project Node via Name:_
``` python
my_project = cript.Project.get(name="My project")
```

_Returns:_

CRIPT Project node of type `cript.data_model.nodes.BaseNode`

_Parameters:_

| Name        | Type   | Description                           | Default |
|-------------|--------|---------------------------------------|---------|
| `name`      | string | name of the project to get            | " "     |
| `uid`       | string | UID of the specific project to get    | " "     |
| `url`       | string | URL of the specific project to get    | " "     |
| `get_level` | int    | Level to recursively get nested nodes | 0       |
| `**kwargs`  |        | Arguments for the constructor.        | `{}`    |

---

### Refresh Project

_Definition:_

Refresh a node to get the latest saved values from CRIPT
`cript.Project.refresh(get_level=0)`

_Example:_
```python
my_project.refresh(name="My new project name")
```

_Returns:_

None

_Parameters:_

| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `get_level`       | int     | Level to recursively get nested nodes                          | 0       |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |

---

### Update Project

_Definition:_

Update a saved Project node with new values

`cript.Project.update(get_level=0, **kwargs)`

_Example:_
``` python
my_project.update(name="My new project name")
```

_Returns:_

None

_Parameters:_

| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `get_level`       | int     | Level to recursively get nested nodes                          | 0       |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |

---

### Delete Project

_Definition:_

Delete a Project node from CRIPT database

`cript.Project.delete()`

_Example:_
``` python
my_project.delete()
```

_Returns:_

None

_Parameters:_

| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `get_level`       | int     | Level to recursively get nested nodes                          | 0       |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |

---

### Search Project

_Definition:_

Search for a Project within CRIPT. This method returns a paginator object

`cript.Project.search(limit=None, offset=None, get_level=0, **kwargs)`

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
