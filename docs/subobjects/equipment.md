# Equipment

## Definition
Equipment are physical instruments, tools, glassware, etc. used in a process. 

??? info
    Settings, or environmental variables controlled by the equipment can be specified with the [conditions](./condition.md)
    attribute. 

    Equipment specification, configuration, and calibration files can be attached to the
    equipment sub-object with the use of a [File](../supporting_nodes/file.md)


## Super-Object
* <a href="../../nodes/process" target="_blank">Process</a>


## Sub-Objects
* <a href="../../subobjects/condition" target="_blank">Condition</a>
* <a href="../../subobjects/citation" target="_blank">Citation</a>


## Attributes

| Attribute   | Type                                         | Example                                         | Description                                                                    | Required |
|-------------|----------------------------------------------|-------------------------------------------------|--------------------------------------------------------------------------------|----------|
| key         | str                                          | "hot plate"                                     | Pick from [CRIPT Equipments](https://criptapp.org/keys/equipment-key/)         | True     |
| description | str                                          | "Hot plate with silicon oil bath with stir bar" | details about the equipment                                                    | False    |
| conditions  | list[[conditions](./condition.md)]           | temperature                                     | conditions under which the property was measured                               | False    |
| files       | list[[files](../supporting_nodes/file.md)]   |                                                 | list of file nodes to link to calibration or equipment specification documents | False    |
| citations   | list[[citations](../subobjects/citation.md)] |                                                 | reference to a book, paper, or scholarly work                                  | False    |

## Equipment Node

```json

```

## Navigating to Equipment 

## Create
```python
equipment = cript.Equipment(key="hot plate", description="Hot plate with silicon oil bath with stir bar")
```

## Add Equipment to Process
```python
process.equipment.append(equipment)
```

## Save
```python
process.save()
```

## Delete
```python
equipment.delete()
```