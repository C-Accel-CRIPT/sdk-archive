# Collection

## Definition

A collection node can be thought as a folder/bucket that can hold either an 
<a href="../experiment" target="_blank">Experiment</a> or 
<a href="../inventory" target="_blank">Inventory</a> node.

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

### Create
`.create(get_level=0, update_existing=False, **kwargs)`

#### Definition
This method can be used when creating a new `Collection` node

#### Example

Creating a `Collection` called *"My Collection"*

```python
my_collection = cript.Collection.create(name="My collection")
```

---

### Save

#### Definition
By saving a node it will be committed to the CRIPT database and saved there

#### Example
```python
my_collection = cript.Collection.create(name="My collection")
my_collection.save()
```


---
### Get

#### Definition
Get a Collection that has already been saved into CRIPT

#### Example

``` python
my_collection = cript.Collection.get(name="My collection")
```

---

### Update

#### Definition
Update a saved Collection node 

#### Example
```python
my_collection.update(name="My new collection name")
```

---
### Refresh

#### Definition
Overwrite a node's attributes with the latest values from the database

#### Example
```python

```


---

### Delete

#### Definition
Delete a Collection node from CRIPT database 

#### Example
```python
my_collection.delete()
```

---

### Search

#### Definition
Search for a Collection within CRIPT

#### Example

```python

```


----





### Other stuff

::: cript.data_model.nodes.base_node.BaseNode
    options:
        members:
            - save
            - delete
            - refresh
            - update
            - create
            - get
            - search