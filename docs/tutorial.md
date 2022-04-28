> Refer to [Quickstart](./quickstart.md) for installation instructions.

### Connect to the public API
```python
import cript

url = "https://criptapp.org"
token = "<your_api_token>"  
api = cript.API(base_url=url, api_token=token)
```
<sup>**Note**: Your API token can be found in the UI under [Account Settings](https://criptapp.org/settings/).</sup>


### Create a Group node
```python
group = cript.Group(name="MyGroup")
api.save(group)
```
<sup>**Note**: Group names are globally unique.</sup>

### Create a Collection node
```python
coll = cript.Collection(group=group, name="Tutorial")
api.save(coll)
```

### Create an Experiment node
```python
expt = cript.Experiment(collection=coll, name="Anionic Polymerization of Styrene with SecBuLi")
api.save(expt)
```

### Get Material nodes
For this tutorial, we will get an existing Inventory node from the database.  
This contains all of the Material nodes we will be using.
```python
url = "https://criptapp.org/api/inventory/134f2658-6245-42d8-a47e-6424aa3472b4/"
inv = api.get(url)
```

Notice that the Material node objects have been auto-generated.
```python
type(inv.materials[0])
# <class 'cript.nodes.Material'>
```
<sup>**Note**: By default, nested node generation occurs one level deep. You can modify this with the `max-level` argument.</sup>


### Create a Process node
```python
prcs = cript.Process(
    experiment=expt, 
    name="Anionic of Styrene",
    description = "In an argon filled glovebox, a round bottom flask was filled with 216 ml of dried toluene. The "
                  "solution of secBuLi (3 ml, 3.9 mmol) was added next, followed by styrene (22.3 g, 176 mmol) to "
                  "initiate the polymerization. The reaction mixture immediately turned orange. After 30 min, "
                  "the reaction was quenched with the addition of 3 ml of methanol. The polymer was isolated by "
                  "precipitation in methanol 3 times and dried under vacuum."
)
api.save(prcs)
```

### Add Ingredient nodes to the Process node
First, let's grab the Material nodes we need from the Inventory node.
```python
solution = next((mat for mat in inv.materials if mat.name == 'SecBuLi solution 1.4M cHex'), None)
toluene = next((mat for mat in inv.materials if mat.name == 'toluene'), None)
styrene = next((mat for mat in inv.materials if mat.name == 'styrene'), None)
butanol = next((mat for mat in inv.materials if mat.name == '1-butanol'), None)
methanol = next((mat for mat in inv.materials if mat.name == 'methanol'), None)
```
Next, we'll define Quantity nodes indicating the amount of each Ingredient.
```python
initiator_qty = cript.Quantity(key="volume", value=0.017, unit="ml")
solvent_qty = cript.Quantity(key="volume", value=10, unit="ml")
monomer_qty = cript.Quantity(key="mass", value=0.455, unit="g")
quench_qty = cript.Quantity(key="volume", value=5, unit="ml")
workup_qty = cript.Quantity(key="volume", value=100, unit="ml")
```
Next, we'll create Ingredient nodes for each.
```python
initiator = cript.Ingredient(keyword="initiator" ,ingredient=solution, quantities=[initiator_qty])
solvent = cript.Ingredient(keyword="solvent" ,ingredient=toluene, quantities=[solvent_qty])
monomer = cript.Ingredient(keyword="monomer" ,ingredient=styrene, quantities=[monomer_qty])
quench = cript.Ingredient(keyword="quench" ,ingredient=butanol, quantities=[quench_qty])
workup = cript.Ingredient(keyword="workup" ,ingredient=methanol, quantities=[workup_qty])
```
Last, we'll add the Ingredient nodes to the Process node.
```python
prcs.add_ingredient(initiator)
prcs.add_ingredient(solvent)
prcs.add_ingredient(monomer)
prcs.add_ingredient(quench)
prcs.add_ingredient(workup)
```

### Add Condition nodes to the Process node
First, we'll define a temperature.
```python
temp = cript.Condition(key="temperature", value=25, unit="celsius")
prcs.add_condition(temp)
```
Next, we'll define the duration.
```python
time = cript.Condition(key="time_duration", value=60, unit="min")
prcs.add_condition(time)
```

### Add a Property node to the Process node
```python
yield_mass = cript.Property(key="yield_mass", value=0.47, unit="g", method="scale")
prcs.add_property(yield_mass)
```

### Create a Material node (process product)
First, we'll instantiate the node.
```python
polystyrene = cript.Material(group=group, name="polystyrene")
```
Next, we'll add some Identifier nodes.
```python
names = cript.Identifier(key="names", value=["poly(styrene)", "poly(vinylbenzene)"])
chem_repeat = cript.Identifier(key="chem_repeat", value="C8H8")
bigsmiles = cript.Identifier(key="bigsmiles", value="[H]{[>][<]C(C[>])c1ccccc1[<]}C(C)CC")
cas = cript.Identifier(key="cas", value="100-42-5")

polystyrene.add_identifier(names)
polystyrene.add_identifier(chem_repeat)
polystyrene.add_identifier(bigsmiles)
polystyrene.add_identifier(cas)
```
Next, we'll add some Property nodes.
```python
phase = cript.Property(key="phase", value="solid")
color = cript.Property(key="color", value="white")

polystyrene.add_property(phase)
polystyrene.add_property(color)
```
Now we can save the Material and add it to the Process node as a product.
```python
api.save(polystyrene)
prcs.add_product(polystyrene)
```
Last, we can save the Process node.
```python
api.save(prcs)
```

### Create a Data node
```python
sec = cript.Data(
    experiment=expt, 
    name="Crude SEC of polystyrene", 
    type="sec_trace",
    sample_prep = "5 mg of polymer in 1 ml of THF, filtered 0.45um pores.",
)
api.save(sec)
```

### Create a File node and upload a file
First, we'll instantiate a File node and associate with the Data node created above.
```python
path = "path/to/local/file"
f = cript.File(group=group, data=[sec], source=path)
```
<sup>**Note**: The `source` field should point to a file on your local filesystem.</sup>  
<sup>**Note**: Depending on the file size, there could be a delay while the checksum is generated.</sup>

Next, we'll upload the local file by saving the File node. Follow all prompts that appear.
```python
api.save(f)
```

### Associate a Data node with a Property node
First, we'll create one more Property node for polystyrene.
```python
mw_n = cript.Property(key="mw_n", value=5200, unit="g/mol")
```
Next, we'll add the Data node to the new Property node.
```python
mw_n.add_data(sec)
```
Last, we'll add the new Property node to polystyrene then save it.
```python
polystyrene.add_property(mw_n)
api.save(polystyrene)
```

### Conclusion
You made it!  
We hope this tutorial has been helpful. Please let us know how it could improve.


