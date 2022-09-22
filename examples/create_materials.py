import cript as c


def define_materials(project: c.Project) -> list[c.Material]:
    water = c.Material(
        project=project,
        group=project.group,
        name="water",
        identifiers=[
            c.Identifier("preferred_name", "water"),
            c.Identifier("names", ["h2o", "dihydrogen oxide"]),
            c.Identifier("cas", "7732-18-5"),
            c.Identifier("smiles", "O"),
            c.Identifier("chem_formula", "H2O"),
            c.Identifier("pubchem_cid", 962),
            c.Identifier("inchi_key", "XLYOFNOQVPJJNP-UHFFFAOYSA-N"),
        ],
        properties=[
            c.Property(key="phase", value="liquid"),
            c.Property(key="color", value="colorless"),
            c.Property(key="molar_mass", value=18.015, unit="g/mol", method="prescribed"),
            c.Property(key="density", value=1.0, unit="g/ml",
                       conditions=[c.Condition(key="temperature", value=4, unit="degC")]
                       ),
            c.Property(key="+temp_boiling", value=100, unit="degC",
                       conditions=[c.Condition(key="pressure", value=1, unit="atm")]
                       ),
            c.Property(key="temp_melt", value=0, unit="degC",
                       conditions=[c.Condition(key="pressure", value=1, unit="bar")]
                       )
        ]
    )

    dueterated_chloroform = c.Material(
        project=project,
        group=project.group,
        name="deuterated chloroform",
        identifiers=[
            c.Identifier("preferred_name", "deuterated chloroform"),
            c.Identifier("names", ["chloroform-d", "deuterochloroform", "trichloro(deuterio)methane"]),
            c.Identifier("cas", "865-49-6"),
            c.Identifier("smiles", "[2H]C(Cl)(Cl)Cl"),
            c.Identifier("chem_formula", "CDCl3"),
            c.Identifier("pubchem_cid", 71583),
            c.Identifier("inchi_key", "HEDRZPFGACZZDS-MICDWDOJSA-N"),
        ],
        properties=[
            c.Property(key="phase", value="liquid"),
            c.Property(key="color", value="colorless"),
            c.Property(key="molar_mass", value=120.384, unit="g/mol", method="prescribed"),
            c.Property(key="density", value=1.5, unit="g/ml",
                       conditions=[c.Condition(key="temperature", value=25, unit="degC")]
                       ),
            c.Property(key="+temp_boiling", value=61, unit="degC",
                       conditions=[c.Condition(key="pressure", value=1, unit="atm")]
                       ),
            c.Property(key="temp_melt", value=-64, unit="degC",
                       conditions=[c.Condition(key="pressure", value=1, unit="bar")]
                       )
        ]
    )

    nitrogen = c.Material(
        project=project,
        group=project.group,
        name="nitrogen",
        identifiers=[
            c.Identifier("preferred_name", "nitrogen"),
            c.Identifier("names", ["N2", "dinitrogen"]),
            c.Identifier("cas", "7727-37-9"),
            c.Identifier("smiles", "N#N"),
            c.Identifier("chem_formula", "N2"),
            c.Identifier("pubchem_cid", 947),
            c.Identifier("inchi_key", "IJGRMHOSHXDMSA-UHFFFAOYSA-N"),
        ],
        properties=[
            c.Property(key="phase", value="gas"),
            c.Property(key="color", value="colorless"),
            c.Property(key="molar_mass", value=28.014, unit="g/mol", method="prescribed"),
            c.Property(key="density", value=1.25, unit="g/l",
                       conditions=[c.Condition(key="temperature", value=4, unit="degC")]
                       ),
            c.Property(key="+temp_boiling", value=77.355, unit="K",
                       conditions=[c.Condition(key="pressure", value=1, unit="atm")]
                       ),
            c.Property(key="temp_melt", value=63.23, unit="K",
                       conditions=[c.Condition(key="pressure", value=1, unit="bar")]
                       )
        ]
    )

    argon = c.Material(
        project=project,
        group=project.group,
        name="Argon",
        identifiers=[
            c.Identifier("preferred_name", "argon"),
            c.Identifier("names", ["Ar"]),
            c.Identifier("cas", "7440-37-1"),
            c.Identifier("smiles", "Ar"),
            c.Identifier("chem_formula", "Ar"),
            c.Identifier("pubchem_cid", 23968),
            c.Identifier("inchi_key", "XKRFYHLGVUSROY-UHFFFAOYSA-N"),
        ],
        properties=[
            c.Property(key="phase", value="gas"),
            c.Property(key="color", value="colorless"),
            c.Property(key="molar_mass", value=39.95, unit="g/mol", method="prescribed"),
            c.Property(key="density", value=1.784, unit="g/l",
                       conditions=[
                           c.Condition(key="temperature", value=0, unit="degC"),
                           c.Condition(key="pressure", value=1, unit="bar")
                       ]
                       ),
            c.Property(key="+temp_boiling", value=87.3, unit="K",
                       conditions=[c.Condition(key="pressure", value=1, unit="atm")]
                       ),
            c.Property(key="temp_melt", value=83.81, unit="K",
                       conditions=[c.Condition(key="pressure", value=1, unit="bar")]
                       )
        ]
    )

    styrene = c.Material(
        project=project,
        group=project.group,
        name="styrene",
        identifiers=[
            c.Identifier("preferred_name", "styrene"),
            c.Identifier("names", ["vinylbenzene", "phenylethylene", "ethenylbenzene"]),
            c.Identifier("cas", "100-42-5"),
            c.Identifier("smiles", "C=Cc1ccccc1"),
            c.Identifier("chem_formula", "C8H8"),
            c.Identifier("pubchem_cid", 7501),
            c.Identifier("inchi_key", "PPBRXRYQALVLMV-UHFFFAOYSA-N"),
        ],
        properties=[
            c.Property(key="phase", value="liquid"),
            c.Property(key="color", value="colorless"),
            c.Property(key="molar_mass", value=104.15, unit="g/mol", method="prescribed"),
            c.Property(key="density", value=0.906, unit="g/ml",
                       conditions=[c.Condition(key="temperature", value=25, unit="degC")]
                       ),
            c.Property(key="+temp_boiling", value=145, unit="degC",
                       conditions=[c.Condition(key="pressure", value=1, unit="atm")]
                       ),
            c.Property(key="temp_melt", value=-30, unit="degC",
                       conditions=[c.Condition(key="pressure", value=1, unit="bar")]
                       )
        ],
        keywords=["styrene"],
        notes=""
    )

    toluene = c.Material(
        project=project,
        group=project.group,
        name="toluene",
        identifiers=[
            c.Identifier("preferred_name", "toluene"),
            c.Identifier("names", ["methylbenzene"]),
            c.Identifier("cas", "108-88-3"),
            c.Identifier("smiles", "Cc1ccccc1"),
            c.Identifier("chem_formula", "C7H8"),
            c.Identifier("pubchem_cid", 1140),
            c.Identifier("inchi_key", "YXFVVABEGXRONW-UHFFFAOYSA-N"),
        ],
        properties=[
            c.Property(key="phase", value="liquid"),
            c.Property(key="color", value="colorless"),
            c.Property(key="molar_mass", value=92.141, unit="g/mol", method="prescribed"),
            c.Property(key="density", value=0.87, unit="g/ml",
                       conditions=[c.Condition(key="temperature", value=25, unit="degC")]
                       ),
            c.Property(key="+temp_boiling", value=111, unit="degC",
                       conditions=[c.Condition(key="pressure", value=1, unit="atm")]
                       ),
            c.Property(key="temp_melt", value=-95, unit="degC",
                       conditions=[c.Condition(key="pressure", value=1, unit="bar")]
                       ),
            c.Property(key="solubility", value=0.52, unit="g/L",
                       conditions=[
                           c.Condition(key="temperature", value=20, unit="degC"),
                           #c.Condition(key="temperature", value=water),
                       ]
                       )
        ]
    )

    thf = c.Material(
        project=project,
        group=project.group,
        name="thf",
        identifiers=[
            c.Identifier("preferred_name", "tetrahydrofuran"),
            c.Identifier("names", ["oxolane", "1,4-epoxybutane", "oxacyclopentane", "THF", "butylene oxide",
                                   "cyclotetramethylene oxide"]),
            c.Identifier("cas", "109-99-9"),
            c.Identifier("smiles", "C1CCOC1"),
            c.Identifier("chem_formula", "C4H8O"),
            c.Identifier("pubchem_cid", 8028),
            c.Identifier("inchi_key", "WYURNTSHIVDZCO-UHFFFAOYSA-N"),
        ],
        properties=[
            c.Property(key="phase", value="liquid"),
            c.Property(key="color", value="colorless"),
            c.Property(key="molar_mass", value=72.107, unit="g/mol", method="prescribed"),
            c.Property(key="density", value=0.8876, unit="g/ml",
                       conditions=[c.Condition(key="temperature", value=20, unit="degC")]
                       ),
            c.Property(key="+temp_boiling", value=66, unit="degC",
                       conditions=[c.Condition(key="pressure", value=1, unit="atm")]
                       ),
            c.Property(key="temp_melt", value=-108, unit="degC",
                       conditions=[c.Condition(key="pressure", value=1, unit="bar")]
                       ),
            c.Property(key="+solubility", value=-1, unit="g/ml",
                       conditions=[
                           c.Condition(key="temperature", value=20, unit="degC"),
                           c.Condition(key="+solvent", material=water),
                       ]
                       )
        ]
    )

    butanol = c.Material(
        project=project,
        group=project.group,
        name="nbutanol",
        identifiers=[
            c.Identifier("preferred_name", "1-butanol"),
            c.Identifier("names", ["n-butanol", "n-butyl alcohol", "1-butyl alcohol", "nBuOH"]),
            c.Identifier("cas", "71-36-3"),
            c.Identifier("smiles", "OCCCC"),
            c.Identifier("chem_formula", "C4H10O"),
            c.Identifier("pubchem_cid", 263),
            c.Identifier("inchi_key", "LRHPLDYGYMQRHN-UHFFFAOYSA-N"),
        ],
        properties=[
            c.Property(key="phase", value="liquid"),
            c.Property(key="color", value="colorless"),
            c.Property(key="molar_mass", value=74.123, unit="g/mol", method="prescribed"),
            c.Property(key="density", value=0.81, unit="g/ml",
                       conditions=[c.Condition(key="temperature", value=20, unit="degC")]
                       ),
            c.Property(key="+temp_boiling", value=117.7, unit="degC",
                       conditions=[c.Condition(key="pressure", value=1, unit="atm")]
                       ),
            c.Property(key="temp_melt", value=-89.9, unit="degC",
                       conditions=[c.Condition(key="pressure", value=1, unit="bar")]
                       )
        ]
    )

    methanol = c.Material(
        project=project,
        group=project.group,
        name="methanol",
        identifiers=[
            c.Identifier("preferred_name", "methanol"),
            c.Identifier("names", ["Methyl alcohol", "CH3OH", "MeOH"]),
            c.Identifier("cas", "67-56-1"),
            c.Identifier("smiles", "CO"),
            c.Identifier("chem_formula", "CH4O"),
            c.Identifier("pubchem_cid", 887),
            c.Identifier("inchi_key", "OKKJLVBELUTLKV-UHFFFAOYSA-N"),
        ],
        properties=[
            c.Property(key="phase", value="liquid"),
            c.Property(key="color", value="colorless"),
            c.Property(key="molar_mass", value=32.0, unit="g/mol", method="prescribed"),
            c.Property(key="density", value=0.792, unit="g/ml",
                       conditions=[c.Condition(key="temperature", value=20, unit="degC")]
                       ),
            c.Property(key="+temp_boiling", value=64.7, unit="degC",
                       conditions=[c.Condition(key="pressure", value=1, unit="atm")]
                       ),
            c.Property(key="temp_melt", value=-97.6, unit="degC",
                       conditions=[c.Condition(key="pressure", value=1, unit="bar")]
                       )
        ]
    )

    secBuLi = c.Material(
        project=project,
        group=project.group,
        name="secBuLi",
        identifiers=[
            c.Identifier("preferred_name", "sec-butyllithium"),
            c.Identifier("names", ["butan-2-yllithium", "sBuLi", "secBuLi", "s-butyllithium"]),
            c.Identifier("cas", "598-30-1"),
            c.Identifier("smiles", "[Li]C(C)CC"),
            c.Identifier("chem_formula", "C4H9Li"),
            c.Identifier("pubchem_cid", 887),
            c.Identifier("inchi_key", "VATDYQWILMGLEW-UHFFFAOYSA-N"),
        ],
        properties=[
            c.Property(key="molar_mass", value=64.06, unit="g/mol", method="prescribed"),
        ]
    )

    secBuLi_solution = c.Material(
        project=project,
        group=project.group,
        name="SecBuLi solution 1.4M cHex",
        components=[secBuLi, toluene],
        identifiers=[
            c.Identifier("preferred_name", "sec-butyllithium"),
            c.Identifier("names", ["butan-2-yllithium", "sBuLi", "secBuLi", "s-butyllithium"]),
            c.Identifier("cas", "598-30-1"),
            c.Identifier("smiles", "[Li]C(C)CC"),
            c.Identifier("chem_formula", "C4H9Li"),
            c.Identifier("pubchem_cid", 887),
            c.Identifier("inchi_key", "VATDYQWILMGLEW-UHFFFAOYSA-N"),
        ],
        properties=[
            c.Property(key="phase", value="solution"),
            c.Property(key="density", value=0.769, unit="g/ml",
                       conditions=[c.Condition(key="pressure", value=1, unit="bar")]
                       ),
            c.Property(key="conc_molar", value=1.4, unit="M", components=[secBuLi], components_relative=[toluene])
        ]
    )

    return [water, dueterated_chloroform, nitrogen, argon, styrene, toluene, thf, butanol, methanol, secBuLi,
            secBuLi_solution]


def main2():
    api = c.APILocal(folder="database")

    # load existing group/project
    group = api.get("9894a1f1-8297-45d7-a853-0c386dfe3fa9")
    project = api.get("673c1941-06d9-4fb4-bf4b-eae571f822a1")

    materials = define_materials(project)

    for material in materials:
        api.save(material)


def main():
    api = c.APILocal(folder="database")

    # create group/project
    group = c.Group(name="example_group")
    api.save(group)
    project = c.Project(group=group, name="testing_project")
    api.save(project)

    materials = define_materials(project)

    for material in materials:
        api.save(material)


if __name__ == "__main__":
    main()
    # main2()
