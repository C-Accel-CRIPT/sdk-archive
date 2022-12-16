# Inventory

## Definition

The inventory node is a list of material nodes. An example of an inventory can be a
grouping of materials that were extracted from literature and curated into a group for machine
learning, or it can be a subset of chemicals that are used for a certain type of synthesis.


## Nodes that can be added to Inventory
* <a href="../../subobjects/citation" target="_blank">Citation</a>


## Attributes

| Attribute  | Type                            | Example        | Description                               | Required |
|------------|---------------------------------|----------------|-------------------------------------------|----------|
| collection | [Collection](collection.md)     |                | collection associated with the inventory  | True     |
| materials  | list[[Material](./material.md)] | "my_inventory_name" | materials that you like to group together | False    |



## Navigating to Inventory 
`Inventory` can be easily found by vising the <a href="https://criptapp.org/inventory/" target="_blank">inventory</a> link in CRIPT.

## Create
```python
my_inventory = cript.Inventory()
```

## Save
```python
my_inventory.save()
```

## Get
**_Get Inventory Node via UID:_**
```python
my_inventory = cript.Inventory.get(uid="134f2658-6245-42d8-a47e-6424aa3472b4")
```

**_Get Inventory Node via URL:_**
```python
my_inventory = cript.Inventory.get(url="https://criptapp.org/inventory/134f2658-6245-42d8-a47e-6424aa3472b4/")
```

**_Get Inventory Node via Name:_**
```python
my_inventory = cript.Inventory.get(name="")
```

## Delete
```python
my_inventory.delete()
```


## Inventory Node
```json
{
    "url": "https://criptapp.org/api/inventory/134f2658-6245-42d8-a47e-6424aa3472b4/",
    "uid": "134f2658-6245-42d8-a47e-6424aa3472b4",
    "group": "https://criptapp.org/api/group/3c612a84-1bf7-483a-942a-7ab56f71f83c/",
    "name": "Tutorial Materials",
    "materials": [
        "https://criptapp.org/api/material/5ad3a4bf-19ea-4132-992b-2f03f00af4d0/",
        "https://criptapp.org/api/material/e4e04474-e5b3-452b-ad97-3fa91a01f8da/",
        "https://criptapp.org/api/material/bb2f7c62-9cd9-454d-97a1-4a8d176f0b81/",
        "https://criptapp.org/api/material/b45d4630-ccf7-41ed-ba6f-04e457f95dee/",
        "https://criptapp.org/api/material/463815a3-e86f-4199-bc53-4160ee69a29d/"
    ],
    "collection": "https://criptapp.org/api/collection/b2c3f5d1-ae88-4e87-9bd1-0302db423466/",
    "notes": null,
    "public": true,
    "created_at": "2022-04-28T03:15:50.619236Z",
    "updated_at": "2022-04-28T03:21:24.455512Z"
}
```
