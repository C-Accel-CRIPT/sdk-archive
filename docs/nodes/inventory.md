# Inventory

## Definition

The inventory node is a list of material nodes. An example of an inventory can be a
grouping of materials that were extracted from literature and curated into a group for machine
learning, or it can be a subset of chemicals that are used for a certain type of synthesis.


## Sub-Objects
* <a href="../../subobjects/citation" target="_blank">Citation</a>


## Attributes

| Attribute  | Type                            | Example        | Description                               | Required |
|------------|---------------------------------|----------------|-------------------------------------------|----------|
| collection | [Collection](collection.md)     |                | collection associated with the inventory  | True     |
| materials  | list[[Material](./material.md)] | "my_inventory_name" | materials that you like to group together | False    |

## inventory Node

```json

```



## Navigating to Inventory 
`Inventory` can be easily found by vising the <a href="https://criptapp.org/inventory/" target="_blank">inventory</a> link in CRIPT.

## Create
```python

```

## Save
```python

```

## Get
**_Get Project Node via UID:_**
```python

```

**_Get Project Node via URL:_**
```python

```

**_Get Project Node via Name:_**
```python

```

## Delete

```python

```
