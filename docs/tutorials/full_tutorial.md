# Install CRIPT
Before proceeding, please make sure you have the <a href="https://pypi.org/project/cript/" target="_blank">CRIPT Python SDK</a> installed (`pip install cript`). For full installation instructions, please refer to the <a href="../installation" target="_blank">Installation docs</a>.

# Connect to CRIPT
To connect to [CRIPT](https://criptapp.org), you must enter a `host` and an `API Token`. For most users, `host` will be `criptapp.org`.

An API token tells CRIPT who you are and ensures that you have permission to view and upload certain types of data. Your API Token can be found in the CRIPT application <a href="https://criptapp.org/security/" target="_blank">security settings</a>. For additional details, please refer to [how to get an API Token](api_token.md)

!!! note
    The word `Token` in front of the random token characters is part of the token as well. Always copy the entire token text.

It is *highly* recommended that you store your API token in a safe location and read it into your code, rather than have it hard-coded. One way to do this is to store
it in an environmental variable (e.g., `CRIPT_API_KEY`) and then read it in via the `os` module. See [API Token documentation](api_token.md) to learn more:
 
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
    If you're connecting to your own private instance of CRIPT, just set the `host` to your local host address (e.g., `http://127.0.0.1:8000/`), and set `tls=False`:

    ```python 
    import cript
    import os
    
    host = "http://127.0.0.1:8000/"
    token = os.environ.get("CRIPT_API_KEY")
    cript.API(host, token, tls=False)
    ```

!!! info
    Use the `tls` parameter to specify whether to use TLS encryption (`https`) for the API connection. This parameter is set to `True` by default. In some cases, such as when running the CRIPT server locally, you may want to disable https and instead run the server on `http` by setting `tls=False`.


# Create a (CRIPT object) node

??? "What is a node?"
    A *node* is simply a CRIPT object (e.g., `Project`, `Experiment`, `Material`) in the graph-based CRIPT data model. 

All data uploaded to CRIPT must be associated with a <a href="../../nodes/project" target="_blank">`Project`</a> node. A <a href="../../nodes/project" target="_blank">`Project`</a> can be thought of as a folder that contains <a href="../../nodes/collection" target="_blank">`Collections`</a> and <a href="../../nodes/material" target="_blank">`Materials`</a>. To create a <a href="../../nodes/project" target="_blank">`Project`</a> and upload it to CRIPT, use the `<node>.create()` method, where `<node>` can be any of the <a href="../../nodes/all" target="_blank">primary CRIPT node types</a>:

```python
 # create a new project in the CRIPT database
my_proj = cript.Project.create(name="My first project")
```

!!! info "Notes"
    * `Project` names are globally unique, meaning no two `Projects` in the entire CRIPT database can have the same name.
    * Notice the use of `create()` here, which both *instantiates* the Python object and *uploads* it to the database in one command.

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
    "name": "My first project",
    "notes": null,
    "group": "https://criptapp.org/api/group/68ed4c57-d1ca-4708-89b2-cb1c1609ace2/",
    "collections": "https://criptapp.org/api/project/910445b2-88ca-43ac-88cf-f6424e85b1ba/collections/",
    "materials": "https://criptapp.org/api/project/910445b2-88ca-43ac-88cf-f6424e85b1ba/materials/",
    "files": "https://criptapp.org/api/project/910445b2-88ca-43ac-88cf-f6424e85b1ba/files/"
}
```

**Congratulations!** You've successfully created your frst project on CRIPT. 

# Create a Collection node

A [`Collection`](../nodes/collection.md) can be thought of as a folder filled with experiments. Just like we did for a [`Project`](../nodes/project.md) node, we use the `create()` method to create a new [`Collection`](../nodes/collection.md). This time, we're also specifying the project that we just created. This will create the new collection **inside** our project. 

``` python
coll = cript.Collection.create(
    project=proj,
    name="My new collection",
)
```

# Create an Experiment node

The CRIPT [`Experiment`](../nodes/experiment.md) node holds [`Process`](../nodes/process.md) and [`Data`](../nodes/data.md) nodes. Now that we have a project and a collection, let's add an [`Experiment`](../nodes/experiment.md) inside our collection.

``` python
expt = cript.Experiment.create(
    collection=coll,
    name="Anionic Polymerization of Styrene with SecBuLi"
)
```

# Get Material nodes

[`Material`](../nodes/material.md) and [`Inventory`](../nodes/inventory.md) nodes can be created in the same way that [`Project`](../nodes/project.md), [`Collection`](../nodes/collection.md), and [`Experiment`](../nodes/experiment.md) nodes were created.

For this tutorial, instead of creating new [`Material`](../nodes/material.md) and [`Inventory`](../nodes/inventory.md) nodes, we will get references to existing nodes using the `<node>.get()` method. The inventory we will get contains all of the [`Material`](../nodes/material.md) nodes we will be using.

``` python
# UID of the inventory node we wish to get
uid = "134f2658-6245-42d8-a47e-6424aa3472b4"
# get the inventory by its UID
inv = cript.Inventory.get(uid=uid, get_level=1)
```

!!! note
    We are setting `get_level` to `1` so that all the inventory's children material nodes are collected as well. This parameter defaults to `0`, but can be set to any integer.

To see what our command returned, use:

``` python
print(type(inv.materials[0]))
```

Something similar to the following should be printed:
``` bash
<class 'cript.data_model.nodes.material.Material'>
```

We've shown that we can get an existing [`Inventory`](../nodes/inventory.md) node using the `get()` method, and that the inventory object has an attribute called `materials`. By printing the first instance of the `materials` attribute, we can see that a [`Material`](../nodes/material.md) object is returned.

# Create a Process node

Now let's create a [`Process`](../nodes/process.md) node using the same `create()` method we used before. Here we are creating the `Process` inside the experiment called `expt` that was previously created. We're also giving the `Process` a name, a `type`, and a `description`.

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

!!! note "Process types"
    The allowed `Process` types are listed in the <a href="https://criptapp.org/keys/process-type/" target="_blank">process type keywords</a> in the CRIPT controlled vocabulary.

# Add Ingredients to a Process

From a chemistry standpoint, most experimental processeses, regardless of whether they are carried out in the lab or simulated using computer code, consist of input ingredients that are transformed in some way. Let's add ingredients to the [`Process`](../nodes/process.md) that we just created.

First, get references to the [`Material`](../nodes/material.md) nodes that were contained within the [`Inventory`](../nodes/inventory.md) node:

``` python
solution = inv['SecBuLi solution 1.4M cHex']
toluene = inv['toluene']
styrene = inv['styrene']
butanol = inv['1-butanol']
methanol = inv['methanol']
```

Next, define [`Quantity`](../subobjects/quantity.md) nodes indicating the amount of each [`Ingredient`](../subobjects/ingredient.md) that we will use in the [`Process`](../nodes/process.md).

``` python
initiator_qty = cript.Quantity(key="volume", value=0.017, unit="ml")
solvent_qty = cript.Quantity(key="volume", value=10, unit="ml")
monomer_qty = cript.Quantity(key="mass", value=0.455, unit="g")
quench_qty = cript.Quantity(key="volume", value=5, unit="ml")
workup_qty = cript.Quantity(key="volume", value=100, unit="ml")
```

Now we can create an [`Ingredient`](../subobjects/ingredient.md) node for each ingredient using the `material` and `quantities` attributes.

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

!!! note "Ingredient keywords"
    The allowed `Ingredient` keywords are listed in the <a href="https://criptapp.org/keys/ingredient-keyword/" target="_blank">ingredient keywords</a> in the CRIPT controlled vocabulary.

Finally, we can add the [`Ingredient`](../subobjects/ingredient.md) nodes to the [`Process`](../nodes/process.md) node.

``` python
prcs.add_ingredient(initiator)
prcs.add_ingredient(solvent)
prcs.add_ingredient(monomer)
prcs.add_ingredient(quench)
prcs.add_ingredient(workup)
```

# Add Conditions to the Process

Its possible that our [`Process`](../nodes/process.md) was carried out under specific physical conditions. We can codify this by adding [`Condition`](../subobjects/condition.md) nodes to the process.

``` python
temp = cript.Condition(key="temperature", value=25, unit="celsius")
time = cript.Condition(key="time_duration", value=60, unit="min")
prcs.add_condition(temp)
prcs.add_condition(time)
```

!!! note "Condition keys"
    The allowed `Condition` keys are listed in the <a href="https://criptapp.org/keys/condition-key/" target="_blank">condition keys</a> in the CRIPT controlled vocabulary.


# Add a Property to a Process

We may also want to associate our process with certain properties. We can do this by adding [`Property`](../subobjects/property.md) nodes to the process.

``` python
yield_mass = cript.Property(
    key="yield_mass",
    value=0.47,
    unit="g",
    method="scale"
)
prcs.add_property(yield_mass)
```

!!! note "Process property keys"
    The allowed process `Property` keys are listed in the <a href="https://criptapp.org/keys/process-property-key/" target="_blank">process property keys</a> in the CRIPT controlled vocabulary.

!!! note "Property methods"
    The allowed `Property` methods are listed in the <a href="https://criptapp.org/keys/property-method/" target="_blank">property methods</a> in the CRIPT controlled vocabulary.


# Create a Material node (process product)

Along with input [`Ingredients`](../subobjects/ingredient.md), our `Process` may also produce product materials.

First, let's create the [`Material`](../nodes/material.md) that will serve as our product. We give the material a `name` attribute and add it to our `Project` using the project's `uid` attribute.

``` python
polystyrene = cript.Material(
    project=proj.uid,
    name="polystyrene",
)
```

Note that we haven't used the `Material.create()` method here, which means that our `Material` node is not yet saved to the CRIPT database. We've merely created an instance of a `Material` object using `cript.Material()`. We will add some more attributes to this `Material` object before we save it.

Let's add some [`Identifier`](../subobjects/identifier.md) nodes to the material to make it easier to identify and search.

``` python
# create a name identifier
names = cript.Identifier(
    key="names",
    value=["poly(styrene)", "poly(vinylbenzene)"]
)
# create a BigSMILES identifier
bigsmiles = cript.Identifier(
    key="bigsmiles",
    value="[H]{[>][<]C(C[>])c1ccccc1[<]}C(C)CC"
)
# create a chemical repeat unit identifier
chem_repeat = cript.Identifier(
    key="chem_repeat",
    value="C8H8",
)

# add the identifiers to the material
polystyrene.add_identifier(names)
polystyrene.add_identifier(chem_repeat)
polystyrene.add_identifier(bigsmiles)
```

!!! note "Identifier keys"
    The allowed `Identifier` keys are listed in the <a href="https://criptapp.org/keys/material-identifier-key/" target="_blank">material identifier keys</a> in the CRIPT controlled vocabulary.

Next, we'll add some [`Property`](../subobjects/property.md) nodes to the `Material`, which represent its physical or virtual (in the case of a simulated material) properties.

``` python
# create a phase property
phase = cript.Property(
    key="phase",
    value="solid",
)
# create a color property
color = cript.Property(
    key="color",
    value="white",
)

# add the properties to the material
polystyrene.add_property(phase)
polystyrene.add_property(color)
```

!!! note "Material property keys"
    The allowed material `Proeprty` keys are listed in the <a href="https://criptapp.org/keys/material-property-key/" target="_blank">material property keys</a> in the CRIPT controlled vocabulary.

Finally we can save the `Material` node, add it as a product to the `Process` node, and then save the changes to the `Process` node.

``` python
# save the material
polystyrene.save()
# add the material as a product of the process
prcs.add_product(polystyrene)

# save the resulting process
prcs.save()
```

*Congratulations!** You've just created a process that represents the polymerization reaction of Polystyrene, starting with a set of input ingredients in various quantities, and ending with a new polymer with specific identifiers and physical properties.




# Create a File node and upload a file

We may want to upload files to CRIPT which contain materials characterization data, simulation data, instrument settings, or other information. While CRIPT can store the actual file object, we can also create a CRIPT `File` node which represents the file and can be linked to other CRIPT nodes.

First, let's instantiate a File node (note that we're not saving it yet) and associate with the Data node created above.

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
