# 1. Setup CRIPT
Before proceeding, please make sure you have <a href="https://pypi.org/project/cript/" target="_blank">CRIPT Python SDK</a> installed (`pip install cript`). For full installation instructions, please refer to the <a href="../installation" target="_blank">Installation docs</a>.

---

# 2. Connect to CRIPT
To connect to [CRIPT](https://criptapp.org), you must enter a `host` and an `API Token`. For most users, `host` will be `criptapp.org`

An API token is required to authenticate each user (i.e., make sure they are a valid CRIPT user) before saving any of their data. Your API Token can be found in [security settings](https://criptapp.org/security/) under the profile icon on the top right of `criptapp.org`. For further explanation, please refer to [how to get an API Token](api_token.md)

!!! note
    The word `Token` in front of the random characters is part of the token as well. 

It is *highly* recommended that you store your API token in a safe location and read it into your code, rather than have it hard-coded. One way to do this is to store
it in an environmental variable (e.g., `CRIPT_API_KEY`) and then read it in via the `os` module:
 
``` python
import cript
import os

host = "criptapp.org"
token = os.environ.get("CRIPT_API_KEY")
cript.API(host, token)
```

You should see the following output:
``` bash
Connected to https://criptapp.org/api
```

??? "Private Instance of CRIPT"
    If any user wants to connect to their own private instance of CRIPT, they can easily do that by just changing the `host` to their local host address (e.g., `http://127.0.0.1:8000/`) and setting `tls=False`:

    ```python 
    import cript
    import os
    
    host = "http://127.0.0.1:8000/"
    token = os.environ.get("CRIPT_API_KEY")
    cript.API(host, token, tls=False)
    ```

---

# 3. Create a node

??? "What is a node?"
    A *node* is simply a CRIPT object (e.g., `Project`, `Experiment`)  in the graph-based data model. 

All data uploaded to CRIPT must be associated with a <a href="../../nodes/project" target="_blank">`Project`</a> node. A <a href="../../nodes/project" target="_blank">`Project`</a> can be thought of as a folder that contains <a href="../../nodes/collection" target="_blank">`Collections`</a>. To create a <a href="../../nodes/project" target="_blank">`Project`</a> and upload it to CRIPT :

```python
my_proj = cript.Project.create(name="My first project") # creates and uploads Project to CRIPT
```

??? "Notes"
    * `Project` names are globally unique, meaning no two `Projects` in the entire CRIPT database can have the same name.
    * Notice the use of `create()` here, which both *instantiates* the Python object and *uploads* it to the database in one go.

Let's print the project to get a better view:

```python
print(my_proj)
```

This should print something similar to the following:
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

# Create a Collection node

A [`Collection`](../nodes/collection.md) can be thought of as a folder filled with experiments. Just like we did for a `Project` node, we use `create()` to create and upload a new `Collection`: 

``` python
coll = cript.Collection.create(project=proj, name="<Your Collection Name>")
```

---

# Create an Experiment node

``` python
expt = cript.Experiment.create(
    collection=coll,
    name="Anionic Polymerization of Styrene with SecBuLi"
)
```

# Get Material nodes

For this tutorial, we will get an existing Inventory node from the database.  
This contains all of the Material nodes we will be using.

``` python
uid = "134f2658-6245-42d8-a47e-6424aa3472b4"
inv = cript.Inventory.get(uid=uid, get_level=1)
```

!!! note
    We are setting `get_level` to `1` so that the Material nodes are auto-generated. This parameter defaults to `0`, but can be set to any integer.

``` python
print( type(inv.materials[0]) )
```

Something similar to the following should be printed:
``` bash
<class 'cript.data_model.nodes.material.Material'>
```
# Create a Process node

``` python
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
```

# Add Ingredient nodes to the Process node

First, let's grab the Material nodes we need from the Inventory node.

``` python
solution = inv['SecBuLi solution 1.4M cHex']
toluene = inv['toluene']
styrene = inv['styrene']
butanol = inv['1-butanol']
methanol = inv['methanol']
```

Next, we'll define Quantity nodes indicating the amount of each Ingredient.

``` python
initiator_qty = cript.Quantity(key="volume", value=0.017, unit="ml")
solvent_qty = cript.Quantity(key="volume", value=10, unit="ml")
monomer_qty = cript.Quantity(key="mass", value=0.455, unit="g")
quench_qty = cript.Quantity(key="volume", value=5, unit="ml")
workup_qty = cript.Quantity(key="volume", value=100, unit="ml")
```

Next, we'll create Ingredient nodes for each.

``` python
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

``` python
prcs.add_ingredient(initiator)
prcs.add_ingredient(solvent)
prcs.add_ingredient(monomer)
prcs.add_ingredient(quench)
prcs.add_ingredient(workup)
```

# Add Condition nodes to the Process node

``` python
temp = cript.Condition(key="temperature", value=25, unit="celsius")
time = cript.Condition(key="time_duration", value=60, unit="min")
prcs.add_condition(temp)
prcs.add_condition(time)
```

# Add a Property node to the Process node

``` python
yield_mass = cript.Property(
    key="yield_mass",
    value=0.47,
    unit="g",
    method="scale"
)
prcs.add_property(yield_mass)
```

# Create a Material node (process product)

First, we'll instantiate the node.

``` python
polystyrene = cript.Material(project=proj.uid, name="polystyrene")
```

Next, we'll add some Identifier nodes.

``` python
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

``` python
phase = cript.Property(key="phase", value="solid")
color = cript.Property(key="color", value="white")

polystyrene.add_property(phase)
polystyrene.add_property(color)
```

Now we can save the Material and add it to the Process node as a product.

``` python
polystyrene.save()
prcs.add_product(polystyrene)
```

Last, we can save the Process node.

``` python
prcs.save()
```

# Create a File node and upload a file

First, we'll instantiate a File node and associate with the Data node created above.

``` python
path = "path/to/local/file"
f = cript.File(project=proj, source=path)
```

!!! note
The `source` field should point to a file on your local filesystem.
!!! info
Depending on the file size, there could be a delay while the checksum is generated.

Next, we'll upload the local file by saving the File node. Follow all prompts that appear.

``` python
f.save()
```

You will be prompted to click a link to obtain an authorization code. Copy and paste the code obtained from this link into the terminal to save the file.

# Create a Data node

``` python
sec = cript.Data(
    experiment=expt,
    name="Crude SEC of polystyrene",
    type="sec_trace",
)
```

.. then add the uploaded File to it:

``` python
sec.add_file(f)
sec.save()
```

# Associate a Data node with a Property node

First, we'll create one more Property node for polystyrene.

``` python
mw_n = cript.Property(key="mw_n", value=5200, unit="g/mol")
```

Next, we'll add the Data node to the new Property node.

``` python
mw_n.data = sec
```

Last, we'll add the new Property node to polystyrene then save it.

``` python
polystyrene.add_property(mw_n)
polystyrene.save()
```

# Conclusion

You made it! We hope this tutorial has been helpful.

Please let us know how you think it could be improved.
