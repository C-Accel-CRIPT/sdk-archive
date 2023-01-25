This tutorial guides you through an example simulation workflow using the CRIPT Python SDK.

This tutorial assumes that you've already installed the `cript` python package and tried the [Quickstart](../quickstart.md) or [Full tutorial](full_tutorial.md) and have some understanding of the CRIPT data model.

# Connect to CRIPT

```py
import cript

host = "criptapp.org"
token = "<your_api_token>"
cript.API(host, token)
```

# Create a Project node

```py
proj = cript.Project.create(name="My simulation project")
```

# Create a Collection node

```py
coll = cript.Collection.create(
    project=proj,
    name="Simulation Tutorial",
)
```

# Create an Experiment node

```py
expt = cript.Experiment.create(
    collection=coll,
    name="Bulk simulation of polystyrene"
)
```

# Get the relevant Software nodes

This step assumes that some standard <a href="../../nodes/software" target="_blank">`Software`</a> nodes already exist in the CRIPT database. Instead of creating new ones, we use the `get()` method to reference the existing ones.

```py
python = cript.Software.get(
    name = "python",
    version = "3.9",
)
rdkit = cript.Software.get(
    name = "rdkit",
    version = "2020.9",
)
stage = cript.Software.get(
    name = "stage",
    source = "https://doi.org/10.1021/jp505332p",
)
packmol = cript.Software.get(
    name = "Packmol",
    source = "http://m3g.iqm.unicamp.br/packmol",
    version = "N/A"
)
openmm = cript.Software.get(
    name = "openmm",
    version = "7.5",
)
```

# Create Software Configurations

Now that we have our <a href="../../nodes/software" target="_blank">`Software`</a> nodes, we can create <a href="../../subobjects/software_configuration" target="_blank">`SoftwareConfiguration`</a> nodes, which will be used for constructing our <a href="../../nodes/computation" target="_blank">`Computation`</a> node.

We can also attach <a href="../../subobjects/algorithm" target="_blank">`Algorithm`</a> nodes to a <a href="../../subobjects/software_configuration" target="_blank">`SoftwareConfiguration`</a> node. The <a href="../../subobjects/algorithm" target="_blank">`Algorithm`</a> nodes may contain nested <a href="../../subobjects/parameter" target="_blank">`Parameter`</a> nodes, as shown in the example below.

```py
# create some software configuration nodes
python_config = cript.SoftwareConfiguration(software=python)
rdkit_config = cript.SoftwareConfiguration(software=rdkit)
stage_config = cript.SoftwareConfiguration(software=stage)

# create a software configuration node with a child Algorithm node
openmm_config = cript.SoftwareConfiguration(
    software = openmm,
    algorithms = [
        cript.Algorithm(
            key="+energy_minimization",
            type="initialization",
        ),
    ]
)

# create a software configuration node, with a child Algorithm node,
# which contains additional parameters
packmol_config = cript.SoftwareConfiguration(
    software = packmol,
    algorithms = [
        cript.Algorithm(
            key="+molecule_packing",
            type="initialization",
            parameters = [
                cript.Parameter(key="+maxit", value=50),
                cript.Parameter(key="+nloop", value=10),
                cript.Parameter(key="+tolerance", value=4.0, unit="angstrom"),
            ]
        )
    ]
)
```

!!! note "Algorithm keys"
    The allowed `Algorithm` keys are listed under <a href="https://criptapp.org/keys/algorithm-key/" target="_blank">algorithm keys</a> in the CRIPT controlled vocabulary.

!!! note "Parameter keys"
    The allowed `Parameter` keys are listed under <a href="https://criptapp.org/keys/parameter-key/" target="_blank">parameter keys</a> in the CRIPT controlled vocabulary.


# Create Computations

Now that we've created some <a href="../../subobjects/software_configuration" target="_blank">`SoftwareConfiguration`</a> nodes, we can used them to build full <a href="../../nodes/computation" target="_blank">`Computation`</a> nodes. Note that each <a href="../../nodes/computation" target="_blank">`Computation`</a> node is nested under a specific <a href="../../nodes/experiment" target="_blank">`Experiment`</a>.

In some cases, we may also want to add <a href="../../subobjects/condition" target="_blank">`Condition`</a> nodes to our computation, to specify the conditions at which the computation was carried out. An example of this is shown below.

```py
# create a Computation node
init = cript.Computation.create(
    experiment = expt,
    name = "Initial snapshot and force-field generation",
    type = "initialization",
    software_configurations = [
        python_config,
        rdkit_config,
        stage_config,
        packmol_config,
        openmm_config,
    ]
)

# create a computation node with Condition nodes
equi = cript.Computation.create(
    experiment = expt,
    name = "Equilibrate data prior to measurement",
    type = "MD",
    software_configurations = [python_config, openmm_config],
    conditions = [
        cript.Condition(key="time_duration", value=100.0, unit="ns"),
        cript.Condition(key="temperature", value=450.0, unit="K"),
        cript.Condition(key="pressure", value=1.0, unit="bar"),
        cript.Condition(key="number", value=31),
    ],
    prerequisite_computation = init,
)

bulk = cript.Computation.create(
    experiment = expt,
    name = "Bulk simulation for measurement",
    type = "MD",
    software_configurations = [python_config, openmm_config],
    conditions = [
        cript.Condition(key="time_duration", value=50.0, unit="ns"),
        cript.Condition(key="temperature", value=450.0, unit="K"),
        cript.Condition(key="pressure", value=1.0, unit="bar"),
        cript.Condition(key="number", value=31),
    ],
    prerequisite_computation = equi,
)

ana = cript.Computation.create(
        experiment = expt,
        name = "Density analysis",
        type = "analysis",
        software_configurations = [python_config],
        prerequisite_computation = bulk,
)
```

!!! note "Computation types"
    The allowed `Computation` types are listed under <a href="https://criptapp.org/keys/computation-type/" target="_blank">computation types</a> in the CRIPT controlled vocabulary.

!!! note "Condition keys"
    The allowed `Condition` keys are listed under <a href="https://criptapp.org/keys/condition-key/" target="_blank">condition keys</a> in the CRIPT controlled vocabulary.


# Create and Upload Files

New we'd like to upload files associated with our simulation. First, we'll instantiate our File nodes under a specific project.

```py
packing_file = cript.File(project=proj, source="path/to/local/file")
forcefield_file = cript.File(project=proj, source="path/to/local/file")
snap_file = cript.File(project=proj, source="path/to/local/file")
final_file = cript.File(project=proj, source="path/to/local/file")
```

!!! note
The `source` field should point to any file on your local filesystem.

!!! info
Depending on the file size, there could be a delay while the checksum is generated.

Next, we'll upload the local files by saving the File nodes. Follow all prompts that appear in the terminal.

```py
packing_file.save()
forcefield_file.save()
snap_file.save()
final_file.save()
```

# Create Data

Next, we'll create a <a href="../../nodes/data" target="_blank">`Data`</a> node which helps organize our <a href="../../nodes/file" target="_blank">`File`</a> nodes and links back to our <a href="../../nodes/computation" target="_blank">`Computation`</a> objects.

```py
packing_data = cript.Data.create(
    experiment = expt,
    name = "Loosely packed chains",
    type = "computation_config",
    files = [packing_file],
    computations = [init],
    notes = "PDB file without topology describing an initial system.",
)

forcefield_data = cript.Data.create(
    experiment = expt,
    name = "OpenMM forcefield",
    type = "computation_forcefield",
    files = [forcefield_file],
    computations = [init],
    notes = "Full forcefield definition and topology.",
)

equi_snap = cript.Data.create(
    experiment = expt,
    name = "Equilibrated simulation snapshot",
    type = "computation_config",
    files = [snap_file],
    computations = [equi],
)

final_data = cript.Data.create(
    experiment = expt,
    name = "Logged volume during simulation",
    type = "+raw_data",
    files = [final_file],
    computations = [bulk],
)
```

!!! note "Data types"
    The allowed `Data` types are listed under the <a href="https://criptapp.org/keys/data-type/" target="_blank">data types</a> in the CRIPT controlled vocabulary.


Next, we'll link these <a href="../../nodes/data" target="_blank">`Data`</a> nodes to the appropriate <a href="../../nodes/computation" target="_blank">`Computation`</a> nodes.

```py
init.update(output_data=[packing_data, forcefield_data])
equi.update(
    input_data=[packing_data, forcefield_data],
    output_data=[equi_snap]
)
ana.update(input_data=[final_data])
bulk.update(output_data=[final_data])
```

!!! note
    Notice the use of `update()` here, which updates and saves the object in one go.

# Create a virtual Material

Finally, we'll create a virtual material and link it to the <a href="../../nodes/computation" target="_blank">`Computation`</a> nodes that we've built.

```py
polystyrene = cript.Material(
    project=proj,
    name="virtual polystyrene",
)
```

Next, let's add some [`Identifier`](../subobjects/identifier.md) nodes to the material to make it easier to identify and search.

```py
names = cript.Identifier(
    key="names",
    value=["poly(styrene)", "poly(vinylbenzene)"],
)

bigsmiles = cript.Identifier(
    key="bigsmiles",
    value="[H]{[>][<]C(C[>])c1ccccc1[<]}C(C)CC",
)

chem_repeat = cript.Identifier(
    key="chem_repeat",
    value="C8H8",
)

polystyrene.add_identifier(names)
polystyrene.add_identifier(chem_repeat)
polystyrene.add_identifier(bigsmiles)
```

!!! note "Identifier keys"
    The allowed `Identifier` keys are listed in the <a href="https://criptapp.org/keys/material-identifier-key/" target="_blank">material identifier keys</a> in the CRIPT controlled vocabulary.

Let's also add some [`Property`](../subobjects/property.md) nodes to the `Material`, which represent its physical or virtual (in the case of a simulated material) properties.

```py
phase = cript.Property(key="phase", value="solid")
color = cript.Property(key="color", value="white")

polystyrene.add_property(phase)
polystyrene.add_property(color)
```

!!! note "Material property keys"
    The allowed material `Property` keys are listed in the <a href="https://criptapp.org/keys/material-property-key/" target="_blank">material property keys</a> in the CRIPT controlled vocabulary.


Finally, we'll create a [`ComputationalForcefield`](../subobjects/computational_forcefield.md) node and link it to the Material.

```py
forcefield = cript.ComputationalForcefield(
    key="opls_aa",
    building_block="atom",
    source="Custom determination via STAGE",
    data=forcefield_data,
)

polystyrene.computational_forcefield = forcefield
polystyrene.save()
```

!!! note "Computational forcefield keys"
    The allowed `ComputationalForcefield` keys are listed under the <a href="https://criptapp.org/keys/computational-forcefield-key/" target="_blank">computational forcefield keys</a> in the CRIPT controlled vocabulary.


# Conclusion

You made it! We hope this tutorial has been helpful.

Please let us know how you think it could be improved.
