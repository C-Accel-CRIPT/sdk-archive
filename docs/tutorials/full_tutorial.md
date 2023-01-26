# 1. Install CRIPT
Before proceeding, please make sure you have the <a href="https://pypi.org/project/cript/" target="_blank">CRIPT Python SDK</a> installed (`pip install cript`). For full installation instructions, please refer to the <a href="../installation" target="_blank">Installation docs</a>.

# 2. Connect to CRIPT
To connect to <a href="https://criptapp.org" target="_blank">CRIPT</a>, you must enter a `host` and an `API Token`. For most users, `host` will be `criptapp.org`.

An API token tells CRIPT who you are and ensures that you have permission to view and upload certain types of data. Your API Token can be found in the CRIPT application <a href="https://criptapp.org/security/" target="_blank">security settings</a>. For additional details, please refer to <a href="../api_token" target="_blank">Getting an API Token</a>.

!!! note
    The word `Token` in front of the random token characters is part of the token as well. Always copy the entire token text.

It is *highly* recommended that you store your API token in a safe location and read it into your code, rather than have it hard-coded. One way to do this is to store
it in an environment variable (e.g., `CRIPT_API_KEY`) and then read it in via the `os` module. See <a href="../api_token" target="_blank">Getting an API Token</a> to learn more:
 
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

# 3. Create a <a href="../../nodes/project" target="_blank">`Project`</a> node

??? "What is a node?"
    A *node* is simply a CRIPT object (e.g., `Project`, `Experiment`, `Material`) in the graph-based CRIPT data model. 

All data uploaded to CRIPT must be associated with a <a href="../../nodes/project" target="_blank">`Project`</a> node. A <a href="../../nodes/project" target="_blank">`Project`</a> can be thought of as a folder that contains <a href="../../nodes/collection" target="_blank">`Collections`</a> and <a href="../../nodes/material" target="_blank">`Materials`</a>. To create a <a href="../../nodes/project" target="_blank">`Project`</a> and upload it to CRIPT, use the <a href="../../nodes/base_node/#cript.data_model.nodes.base_node.BaseNode.create" target="_blank">`cript.<node>.create()`</a> method, where `<node>` can be any of the <a href="../../nodes/all" target="_blank">primary CRIPT node types</a>:

```python
# create a new project in the CRIPT database
my_proj = cript.Project.create(name="My first project")
```

!!! info "Notes"
    * <a href="../../nodes/project" target="_blank">`Project`</a> names are globally unique, meaning no two <a href="../../nodes/project" target="_blank">`Projects`</a> in the entire CRIPT database can have the same name.
    * The <a href="../../nodes/base_node/#cript.data_model.nodes.base_node.BaseNode.create" target="_blank">`cript.<node>.create()`</a> method both *instantiates* the Python object and *uploads* it to the database in one command.

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

**Congratulations!** You've successfully created your first project on CRIPT. 

# 4. Create a <a href="../../nodes/collection" target="_blank">`Collection`</a> node

A <a href="../../nodes/collection" target="_blank">`Collection`</a> can be thought of as a folder filled with <a href="../../nodes/experiment" target="_blank">`Experiments`</a>. Just like we did for a <a href="../../nodes/project" target="_blank">`Project`</a> node, we use the <a href="../../nodes/base_node/#cript.data_model.nodes.base_node.BaseNode.create" target="_blank">`cript.<node>.create()`</a> method to create a new <a href="../../nodes/collection" target="_blank">`Collection`</a>. However, we also have to specify the <a href="../../nodes/project" target="_blank">`Project`</a> that this <a href="../../nodes/collection" target="_blank">`Collection`</a> will belong to. Let's use the project we just created: 

``` python
my_coll = cript.Collection.create(
    project=my_proj,
    name="My new collection",
)
```

# 5. Create an <a href="../../nodes/experiment" target="_blank">`Experiment`</a> node

An <a href="../../nodes/experiment" target="_blank">`Experiment`</a> node can hold <a href="../../nodes/process" target="_blank">`Process`</a> and <a href="../../nodes/data" target="_blank">`Data`</a> nodes. Similar to how a <a href="../../nodes/collection" target="_blank">`Collection`</a> must belong to a certain <a href="../../nodes/project" target="_blank">`Project`</a>, an <a href="../../nodes/experiment" target="_blank">`Experiment`</a> must belong to a <a href="../../nodes/collection" target="_blank">`Collection`</a>:

``` python
my_expt = cript.Experiment.create(
    collection=my_coll,
    name="Anionic Polymerization of Styrene with SecBuLi"
)
```

# 6. Get <a href="../../nodes/material" target="_blank">`Material`</a> nodes

<a href="../../nodes/material" target="_blank">`Material`</a> and <a href="../../nodes/inventory" target="_blank">`Inventory`</a> nodes can be created in the same way that <a href="../../nodes/project" target="_blank">`Project`</a>, <a href="../../nodes/collection" target="_blank">`Collection`</a>, and <a href="../../nodes/Experiment" target="_blank">`Experiment`</a>  nodes were created.

For this tutorial, instead of creating new <a href="../../nodes/material" target="_blank">`Material`</a> and <a href="../../nodes/inventory" target="_blank">`Inventory`</a> nodes, we will get references to existing nodes using the <a href="../../nodes/base_node/#cript.data_model.nodes.base_node.BaseNode.get" target="_blank">`cript.<node>.get()`</a> method. The <a href="../../nodes/inventory" target="_blank">`Inventory`</a> we will get contains all of the <a href="../../nodes/material" target="_blank">`Material`</a> nodes we will be using.

``` python
# UID of the inventory node we wish to get
inv_uid = "134f2658-6245-42d8-a47e-6424aa3472b4"
# get the inventory by its UID
my_inv = cript.Inventory.get(uid=inv_uid, get_level=1)
```

!!! note
    We are setting `get_level` to `1` so that all the <a href="../../nodes/inventory" target="_blank">`Inventory's`</a> children <a href="../../nodes/material" target="_blank">`Material`</a> nodes are collected as well. This parameter defaults to `0`, but can be set to any integer.

To see what this command returned, use:

``` python
print(type(my_inv.materials[0]))
```

Something similar to the following should be printed:
``` bash
<class 'cript.data_model.nodes.material.Material'>
```

We see that the <a href="../../nodes/inventory" target="_blank">`Inventory`</a> object has an attribute called `materials`. By printing the first element of the `materials` list, we can see that a <a href="../../nodes/material" target="_blank">`Material`</a> node is returned.

# 7. Create a <a href="../../nodes/process" target="_blank">`Process`</a> node

Now let's create a <a href="../../nodes/process" target="_blank">`Process`</a> node using the same <a href="../../nodes/base_node/#cript.data_model.nodes.base_node.BaseNode.create" target="_blank">`cript.<node>.create()`</a> method we used before. For a <a href="../../nodes/process" target="_blank">`Process`</a>, we must specify the <a href="../../nodes/experiment" target="_blank">`Experiment`</a> it belongs to:

``` python
my_prcs = cript.Process.create(
    experiment=my_expt,
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
    The allowed <a href="../../nodes/process" target="_blank">`Process`</a> types are listed in the <a href="https://criptapp.org/keys/process-type/" target="_blank">process type keywords</a> in the CRIPT controlled vocabulary.

# 8. Add <a href="../../subobjects/ingredient" target="_blank">`Ingredients`</a> to a <a href="../../nodes/process" target="_blank">`Process`</a>

From a chemistry standpoint, most experimental processeses, regardless of whether they are carried out in the lab or simulated using computer code, consist of input ingredients that are transformed in some way. Let's add <a href="../../subobjects/ingredient" target="_blank">`Ingredients`</a> to the <a href="../../nodes/process" target="_blank">`Process`</a> that we just created.

First, get references to the <a href="../../nodes/material" target="_blank">`Material`</a> nodes that were contained within the <a href="../../nodes/inventory" target="_blank">`Inventory`</a> node:

``` python
solution = my_inv['SecBuLi solution 1.4M cHex']
toluene = my_inv['toluene']
styrene = my_inv['styrene']
butanol = my_inv['1-butanol']
methanol = my_inv['methanol']
```

Next, define <a href="../../subobjects/quantity" target="_blank">`Quantity`</a> nodes indicating the amount of each <a href="../../subobjects/ingredient" target="_blank">`Ingredient`</a> that we will use in the <a href="../../nodes/process" target="_blank">`Process`</a>.

``` python
initiator_qty = cript.Quantity(key="volume", value=0.017, unit="ml")
solvent_qty = cript.Quantity(key="volume", value=10, unit="ml")
monomer_qty = cript.Quantity(key="mass", value=0.455, unit="g")
quench_qty = cript.Quantity(key="volume", value=5, unit="ml")
workup_qty = cript.Quantity(key="volume", value=100, unit="ml")
```

Now we can create an <a href="../../subobjects/ingredient" target="_blank">`Ingredients`</a> node for each ingredient using the `material` and `quantities` attributes.

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
    The allowed <a href="../../subobjects/ingredient" target="_blank">`Ingredient`</a> keywords are listed in the <a href="https://criptapp.org/keys/ingredient-keyword/" target="_blank">ingredient keywords</a> in the CRIPT controlled vocabulary.

Finally, we can add the <a href="../../subobjects/ingredient" target="_blank">`Ingredients`</a> nodes to the <a href="../../nodes/process" target="_blank">`Process`</a> node.

``` python
my_prcs.add_ingredient(initiator)
my_prcs.add_ingredient(solvent)
my_prcs.add_ingredient(monomer)
my_prcs.add_ingredient(quench)
my_prcs.add_ingredient(workup)
```

# 9. Add <a href="../../subobjects/condition" target="_blank">`Conditions`</a> to the <a href="../../nodes/process" target="_blank">`Process`</a>

It's possible that our <a href="../../nodes/process" target="_blank">`Process`</a> was carried out under specific physical conditions. We can codify this by adding <a href="../../subobjects/condition" target="_blank">`Condition`</a> nodes to the process.

``` python
my_temp = cript.Condition(key="temperature", value=25, unit="celsius")
my_time = cript.Condition(key="time_duration", value=60, unit="min")
my_prcs.add_condition(my_temp)
my_prcs.add_condition(my_time)
```

!!! note "Condition keys"
    The allowed <a href="../../subobjects/condition" target="_blank">`Condition`</a> keys are listed in the <a href="https://criptapp.org/keys/condition-key/" target="_blank">condition keys</a> in the CRIPT controlled vocabulary.


# 10. Add a <a href="../../subobjects/property" target="_blank">`Property`</a> to a <a href="../../nodes/process" target="_blank">`Process`</a>

We may also want to associate our process with certain properties. We can do this by adding <a href="../../subobjects/property" target="_blank">`Property`</a> nodes to the process.

``` python
yield_mass = cript.Property(
    key="yield_mass",
    value=0.47,
    unit="g",
    method="scale"
)
my_prcs.add_property(yield_mass)
```

!!! note "Process property keys"
    The allowed process  <a href="../../subobjects/property" target="_blank">`Property`</a> keys are listed in the <a href="https://criptapp.org/keys/process-property-key/" target="_blank">process property keys</a> in the CRIPT controlled vocabulary.

!!! note "Property methods"
    The allowed <a href="../../subobjects/property" target="_blank">`Property`</a> methods are listed in the <a href="https://criptapp.org/keys/property-method/" target="_blank">property methods</a> in the CRIPT controlled vocabulary.


# 11. Create a <a href="../../nodes/material" target="_blank">`Material`</a> node as a <a href="../../nodes/process" target="_blank">`Process`</a> product

Along with input <a href="../../subobjects/ingredient" target="_blank">`Ingredients`</a>, our <a href="../../nodes/process" target="_blank">`Process`</a> may also produce product <a href="../../nodes/material" target="_blank">`Materials`</a>.

First, let's create the <a href="../../nodes/material" target="_blank">`Material`</a> that will serve as our product. We give the material a `name` attribute and add it to our <a href="../../nodes/project" target="_blank">`Project`</a> using the project's `uid` attribute.

``` python
polystyrene = cript.Material(
    project=my_proj.uid,
    name="polystyrene",
)
```

Note that we haven't used the `cript.Material.create()` method here, which means that our <a href="../../nodes/material" target="_blank">`Material`</a> node is not yet saved to the CRIPT database. By using `cript.Material()`, we've only created an instance of a Python object. We will add some more attributes to this <a href="../../nodes/material" target="_blank">`Material`</a> object before we save it.

Let's add some <a href="../../subobjects/identifier" target="_blank">`Identifier`</a> nodes to the <a href="../../nodes/material" target="_blank">`Material`</a> to make it easier to identify and search.

``` python
# create a name identifier
my_names = cript.Identifier(
    key="names",
    value=["poly(styrene)", "poly(vinylbenzene)"]
)
# create a BigSMILES identifier
my_bigsmiles = cript.Identifier(
    key="bigsmiles",
    value="[H]{[>][<]C(C[>])c1ccccc1[<]}C(C)CC"
)
# create a chemical repeat unit identifier
my_chem_repeat = cript.Identifier(
    key="chem_repeat",
    value="C8H8",
)

# add the identifiers to the material
polystyrene.add_identifier(my_names)
polystyrene.add_identifier(my_chem_repeat)
polystyrene.add_identifier(my_bigsmiles)
```

!!! note "Identifier keys"
    The allowed <a href="../../subobjects/identifier" target="_blank">`Identifier`</a> keys are listed in the <a href="https://criptapp.org/keys/material-identifier-key/" target="_blank">material identifier keys</a> in the CRIPT controlled vocabulary.

Next, we'll add some <a href="../../subobjects/property" target="_blank">`Property`</a> nodes to the <a href="../../nodes/material" target="_blank">`Material`</a>, which represent its physical or virtual (in the case of a simulated material) properties.

``` python
# create a phase property
my_phase = cript.Property(
    key="phase",
    value="solid",
)
# create a color property
my_color = cript.Property(
    key="color",
    value="white",
)

# add the properties to the material
polystyrene.add_property(my_phase)
polystyrene.add_property(my_color)
```

!!! note "Material property keys"
    The allowed material <a href="../../subobjects/property" target="_blank">`Property`</a> keys are listed in the <a href="https://criptapp.org/keys/material-property-key/" target="_blank">material property keys</a> in the CRIPT controlled vocabulary.

Finally we can save the <a href="../../nodes/material" target="_blank">`Material`</a> node, add it as a product to the <a href="../../nodes/process" target="_blank">`Process`</a> node, and then save the changes to the <a href="../../nodes/process" target="_blank">`Process`</a> node.

``` python
# save the material
polystyrene.save()
# add the material as a product of the process
my_prcs.add_product(polystyrene)

# save the resulting process
my_prcs.save()
```

**Congratulations!** You've just created a <a href="../../nodes/process" target="_blank">`Process`</a> that represents the polymerization reaction of Polystyrene, starting with a set of input <a href="../../subobjects/ingredient" target="_blank">`Ingredients`</a> in various <a href="../../subobjects/quantity" target="_blank">`Quantities`</a>, and ending with a new polymer with specific <a href="../../subobjects/identifier" target="_blank">`Identifiers`</a> and physical <a href="../../subobjects/property" target="_blank">`Properties`</a>.

# 12. Create a <a href="../../nodes/data" target="_blank">`Data`</a> node

We may want to associate some files with our polymerization reaction. For this, we will create a CRIPT <a href="../../nodes/data" target="_blank">`Data`</a> node, which helps us store files in an organized way. Note that we are attaching the <a href="../../nodes/data" target="_blank">`Data`</a> node to our previous <a href="../../nodes/experiment" target="_blank">`Experiment`</a>, but not saving it yet.

``` python
my_sec_data = cript.Data(
    experiment=my_expt,
    name="Crude SEC of polystyrene",
    type="sec_trace",
)
```

!!! note "Data types"
    The allowed <a href="../../nodes/data" target="_blank">`Data`</a> types are listed in the <a href="https://criptapp.org/keys/data-type/" target="_blank">data types</a> in the CRIPT controlled vocabulary.


# 13. Associate a <a href="../../nodes/data" target="_blank">`Data`</a> node with a <a href="../../subobjects/property" target="_blank">`Property`</a> node

Now lets associate our <a href="../../nodes/data" target="_blank">`Data`</a> with a specific <a href="../../nodes/material" target="_blank">`Material`</a> property. To do this, we'll create one more <a href="../../subobjects/property" target="_blank">`Property`</a> node for polystyrene.

``` python
poly_mw = cript.Property(
    key="mw_n",
    value=5200,
    unit="g/mol",
)
```

Next, we'll add the <a href="../../nodes/data" target="_blank">`Data`</a> node to the new <a href="../../subobjects/property" target="_blank">`Property`</a> node.

``` python
poly_mw.data = my_sec_data
```

Last, we'll add the new <a href="../../subobjects/property" target="_blank">`Property`</a> node to polystyrene and save it.

``` python
polystyrene.add_property(poly_mw)
polystyrene.save()
```

# 14. Create a <a href="../../nodes/file" target="_blank">`File`</a> node

Now that we have a <a href="../../nodes/data" target="_blank">`Data`</a> node object, we can add files to it. We may want to upload files to CRIPT which contain materials characterization data, simulation data, instrument settings, or other information. While CRIPT can store the actual file object, we can also create a CRIPT <a href="../../nodes/file" target="_blank">`File`</a> node which represents the file and can be linked to our other CRIPT node objects.

First, let's instantiate a <a href="../../nodes/file" target="_blank">`File`</a> node (note that we're not saving it yet) and associate it with the <a href="../../nodes/data" target="_blank">`Data`</a> node that we created above.

``` python
# specify the local path of the file
my_path = "~/quickstart.csv" # path to local file
# instantiate a new the file node
my_file = cript.File(
    project=my_proj,
    source=my_path,
)
```

!!! note
    The `source` field should point to a file on your local filesystem.

!!! info
    Depending on the file size, there could be a delay while the checksum is generated.

Next, we'll upload the local file by saving the <a href="../../nodes/file" target="_blank">`File`</a> node. Follow all prompts that appear.

``` python
my_file.save()
```

You will be prompted to click a link to obtain an authorization code for uploading this file to the CRIPT file storage client. Copy and paste the code obtained from this link into the terminal to save the file.

Once the <a href="../../nodes/file" target="_blank">`File`</a> node is saved, we add the newly uploaded file to our <a href="../../nodes/data" target="_blank">`Data`</a> node and save it.

``` python
my_sec_data.add_file(my_file)
my_sec_data.save()
```

# Conclusion

You made it! We hope this tutorial has been helpful.

Please let us know how you think it could be improved.
