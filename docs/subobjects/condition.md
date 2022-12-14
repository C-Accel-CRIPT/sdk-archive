# Condition

## Definition
`Condition` is the conditions under which the experiment was conducted.

Some examples include `temperature`, `mixing_rate`, `stirring`, `time_duration`

Please visit <a href="https://criptapp.org/keys/condition-key/" target="_blank">
  condition controlled vocabulary</a> for a full list of conditions    

## Can be added to
* <a href="../property" target="_blank">Property</a>
* <a href="../../nodes/process" target="_blank">Process</a>
* <a href="../../nodes/computation" target="_blank">Computation</a>
* <a href="../../nodes/computational_process" target="_blank">Computational Process</a>


## Navigating to Condition 

## Create
```python
temp = cript.Condition(key="temperature", value=25, unit="celsius")
```

## Add Condition to [Node](#can-be-added-to)
```python
my_process.add_condition(temp)
```

## Save
```python
my_process.save()
```

## Remove Condition from [Node](#can-be-added-to)
```python
my_process.remove_condition(temp)
```

## Condition Node
```json linenums="1" hl_lines="42-67"
{
    "url": "https://criptapp.org/api/process/2d8c2248-e210-451f-b6f2-a76a690afa3e/",
    "uid": "2d8c2248-e210-451f-b6f2-a76a690afa3e",
    "group": "https://criptapp.org/api/group/ac0415e5-e8d2-485e-ad7d-5029b73dc3c1/",
    "experiment": "https://criptapp.org/api/experiment/57ebd710-a2fd-4b12-b386-b927260f6b76/",
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
            "material": "https://criptapp.org/api/material/e3cd0a06-88a8-455e-bf94-74ed7a5d2c3d/",
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
