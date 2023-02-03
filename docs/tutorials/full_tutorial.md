!!! abstract "Summary"
    This tutorial goes over creating a `Project`, `Collection`, `Experiment` and adding the process product to CRIPT 

# Install CRIPT

```
pip install cript
```

> For detailed installation instructions, please refer to the <a href="../installation" target="_blank">Installation docs</a>.

---

# Connect to CRIPT
To connect to <a href="https://criptapp.org" target="_blank">CRIPT</a>, you must enter a `host` and an `API Token`. For most users, `host` will be `criptapp.org`.

An API token tells CRIPT who you are and ensures that you have permission to view and upload certain types of data. 
Your API Token can be found in the CRIPT application <a href="https://criptapp.org/security/" target="_blank">security settings</a>. 
For additional details, please refer to <a href="../api_token" target="_blank">Getting an API Token</a>.

!!! warning "Security Warning"
    It is **highly** recommended that you store your API token as an environment variable, as explained in the [Getting an API Token](../api_token/).
 
``` python
import cript
import os

host = "criptapp.org"
token = os.environ.get("CRIPT_API_KEY")
cript.API(host, token)
```
> The word `Token` in front of the random characters is part of the token as well. 

You should see the following output:
``` bash
Connected to https://criptapp.org/api
```

??? "Private Instance of CRIPT"
    By default CRIPT uses `https` to connect to the host. 
    
    Connecting to a host via `http` can be done by setting `tls=False`:

    ```python 
    import cript
    import os
    
    host = "127.0.0.1:8000"
    token = os.environ.get("CRIPT_API_KEY")
    cript.API(host, token, tls=False)
    ```

---

# Create a <a href="../../nodes/project" target="_blank">`Project`</a> node

All data uploaded to CRIPT must be associated with a <a href="../../nodes/project" target="_blank">`Project`</a> node. A <a href="../../nodes/project" target="_blank">`Project`</a> can be thought of as a folder that contains <a href="../../nodes/collection" target="_blank">`Collections`</a> and <a href="../../nodes/material" target="_blank">`Materials`</a>. 

```python
my_project = cript.Project(name="My first project") # instantiate a new Project node (creating a new node) and name your project
my_project.save() # save your project to CRIPT database
```

!!! warning "Project Names Must Be Unique"
    <a href="../../nodes/project" target="_blank">`Project`</a> names are globally unique, meaning no two <a href="../../nodes/project" target="_blank">`Projects`</a> in the entire CRIPT database can have the same name.



??? note ".create( ) method"
    The <a href="../../nodes/base_node/#cript.data_model.nodes.base_node.BaseNode.create" target="_blank">`cript.<node>.create()`</a> method both *instantiates* a Python object and *saves* it to the CRIPT database in one command.

---

# Create a <a href="../../nodes/collection" target="_blank">`Collection`</a> node

A <a href="../../nodes/collection" target="_blank">`Collection`</a> can be thought of as a folder 
filled with <a href="../../nodes/experiment" target="_blank">`Experiments`</a>. 


A `Collection` can be created in the same way as `Project`, however, since every `Collection` must lives inside of a `Project`, the `Project` that this new `Collection` belongs to must be specified during instantiation.

``` python
my_collection = cript.Collection(
    project=my_project,
    name="My new collection",
)

my_collection.save()
```

---

# Create an <a href="../../nodes/experiment" target="_blank">`Experiment`</a> node

An <a href="../../nodes/experiment" target="_blank">`Experiment`</a> node can be thought of as a folder that can hold 
<a href="../../nodes/process" target="_blank">`Process`</a> and <a href="../../nodes/data" target="_blank">`Data`</a> nodes. 
An <a href="../../nodes/experiment" target="_blank">`Experiment`</a> lives inside of a <a href="../../nodes/collection" target="_blank">`Collection`</a> node:

``` python
# instantiate an experiment node 
# name your experiment
# put it inside of a collection
my_experiment = cript.Experiment(
    collection=my_collection,
    name="Anionic Polymerization of Styrene with SecBuLi"
)

my_experiment.save()
```

---

# Get <a href="../../nodes/material" target="_blank">`Material`</a> nodes

<a href="../../nodes/material" target="_blank">`Material`</a> and <a href="../../nodes/inventory" target="_blank">`Inventory`</a> nodes can be created in the same way that <a href="../../nodes/project" target="_blank">`Project`</a>, <a href="../../nodes/collection" target="_blank">`Collection`</a>, and <a href="../../nodes/Experiment" target="_blank">`Experiment`</a>  nodes were created.

For this tutorial, instead of creating new <a href="../../nodes/material" target="_blank">`Material`</a> and <a href="../../nodes/inventory" target="_blank">`Inventory`</a> nodes, we will get references to existing nodes using the <a href="../../nodes/base_node/#cript.data_model.nodes.base_node.BaseNode.get" target="_blank">`cript.<node>.get()`</a> method. The <a href="../../nodes/inventory" target="_blank">`Inventory`</a> we will get contains all of the <a href="../../nodes/material" target="_blank">`Material`</a> nodes we will be using.

``` python
# UID of the inventory node we wish to get
inv_uid = "134f2658-6245-42d8-a47e-6424aa3472b4"
# get the inventory by its UID
my_inventory = cript.Inventory.get(uid=inv_uid, get_level=1)
```

!!! note
    We are setting `get_level` to `1` so that all the <a href="../../nodes/inventory" target="_blank">`Inventory's`</a> children <a href="../../nodes/material" target="_blank">`Material`</a> nodes are collected as well. This parameter defaults to `0`, but can be set to any integer.

---

# Create a <a href="../../nodes/process" target="_blank">`Process`</a> node

Now let's create a <a href="../../nodes/process" target="_blank">`Process`</a> node using the same <a href="../../nodes/base_node/#cript.data_model.nodes.base_node.BaseNode.create" target="_blank">`cript.<node>.create()`</a> method we used before. For a <a href="../../nodes/process" target="_blank">`Process`</a>, we must specify the <a href="../../nodes/experiment" target="_blank">`Experiment`</a> it belongs to:

``` python
my_process = cript.Process(
    experiment=my_experiment,
    name="Anionic of Styrene",
    type = "multistep",
    description = "In an argon filled glovebox, a round bottom flask was filled with 216 ml of dried toluene. The "
                  "solution of secBuLi (3 ml, 3.9 mmol) was added next, followed by styrene (22.3 g, 176 mmol) to "
                  "initiate the polymerization. The reaction mixture immediately turned orange. After 30 min, "
                  "the reaction was quenched with the addition of 3 ml of methanol. The polymer was isolated by "
                  "precipitation in methanol 3 times and dried under vacuum."
)

my_process.save()
```

!!! info "Process types"
    The allowed <a href="../../nodes/process" target="_blank">`Process`</a> types are listed in the <a href="https://criptapp.org/keys/process-type/" target="_blank">process type keywords</a> in the CRIPT controlled vocabulary.


---

# Add <a href="../../subobjects/ingredient" target="_blank">`Ingredients`</a> to a <a href="../../nodes/process" target="_blank">`Process`</a>

Let's add <a href="../../subobjects/ingredient" target="_blank">`Ingredients`</a> to the <a href="../../nodes/process" target="_blank">`Process`</a> that we just created.

First, get references to the <a href="../../nodes/material" target="_blank">`Material`</a> nodes that were contained within the <a href="../../nodes/inventory" target="_blank">`Inventory`</a> node:

``` python
solution = my_inventory['SecBuLi solution 1.4M cHex']
toluene = my_inventory['toluene']
styrene = my_inventory['styrene']
butanol = my_inventory['1-butanol']
methanol = my_inventory['methanol']
```

Next, define <a href="../../subobjects/quantity" target="_blank">`Quantity`</a> nodes indicating the amount of each <a href="../../subobjects/ingredient" target="_blank">`Ingredient`</a> that we will use in the <a href="../../nodes/process" target="_blank">`Process`</a>.

``` python
# instantiate Quantity nodes
initiator_quantity = cript.Quantity(key="volume", value=0.017, unit="ml")
solvent_quantity = cript.Quantity(key="volume", value=10, unit="ml")
monomer_quantity = cript.Quantity(key="mass", value=0.455, unit="g")
quench_quantity = cript.Quantity(key="volume", value=5, unit="ml")
workup_quantity = cript.Quantity(key="volume", value=100, unit="ml")
```

Now we can create <a href="../../subobjects/ingredient" target="_blank">`Ingredients`</a> node for each ingredient using the `material` and `quantities` attributes.

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
my_process.add_ingredient(initiator)
my_process.add_ingredient(solvent)
my_process.add_ingredient(monomer)
my_process.add_ingredient(quench)
my_process.add_ingredient(workup)
```

---

# Add <a href="../../subobjects/condition" target="_blank">`Conditions`</a> to the <a href="../../nodes/process" target="_blank">`Process`</a>

It's possible that our <a href="../../nodes/process" target="_blank">`Process`</a> was carried out under specific physical conditions. We can codify this by adding <a href="../../subobjects/condition" target="_blank">`Condition`</a> nodes to the process.

``` python
my_temperature = cript.Condition(key="temperature", value=25, unit="celsius")
my_time = cript.Condition(key="time_duration", value=60, unit="min")
my_process.add_condition(my_temperature)
my_process.add_condition(my_time)
```

!!! note "Condition keys"
    The allowed <a href="../../subobjects/condition" target="_blank">`Condition`</a> keys are listed in the <a href="https://criptapp.org/keys/condition-key/" target="_blank">condition keys</a> in the CRIPT controlled vocabulary.

---

# Add a <a href="../../subobjects/property" target="_blank">`Property`</a> to a <a href="../../nodes/process" target="_blank">`Process`</a>

We may also want to associate our process with certain properties. This can be done by adding <a href="../../subobjects/property" target="_blank">`Property`</a> nodes to the process.

``` python
yield_mass = cript.Property(
    key="yield_mass",
    value=0.47,
    unit="g",
    method="scale"
)
my_process.add_property(yield_mass)
```

!!! note "Allowed Keys"
    * The allowed process  <a href="../../subobjects/property" target="_blank">`Property`</a> keys are listed in the <a href="https://criptapp.org/keys/process-property-key/" target="_blank">process property keys</a> in the CRIPT controlled vocabulary.

    * The allowed <a href="../../subobjects/property" target="_blank">`Property`</a> methods are listed in the <a href="https://criptapp.org/keys/property-method/" target="_blank">property methods</a> in the CRIPT controlled vocabulary.

---

# Create a <a href="../../nodes/material" target="_blank">`Material`</a> node as a <a href="../../nodes/process" target="_blank">`Process`</a> product

After the process is complete it may produce a product, this is referred to as a `Process Product`, which is essentially another `Material`.

``` python
# create a new material named my polystyrene
# add the newly created material to my project
my_polystyrene = cript.Material(
    name="my polystyrene",
    project=my_project
)
```

> Note: The material has only been created and not yet saved anywhere

Let's add some <a href="../../subobjects/identifier" target="_blank">`Identifier`</a> nodes to the <a href="../../nodes/material" target="_blank">`Material`</a> to make it easier to identify and search.

``` python
# add name identifier (the names this material is also known by)
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

Next, we'll add some <a href="../../subobjects/property" target="_blank">`Property`</a> properties to the <a href="../../nodes/material" target="_blank">`Material`</a>, which represent its physical or virtual (in the case of a simulated material) properties.

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
my_polystyrene.add_property(my_phase)
my_polystyrene.add_property(my_color)


# save the material
my_polystyrene.save()
```

!!! note "Material property keys"
    The allowed material <a href="../../subobjects/property" target="_blank">`Property`</a> keys are listed in the <a href="https://criptapp.org/keys/material-property-key/" target="_blank">material property keys</a> in the CRIPT controlled vocabulary.

Finally we can save the <a href="../../nodes/material" target="_blank">`Material`</a> node, add it as a product to the <a href="../../nodes/process" target="_blank">`Process`</a> node, and then save the changes to the <a href="../../nodes/process" target="_blank">`Process`</a> node.

``` python
# add the material as a product of the process
my_process.add_product(my_polystyrene)

# save the resulting process
my_process.save()
```

You've just created a <a href="../../nodes/process" target="_blank">`Process`</a> that represents the polymerization reaction of Polystyrene, starting with a set of input <a href="../../subobjects/ingredient" target="_blank">`Ingredients`</a> in various <a href="../../subobjects/quantity" target="_blank">`Quantities`</a>, and ending with a new polymer with specific <a href="../../subobjects/identifier" target="_blank">`Identifiers`</a> and physical <a href="../../subobjects/property" target="_blank">`Properties`</a>.

---

# Create a <a href="../../nodes/data" target="_blank">`Data`</a> node

We may want to associate some files with our polymerization reaction. For this, we will create a CRIPT <a href="../../nodes/data" target="_blank">`Data`</a> node, which helps us store files in an organized way. 

> Note that we are attaching the <a href="../../nodes/data" target="_blank">`Data`</a> node to our previous <a href="../../nodes/experiment" target="_blank">`Experiment`</a>, but not saving it yet.

``` python
my_sec_data = cript.Data(
    experiment=my_experiment,
    name="Crude SEC of polystyrene",
    type="sec_trace",
)
```

!!! note "Data types"
    The allowed <a href="../../nodes/data" target="_blank">`Data`</a> types are listed in the <a href="https://criptapp.org/keys/data-type/" target="_blank">data types</a> in the CRIPT controlled vocabulary.


---

# Associate a <a href="../../nodes/data" target="_blank">`Data`</a> node with a <a href="../../subobjects/property" target="_blank">`Property`</a> node

Now lets associate our <a href="../../nodes/data" target="_blank">`Data`</a> with a specific <a href="../../nodes/material" target="_blank">`Material`</a> property, molecular weight. To do this, we'll create one more <a href="../../subobjects/property" target="_blank">`Property`</a> node for polystyrene.

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

---

# Create a <a href="../../nodes/file" target="_blank">`File`</a> node

Now that we have a <a href="../../nodes/data" target="_blank">`Data`</a> node object, we can add files to it. We may want to upload files to CRIPT which contain materials characterization data, simulation data, instrument settings, or other information. While CRIPT can store the actual file object, we can also create a CRIPT <a href="../../nodes/file" target="_blank">`File`</a> node which represents the file and can be linked to our other CRIPT node objects.

First, let's instantiate a <a href="../../nodes/file" target="_blank">`File`</a> node (note that we're not saving it yet) and associate it with the <a href="../../nodes/data" target="_blank">`Data`</a> node that we created above.

``` python
# specify path to file
my_path = "path/to/my/file" # path to file

my_file = cript.File(   # instantiate a new the file node
    project=my_project, # associate it with a project
    source=my_path,     # say where the file is located
)
```

!!! note
    The `source` field should point to a file on your local filesystem.

??? info
    Depending on the file size, there could be a delay while the checksum is generated.

Next, we'll upload the local file by saving the <a href="../../nodes/file" target="_blank">`File`</a> node. Follow all prompts that appear.

``` python
my_file.save()
```
!!! info
    You will be prompted to click a link to obtain an authorization code for uploading this file to the CRIPT file storage client. Copy and paste the code obtained from this link into the terminal to save the file.

Once the <a href="../../nodes/file" target="_blank">`File`</a> node is saved, we add the newly uploaded file to our <a href="../../nodes/data" target="_blank">`Data`</a> node and save it.

``` python
my_sec_data.add_file(my_file)
my_sec_data.save()
```
