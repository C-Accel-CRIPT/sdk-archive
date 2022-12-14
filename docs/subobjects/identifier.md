# Identifier

## Definition

An `Identifier` exists only for the material node, and to identify a single material.

Some examples of identifiers include: _SMILES_, _BigSMILES_, _chemical_id_, etc.

## Identifier Structure

Identifiers are a key-value pair, with ‘key’ specifying the type of identifier and
‘value’ being the content

## List of Material Identifier Keys
<a href="https://criptapp.org/keys/material-identifier-key/" target="_blank">
  material identifier controlled vocabulary
</a>


## Create Identifier

```python
# get polystyrene from CRIPT
polystyrene = cript.Material.get(uid="c27e320e-23f6-47d5-8348-1b842e7b9767")

# create identifier
identifier_bigsmiles = cript.Identifier(
    key="bigsmiles", 
    value="[H]{[>][<]C(C[>])c1ccccc1[<]}C(C)CC"
)
```

## Add Identifier to Material
```python
# attach the identifiers to the material
polystyrene.add_identifier(bigsmiles)
```

## Save Material with Identifier
```python
# save the node to CRIPT database
polystyrene.save()
```

## Remove Identifier
```python
polystyrene.remove_identifier(bigsmiles)
```

<br/>

## Object Example

The identifier sub-object can be seen for the material _polystyrene_

```json  hl_lines="7-31"
{
    "url": "https://criptapp.org/api/material/c27e320e-23f6-47d5-8348-1b842e7b9767/",
    "uid": "c27e320e-23f6-47d5-8348-1b842e7b9767",
    "group": "https://criptapp.org/api/group/30bad7ab-ed35-4659-a56f-9fc384d996f4/",
    "project": "https://criptapp.org/api/project/ab890408-4da1-4311-aa7e-6a4f7897619f/",
    "name": "polystyrene",
    "identifiers": [
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
