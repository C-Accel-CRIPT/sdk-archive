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


## Equipment Node

```json linenums="1" hl_lines="31-39"
{
    "url": "https://staging.criptapp.org/api/process/2d8c2248-e210-451f-b6f2-a76a690afa3e/",
    "uid": "2d8c2248-e210-451f-b6f2-a76a690afa3e",
    "group": "https://staging.criptapp.org/api/group/ac0415e5-e8d2-485e-ad7d-5029b73dc3c1/",
    "experiment": "https://staging.criptapp.org/api/experiment/57ebd710-a2fd-4b12-b386-b927260f6b76/",
    "name": "Anionic of Styrene - 1",
    "type": "no_op",
    "keywords": [
        "polymerization",
        "living_poly",
        "anionic",
        "solution"
    ],
    "description": "In an argon filled glovebox, a round bottom flask was filled with dried toluene.",
    "prerequisite_processes": [],
    "ingredients": [
        {
            "material": "https://staging.criptapp.org/api/material/e3cd0a06-88a8-455e-bf94-74ed7a5d2c3d/",
            "keyword": "solvent",
            "quantities": [
                {
                    "key": "volume",
                    "value": 1.0000000000000003e-05,
                    "unit": "m**3",
                    "uncertainty": null,
                    "uncertainty_type": null
                }
            ]
        }
    ],
    "equipment": [
        {
            "key": "glass_rbf",
            "description": "Glass round bottom flask",
            "conditions": [],
            "files": [],
            "citations": []
        }
    ],
    "set_id": null,
    "properties": [],
    "conditions": [
        {
            "key": "time_duration",
            "value": 1800.0,
            "unit": "second",
            "uncertainty": null,
            "uncertainty_type": null,
            "material": null,
            "descriptor": null,
            "set_id": null,
            "measurement_id": null,
            "data": null
        },
        {
            "key": "temperature",
            "value": 298.15,
            "unit": "kelvin",
            "uncertainty": null,
            "uncertainty_type": null,
            "material": null,
            "descriptor": null,
            "set_id": null,
            "measurement_id": null,
            "data": null
        }
    ],
    "products": [],
    "waste": [],
    "citations": [],
    "public": false,
    "created_at": "2022-10-28T00:26:08.790724Z",
    "updated_at": "2022-11-28T23:55:44.871454Z"
}

```