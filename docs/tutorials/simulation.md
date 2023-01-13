# Simulation example workflow

> Refer to [Quickstart](../quickstart.md) for installation instructions.

## Connect to the public API

```py
import cript

host = "criptapp.org"
token = "<your_api_token>"
cript.API(host, token)
```

!!! note
Your API token can be found in the UI under [Account Settings](https://criptapp.org/settings/).

### Create a Project node

```py
proj = cript.Project(name="<your_project_name>")
proj.save()
```

!!! note
Project names are globally unique.

### Create a Collection node

```py
coll = cript.Collection(project=proj, name="Simulation Tutorial")
coll.save()
```

### Create an Experiment node

```py
expt = cript.Experiment(
    collection=coll,
    name="Bulk simulation of polystyrene"
)
expt.save()
```

### Get the relevant Software nodes

```py
python = cript.Software.get(
    name = "python",
    version = "3.9"
)
rdkit = cript.Software.get(
    name = "rdkit",
    version = "2020.9"
)
stage = cript.Software.get(
    name = "stage",
    source = "https://doi.org/10.1021/jp505332p"
)
packmol = cript.Software.get(
    name = "Packmol",
    source = "http://m3g.iqm.unicamp.br/packmol",
    version = "N/A"
)
openmm = cript.Software.get(
    name = "openmm",
    version = "7.5"
)
```

### Create Software Configurations

```py
python_config = cript.SoftwareConfiguration(software=python)
rdkit_config = cript.SoftwareConfiguration(software=rdkit)
stage_config = cript.SoftwareConfiguration(software=stage)
openmm_config = cript.SoftwareConfiguration(
    software = openmm,
    algorithms = [
        cript.Algorithm(key="+energy_minimization", type="initialization")
    ]
)
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

### Create Computations

```py
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

!!! note
Notice the use of `create()` here, which instantiates and saves the object in one go.

### Create and Upload Files

First, we'll instantiate our File nodes.

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

Next, we'll upload the local files by saving the File nodes. Follow all prompts that appear.

```py
packing_file.save()
forcefield_file.save()
snap_file.save()
final_file.save()
```

### Create Data

First, we'll create a few Data nodes.

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

Next, we'll add these to the appropriate Computation nodes.

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

### Create a virtual Material

First, we'll instantiate our Material node:

```py
polystyrene = cript.Material(project=proj, name="Polystyrene")
```

Next, we'll add some Identifiers nodes:

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

... and Property nodes:

```py
phase = cript.Property(key="phase", value="solid")
color = cript.Property(key="color", value="white")

polystyrene.add_property(phase)
polystyrene.add_property(color)
```

Last, we'll create a ComputationalForcefield node and add it to the Material:

```py
forcefield = cript.ComputationalForcefield(
    key = "opls_aa",
    building_block = "atom",
    source = "Custom determination via STAGE",
    data = forcefield_data
)

polystyrene.computational_forcefield = forcefield
polystyrene.save()
```

### Conclusion

You made it! We hope this tutorial has been helpful.

Please let us know how you think it could be improved.
