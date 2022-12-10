# Property

## Definition

A `Property` sub-object can exists for the following nodes:

* <a href="../nodes/material" target="_blank">Material</a>
* <a href="../nodes/process" target="_blank">Process</a>
* <a href="../nodes/computational_process" target="_blank">Computational_Process</a>

Some examples of Propertys include: _SMILES_, _BigSMILES_, _chemical_id_, etc.

## Property Structure

Propertys are a key-value pair, with ‘key’ specifying the type of Property and
‘value’ being the content

## List of Property Keys
* <a href="https://criptapp.org/keys/material-property-key/" target="_blank">
    Material Property Keys
</a>

* <a href="https://criptapp.org/keys/process-property-key/" target="_blank">
    Process Property Key
</a>

* <a href="https://criptapp.org/keys/computational-process-property-key/" target="_blank">
    Computational Property Keys
</a>


## Code Example

### Adding Property to Material
```python

```

### Adding Property to Process
```python

```

### Adding Property to Computational Process
```python

```


<br/>

??? tip "JSON Example"

    The Property sub-object can be seen for the material _polystyrene_

    ```json linenums="1"  hl_lines="35-131"
    {
        "url": "https://criptapp.org/api/material/c27e320e-23f6-47d5-8348-1b842e7b9767/",
        "uid": "c27e320e-23f6-47d5-8348-1b842e7b9767",
        "group": "https://criptapp.org/api/group/30bad7ab-ed35-4659-a56f-9fc384d996f4/",
        "project": "https://criptapp.org/api/project/ab890408-4da1-4311-aa7e-6a4f7897619f/",
        "name": "polystyrene",
        "Propertys": [
            {
                "key": "preferred_name",
                "value": "polystyrene"
            },
            {
                "key": "names",
                "value": [
                    "poly(styrene)",
                    "poly(vinylbenzene)"
                ]
            },
            {
                "key": "chem_repeat",
                "value": "C8H8"
            },
            {
                "key": "chemical_id",
                "value": "100-42-5"
            },
            {
                "key": "bigsmiles",
                "value": "*{[<][<]CC([>])c1ccccc1[>]}*"
            }
        ],
        "components": [],
        "keywords": [],
        "notes": "",
        "properties": [
            {
                "key": "color",
                "value": "white",
                "unit": null,
                "uncertainty": null,
                "uncertainty_type": null,
                "type": null,
                "method": null,
                "components": [],
                "components_relative": [],
                "structure": null,
                "sample_preparation": null,
                "set_id": null,
                "conditions": [],
                "data": null,
                "computations": [],
                "citations": [],
                "notes": null
            },
            {
                "key": "mw_d",
                "value": 1.03,
                "unit": null,
                "uncertainty": 0.02,
                "uncertainty_type": null,
                "type": null,
                "method": "sec",
                "components": [],
                "components_relative": [],
                "structure": null,
                "sample_preparation": null,
                "set_id": null,
                "conditions": [],
                "data": "https://criptapp.org/api/data/6f66cba6-f6c3-421f-9384-07105cb540fa/",
                "computations": [],
                "citations": [],
                "notes": null
            },
            {
                "key": "phase",
                "value": "solid",
                "unit": null,
                "uncertainty": null,
                "uncertainty_type": null,
                "type": null,
                "method": null,
                "components": [],
                "components_relative": [],
                "structure": null,
                "sample_preparation": null,
                "set_id": null,
                "conditions": [],
                "data": null,
                "computations": [],
                "citations": [],
                "notes": null
            },
            {
                "key": "mw_n",
                "value": 5.2,
                "unit": "kilogram / mole",
                "uncertainty": 0.1,
                "uncertainty_type": null,
                "type": null,
                "method": "sec",
                "components": [],
                "components_relative": [],
                "structure": null,
                "sample_preparation": null,
                "set_id": null,
                "conditions": [],
                "data": "https://criptapp.org/api/data/6f66cba6-f6c3-421f-9384-07105cb540fa/",
                "computations": [],
                "citations": [],
                "notes": null
            },
            {
                "key": "mw_n",
                "value": 4.8,
                "unit": "kilogram / mole",
                "uncertainty": 0.4,
                "uncertainty_type": null,
                "type": null,
                "method": "nmr",
                "components": [],
                "components_relative": [],
                "structure": null,
                "sample_preparation": null,
                "set_id": null,
                "conditions": [],
                "data": "https://criptapp.org/api/data/293631b7-dad3-43ec-96b7-86f233f444c7/",
                "computations": [],
                "citations": [],
                "notes": null
            }
        ],
        "process": "https://criptapp.org/api/process/9f468e7a-7eb2-4796-b438-29fccfea4b4f/",
        "computational_forcefield": null,
        "public": true,
        "created_at": "2022-09-08T17:36:08.154333Z",
        "updated_at": "2022-10-06T14:17:21.817950Z"
    }
    ```



