# Quantity

## Definition
The amount of material involved in a process.

They are only used for the [Ingredients](./ingredient.md) sub-object. 


## Super-Object
* <a href="../ingredient" target="_blank">Ingredients</a>


## Sub-Objects
* None


## Attributes

| Attribute        | Type | Example | Description                                                                       | Required |
|------------------|------|---------|-----------------------------------------------------------------------------------|----------|
| key              | str  | "mass"  | Pick from [type of quantity](https://criptapp.org/keys/quantity-key/)             | True     |
| value            | Any  | 1.23    | amount of material                                                                | True     |
| unit             | str  | "grams" | unit for quantity                                                                 | True     |
| uncertainty      | Any  | 0.1     | uncertainty of value (margin of error)                                            | True     |
| uncertainty_type | any  | std     |  Pick [ Uncertainty type Vocabulary](https://criptapp.org/keys/uncertainty-type/) | True     |                                                                                           | True     |


??? tip "Quantity"
    The proper: 

    * value type (number)
    * range ([0, 1.79e+308])
    * SI Unit (kg)
    * Preferred Unit (ml)
    * Description
    
    can be found in the [CRIPT Quantity vocabulary](https://criptapp.org/keys/quantity-key/)

## Navigating to quantity 

## Create
```python
my_quantity = cript.Quantity(key="volume", value=0.017, unit="ml")
```

## Add Quantity to Ingredient
```python
my_ingredient = cript.Ingredient(
    keyword="initiator", 
    material=solution, 
    quantities=[my_quantity]    # add quantity to ingredient
)

process.add_ingredient(my_quantity) # add ingredient to process
```

## Save
```python
process.save()
```

## Delete
```python
process.delete()
```

## Quantity Node

```json linenums="1" hl_lines="20-28"
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
