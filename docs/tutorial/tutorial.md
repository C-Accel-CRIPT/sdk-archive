# Tutorial

## Setup CRIPT
Before proceeding, please make sure you have [CRIPT Python SDK](https://pypi.org/project/cript/) installed (`pip install cript`).

For full installation instructions, please refer to the [installation docs](cript_installation.md).

---

## :octicons-terminal-16: Using CRIPT on the command line

### Launch python interpreter

Open a terminal on your computer (e.g., Terminal on MacOS, Linux console on Unix-like OS, or Powershell on Windows). This tutorial is done using Windows Powershell.
 
Start the python interpreter by typing `python` in the terminal:

:fontawesome-regular-keyboard: My Input:
```bash
python
```

:octicons-terminal-16: Terminal Output:
```bash
Python 3.10.5 (tags/v3.10.5:f377153, Jun  6 2022, 16:14:13) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

---

### Connect to CRIPT
To connect to [CRIPT](https://criptapp.org), you must enter a `host` and an `API Token`.

#### Host

The `host` indicates the CRIPT instance that you want to upload your data to, whether that is CRIPT or a private instance. 

!!! note 
    For most users, `host` will be `criptapp.org`

#### API Token

The token is needed because we need to authenticate the user (i.e., make sure they are a valid CRIPT user) before saving any of their data.

Your API Token can be found in [security settings](https://criptapp.org/security/) under the profile icon on the top right of `criptapp.org`. For further explanation, please refer to [how to get an API Token](acquiring_api_token.md)

!!! note
    The word `Token` in front of the random characters is part of the token as well. 

It is *highly* recommended that you store your API token in a safe location and read it into your code, rather than have it hard-coded. One way to do this is to store
it in an environmental variable (e.g., `CRIPT_API_KEY`) and then read it in via the `os` module.
 
:fontawesome-regular-keyboard: My Input:
```python
import cript
import os

host = "criptapp.org"
token = os.environ.get("CRIPT_API_KEY")
cript.API(host, token)
```
:octicons-terminal-16: Terminal Output:
```bash
Connected to https://criptapp.org/api
```

??? "Private Instance of CRIPT"
    If any user wants to connect to their own private instance of CRIPT, they can easily do that by just changing both the `Host` and `API Token` to their own `Host` and `API Token` continue everything else as normal.

---
## What is a node?
* A *node* is simply a CRIPT object (e.g., `Project`, `Experiment`)  in the graph-based data model. Details on how to create, modify, and save different type of nodes
are given in the following sections.

### How to tell if a node has been created and saved in the database?
* When a node is saved, a URL is created for it - you can check if a particular node exists in the database by typing ``. 

---

## Create a [Project](../nodes/project.md) node

A [`Project`](../nodes/project.md) can be thought of as a folder that contains [`Collections`](../nodes/collection.md). Each [`Collections`](../nodes/collection.md) must belong inside of a [`Project`](../nodes/project.md).

!!! warning "Project Name"
    **Project names are globally unique**, meaning no 2 projects on the entire system can have the same name

### Example
 _continuing the example from above..._

:fontawesome-regular-keyboard: My Input:
```py
Connected to https://criptapp.org/api

proj = cript.Project.create(name="<Your Project Name>")
proj.save()
```

:octicons-terminal-16: Terminal Output:

<small>
    The terminal gives no output
</small>

```bash

```

!!! Info
    Lets print the project to get a better view

:fontawesome-regular-keyboard: My Input:
```py
print(proj)
```

:octicons-terminal-16: Terminal Output:
```bash
{
    "url": "https://criptapp.org/api/project/910445b2-88ca-43ac-88cf-f6424e85b1ba/",
    "uid": "910445b2-88ca-43ac-88cf-f6424e85b1ba",
    "public": false,
    "created_at": "2022-11-23T00:47:40.011485Z",
    "updated_at": "2022-11-23T00:47:40.011507Z",
    "name": "Navid's Project SDK",
    "notes": null,
    "group": "https://criptapp.org/api/group/68ed4c57-d1ca-4708-89b2-cb1c1609ace2/",
    "collections": "https://criptapp.org/api/project/910445b2-88ca-43ac-88cf-f6424e85b1ba/collections/",
    "materials": "https://criptapp.org/api/project/910445b2-88ca-43ac-88cf-f6424e85b1ba/materials/",
    "files": "https://criptapp.org/api/project/910445b2-88ca-43ac-88cf-f6424e85b1ba/files/"
}
```

---

## Create a Collection node

A [Collection](../nodes/collection.md) can be thought of as a folder filled with experiments

!!! note
    Notice the use of `create()` here, which instantiates and saves the object in one go.

:fontawesome-regular-keyboard: My Input:
```py
coll = cript.Collection.create(project=proj, name="<Your Collection Name>")
```

:octicons-terminal-16: Terminal Output:

<small>
    The terminal gives no output
</small>

```bash

```


---

## Create an Experiment node

```py
expt = cript.Experiment.create(
    collection=coll,
    name="Anionic Polymerization of Styrene with SecBuLi"
)
expt.save()
```

## Get Material nodes

For this tutorial, we will get an existing Inventory node from the database.  
This contains all of the Material nodes we will be using.

```py
uid = "134f2658-6245-42d8-a47e-6424aa3472b4"
inv = cript.Inventory.get(uid=uid, get_level=1)
```

!!! note
We are setting `get_level` to `1` so that the Material nodes are auto-generated. This parameter defaults to `0`, but can be set to any integer.

Notice that the Material node objects have been auto-generated.

```py
type(inv.materials[0])
# <class 'cript.data_model.nodes.material.Material'>
```

## Create a Process node

```py
prcs = cript.Process.create(
    experiment=expt,
    name="Anionic of Styrene",
    type = "multistep",
    description = "In an argon filled glovebox, a round bottom flask was filled with 216 ml of dried toluene. The "
                  "solution of secBuLi (3 ml, 3.9 mmol) was added next, followed by styrene (22.3 g, 176 mmol) to "
                  "initiate the polymerization. The reaction mixture immediately turned orange. After 30 min, "
                  "the reaction was quenched with the addition of 3 ml of methanol. The polymer was isolated by "
                  "precipitation in methanol 3 times and dried under vacuum."
)
prcs.save()
```

## Add Ingredient nodes to the Process node

First, let's grab the Material nodes we need from the Inventory node.

```py
solution = inv['SecBuLi solution 1.4M cHex']
toluene = inv['toluene']
styrene = inv['styrene']
butanol = inv['1-butanol']
methanol = inv['methanol']
```

Next, we'll define Quantity nodes indicating the amount of each Ingredient.

```py
initiator_qty = cript.Quantity(key="volume", value=0.017, unit="ml")
solvent_qty = cript.Quantity(key="volume", value=10, unit="ml")
monomer_qty = cript.Quantity(key="mass", value=0.455, unit="g")
quench_qty = cript.Quantity(key="volume", value=5, unit="ml")
workup_qty = cript.Quantity(key="volume", value=100, unit="ml")
```

Next, we'll create Ingredient nodes for each.

```py
initiator = cript.Ingredient(
    keyword="initiator",
    material=solution,
    quantities=[initiator_qty]
)
solvent = cript.Ingredient(
    keyword="solvent",
    material=toluene,
    quantities=[solvent_qty]
)
monomer = cript.Ingredient(
    keyword="monomer",
    material=styrene,
    quantities=[monomer_qty]
)
quench = cript.Ingredient(
    keyword="quench",
    material=butanol,
    quantities=[quench_qty]
)
workup = cript.Ingredient(
    keyword="workup",
    material=methanol,
    quantities=[workup_qty]
)
```

Last, we'll add the Ingredient nodes to the Process node.

```py
prcs.add_ingredient(initiator)
prcs.add_ingredient(solvent)
prcs.add_ingredient(monomer)
prcs.add_ingredient(quench)
prcs.add_ingredient(workup)
```

## Add Condition nodes to the Process node

```py
temp = cript.Condition(key="temperature", value=25, unit="celsius")
time = cript.Condition(key="time_duration", value=60, unit="min")
prcs.add_condition(temp)
prcs.add_condition(time)
```

## Add a Property node to the Process node

```py
yield_mass = cript.Property(
    key="yield_mass",
    value=0.47,
    unit="g",
    method="scale"
)
prcs.add_property(yield_mass)
```

## Create a Material node (process product)

First, we'll instantiate the node.

```py
polystyrene = cript.Material(project=proj, name="polystyrene")
```

Next, we'll add some Identifier nodes.

```py
names = cript.Identifier(
    key="names",
    value=["poly(styrene)", "poly(vinylbenzene)"]
)
bigsmiles = cript.Identifier(
    key="bigsmiles",
    value="[H]{[>][<]C(C[>])c1ccccc1[<]}C(C)CC"
)
chem_repeat = cript.Identifier(key="chem_repeat", value="C8H8")

polystyrene.add_identifier(names)
polystyrene.add_identifier(chem_repeat)
polystyrene.add_identifier(bigsmiles)
```

Next, we'll add some Property nodes.

```py
phase = cript.Property(key="phase", value="solid")
color = cript.Property(key="color", value="white")

polystyrene.add_property(phase)
polystyrene.add_property(color)
```

Now we can save the Material and add it to the Process node as a product.

```py
polystyrene.save()
prcs.add_product(polystyrene)
```

Last, we can save the Process node.

```py
prcs.save()
```

## Create a File node and upload a file

First, we'll instantiate a File node and associate with the Data node created above.

```py
path = "path/to/local/file"
f = cript.File(project=proj, source=path)
```

!!! note
The `source` field should point to a file on your local filesystem.
!!! info
Depending on the file size, there could be a delay while the checksum is generated.

Next, we'll upload the local file by saving the File node. Follow all prompts that appear.

```py
api.save(f)
```

## Create a Data node

```py
sec = cript.Data(
    experiment=expt,
    name="Crude SEC of polystyrene",
    type="sec_trace",
)
```

.. then add the uploaded File to it:

```python
sec.add_file(f)
sec.save()
```

## Associate a Data node with a Property node

First, we'll create one more Property node for polystyrene.

```py
mw_n = cript.Property(key="mw_n", value=5200, unit="g/mol")
```

Next, we'll add the Data node to the new Property node.

```py
mw_n.data = sec
```

Last, we'll add the new Property node to polystyrene then save it.

```py
polystyrene.add_property(mw_n)
polystyrene.save()
```

## Conclusion

You made it! We hope this tutorial has been helpful.

Please let us know how you think it could be improved.
