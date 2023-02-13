This tutorial guides you through an example simulation workflow using the CRIPT Python SDK. This tutorial assumes that you've already installed the `cript` python package and tried the <a href="../../quickstart" target="_blank">Quickstart</a> or <a href="../full_tutorial" target="_blank">Full tutorial</a> and have some understanding of the CRIPT data model.

# Connect to CRIPT

``` python
import cript
import os

host = "criptapp.org"
token = os.environ.get("CRIPT_API_KEY")
cript.API(host, token)
```

# Create a Project node

```py
my_project = cript.Project(name="My simulation project")
my_project.save()
```

# Create a Collection node

```py
my_collection = cript.Collection(
    project=my_project,
    name="Simulation Tutorial",
)
my_collection.save()
```

# Create an Experiment node

```py
my_experiment = cript.Experiment(
    collection=my_collection,
    name="Bulk simulation of polystyrene"
)
my_experiment.save()
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
my_python_config = cript.SoftwareConfiguration(software=python)
my_rdkit_config = cript.SoftwareConfiguration(software=rdkit)
my_stage_config = cript.SoftwareConfiguration(software=stage)

# create a software configuration node with a child Algorithm node
my_openmm_config = cript.SoftwareConfiguration(
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
my_packmol_config = cript.SoftwareConfiguration(
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

!!! note "Allowed"
    - The allowed <a href="../../subobjects/algorithm" target="_blank">`Algorithm`</a> keys are listed under <a href="https://criptapp.org/keys/algorithm-key/" target="_blank">algorithm keys</a> in the CRIPT controlled vocabulary.
    - The allowed <a href="../../subobjects/parameter" target="_blank">`Parameter`</a> keys are listed under <a href="https://criptapp.org/keys/parameter-key/" target="_blank">parameter keys</a> in the CRIPT controlled vocabulary.


# Create Computations

Now that we've created some <a href="../../subobjects/software_configuration" target="_blank">`SoftwareConfiguration`</a> nodes, we can used them to build full <a href="../../nodes/computation" target="_blank">`Computation`</a> nodes. Note that each <a href="../../nodes/computation" target="_blank">`Computation`</a> node is nested under a specific <a href="../../nodes/experiment" target="_blank">`Experiment`</a>.

In some cases, we may also want to add <a href="../../subobjects/condition" target="_blank">`Condition`</a> nodes to our computation, to specify the conditions at which the computation was carried out. An example of this is shown below.

```py
# create a Computation node for initialization
my_initialization = cript.Computation(
    experiment = my_experiment,
    name = "Initial snapshot and force-field generation",
    type = "initialization",
    software_configurations = [
        my_python_config,
        my_rdkit_config,
        my_stage_config,
        my_packmol_config,
        my_openmm_config,
    ]
)
my_initialization.save()

# create a Computation node for equilibration
my_equilibration = cript.Computation(
    experiment = my_experiment,
    name = "Equilibrate data prior to measurement",
    type = "MD",
    software_configurations = [my_python_config, my_openmm_config],
    conditions = [
        cript.Condition(key="time_duration", value=100.0, unit="ns"),
        cript.Condition(key="temperature", value=450.0, unit="K"),
        cript.Condition(key="pressure", value=1.0, unit="bar"),
        cript.Condition(key="number", value=31),
    ],
    prerequisite_computation = my_initialization,
)
my_equilibration.save()

# create a Computation node for a bulk simulation
my_bulk = cript.Computation(
    experiment = my_experiment,
    name = "Bulk simulation for measurement",
    type = "MD",
    software_configurations = [my_python_config, my_openmm_config],
    conditions = [
        cript.Condition(key="time_duration", value=50.0, unit="ns"),
        cript.Condition(key="temperature", value=450.0, unit="K"),
        cript.Condition(key="pressure", value=1.0, unit="bar"),
        cript.Condition(key="number", value=31),
    ],
    prerequisite_computation = my_equilibration,
)
my_bulk.save()

# create a Computation node for analysis
my_analysis = cript.Computation(
        experiment = my_experiment,
        name = "Density analysis",
        type = "analysis",
        software_configurations = [my_python_config],
        prerequisite_computation = my_bulk,
)
my_analysis.save()
```

!!! note "Computation types"
    The allowed <a href="../../nodes/computation" target="_blank">`Computation`</a> types are listed under <a href="https://criptapp.org/keys/computation-type/" target="_blank">computation types</a> in the CRIPT controlled vocabulary.

!!! note "Condition keys"
    The allowed <a href="../../subobjects/condition" target="_blank">`Condition`</a> keys are listed under <a href="https://criptapp.org/keys/condition-key/" target="_blank">condition keys</a> in the CRIPT controlled vocabulary.


# Create and Upload <a href="../../nodes/file" target="_blank">`File`</a> nodes

New we'd like to upload files associated with our simulation. First, we'll instantiate our <a href="../../nodes/file" target="_blank">`File`</a> nodes under a specific project.

```py
my_packing_file = cript.File(project=my_project, source="path/to/local/packing_file")
my_forcefield_file = cript.File(project=my_project, source="path/to/local/forcefield_file")
my_snap_file = cript.File(project=my_project, source="path/to/local/snap_file")
my_final_file = cript.File(project=my_project, source="path/to/local/final_file")

my_packing_file.save()
my_forcefield_file.save()
my_snap_file.save()
my_final_file.save()
```

!!! note
    The `source` field should point to a file on your local filesystem.

!!! info
    - You will be prompted to click a link to obtain an authorization code for uploading this file to the CRIPT file storage client. Copy and paste the code obtained from this link into the terminal to save the file.
    - Depending on the file size, there could be a delay while file is being uploaded to CRIPT.

# Create a <a href="../../nodes/data" target="_blank">`Data`</a> node

Next, we'll create a <a href="../../nodes/data" target="_blank">`Data`</a> node which helps organize our <a href="../../nodes/file" target="_blank">`File`</a> nodes and links back to our <a href="../../nodes/computation" target="_blank">`Computation`</a> objects.

```py
my_packing_data = cript.Data(
    experiment = my_experiment,
    name = "Loosely packed chains",
    type = "computation_config",
    files = [my_packing_file],
    computations = [my_initialization],
    notes = "PDB file without topology describing an initial system.",
)
my_packing_data.save()

my_forcefield_data = cript.Data(
    experiment = my_experiment,
    name = "OpenMM forcefield",
    type = "computation_forcefield",
    files = [my_forcefield_file],
    computations = [my_initialization],
    notes = "Full forcefield definition and topology.",
)
my_forcefield_data.save()

my_equi_snap = cript.Data(
    experiment = my_experiment,
    name = "Equilibrated simulation snapshot",
    type = "computation_config",
    files = [my_snap_file],
    computations = [my_equilibration],
)
my_equi_snap.save()

my_final_data = cript.Data(
    experiment = my_experiment,
    name = "Logged volume during simulation",
    type = "+raw_data",
    files = [my_final_file],
    computations = [my_bulk],
)
my_final_data.save()
```

!!! note "Data types"
    The allowed <a href="../../nodes/data" target="_blank">`Data`</a> types are listed under the <a href="https://criptapp.org/keys/data-type/" target="_blank">data types</a> in the CRIPT controlled vocabulary.


Next, we'll link these <a href="../../nodes/data" target="_blank">`Data`</a> nodes to the appropriate <a href="../../nodes/computation" target="_blank">`Computation`</a> nodes.

```py
my_initialization.update(output_data=[my_packing_data, my_forcefield_data])
my_equilibration.update(
    input_data=[my_packing_data, my_forcefield_data],
    output_data=[my_equi_snap]
)
my_analysis.update(input_data=[my_final_data])
my_bulk.update(output_data=[my_final_data])
```

!!! note
    Notice the use of `update()` here, which updates and saves the object in one go.

# Create a <a href="../../nodes/material" target="_blank">`Material`</a> node

Finally, we'll create a virtual material and link it to the <a href="../../nodes/computation" target="_blank">`Computation`</a> nodes that we've built.

```py
my_polystyrene = cript.Material(
    project=my_project,
    name="virtual polystyrene",
)

my_polystyrene.save()
```

Next, let's add some <a href="../../subobjects/identifier" target="_blank">`Identifier`</a> nodes to the <a href="../../nodes/material" target="_blank">`Material`</a> to make it easier to identify and search.

```py
my_names = cript.Identifier(
    key="names",
    value=["poly(styrene)", "poly(vinylbenzene)"],
)

my_bigsmiles = cript.Identifier(
    key="bigsmiles",
    value="[H]{[>][<]C(C[>])c1ccccc1[<]}C(C)CC",
)

my_chem_repeat = cript.Identifier(
    key="chem_repeat",
    value="C8H8",
)

my_polystyrene.add_identifier(my_names)
my_polystyrene.add_identifier(my_chem_repeat)
my_polystyrene.add_identifier(my_bigsmiles)

my_polystyrene.save()
```

!!! note "Identifier keys"
    The allowed <a href="../../subobjects/identifier" target="_blank">`Identifier`</a> keys are listed in the <a href="https://criptapp.org/keys/material-identifier-key/" target="_blank">material identifier keys</a> in the CRIPT controlled vocabulary.

Let's also add some <a href="../../subobjects/property" target="_blank">`Property`</a> nodes to the <a href="../../nodes/material" target="_blank">`Material`</a>, which represent its physical or virtual (in the case of a simulated material) properties.

```py
my_phase = cript.Property(key="phase", value="solid")
my_color = cript.Property(key="color", value="white")

my_polystyrene.add_property(my_phase)
my_polystyrene.add_property(my_color)

my_polystyrene.save()
```

!!! note "Material property keys"
    The allowed material <a href="../../subobjects/property" target="_blank">`Property`</a> keys are listed in the <a href="https://criptapp.org/keys/material-property-key/" target="_blank">material property keys</a> in the CRIPT controlled vocabulary.


Finally, we'll create a <a href="../../subobjects/computational_forcefield" target="_blank">`ComputationalForcefield`</a> node and link it to the <a href="../../nodes/material" target="_blank">`Material`</a>.

```py
my_forcefield = cript.ComputationalForcefield(
    key="opls_aa",
    building_block="atom",
    source="Custom determination via STAGE",
    data=my_forcefield_data,
)

my_polystyrene.computational_forcefield = my_forcefield
my_polystyrene.save()
```

!!! note "Computational forcefield keys"
    The allowed <a href="../../subobjects/computational_forcefield" target="_blank">`ComputationalForcefield`</a> keys are listed under the <a href="https://criptapp.org/keys/computational-forcefield-key/" target="_blank">computational forcefield keys</a> in the CRIPT controlled vocabulary.

