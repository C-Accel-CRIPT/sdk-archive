from cript import *

# Connect to database
db_username = "DW_cript"
db_password = "YXMaoE1"
db_project = "cript_testing"
db_database = "test"

db = CriptDB(db_username, db_password, db_project, db_database)

# Generate your User node
user_node = User(
    name="Dylan Walsh",
    email="dylanwal@mit.edu",
    organization="Mass. Institute of Technology",
    position="Postdoc"
)

db.save(user_node)

#####################################################
new_group = Group(
    name="CRIPT_development_team"
)
db.save(new_group)

new_group = Group(
    name="Mass. Institute of Technology"
)
db.save(new_group)

new_group = Group(
    name="Brad Olsen Research Group",
    website="https://olsenlab.mit.edu/"
)
db.save(new_group)

new_group = Group(
    name="Klavs Jensen Research Group",
    website="https://jensenlab.mit.edu/"
)
db.save(new_group)

new_group = Group(
    name="CRIPT_community"
)
db.save(new_group)

#####################################################

collection = Collection("Tutorial Examples")
db.save(collection, new_group)

expt = Experiment("Anionic Polymerization of Styrene with SecBuLi")
db.save(expt, collection)

inventory = Inventory("Tutorial Materials")
db.save(inventory, collection)

mat_water = Material(
    iden=Iden(
        name="water",
        names=["h2o", "dihydrogen oxide"],
        chem_formula="H2O",
        smiles="O",
        cas="7732-18-5",
        pubchem_cid="962",
        inchi_key="XLYOFNOQVPJJNP-UHFFFAOYSA-N"
    ),
    prop=[Prop(key="phase", value="liquid"),
          Prop(key="color", value="colorless"),
          Prop(key="molar_mass", value=18.015 * Unit("g/mol"), method="prescribed"),
          Prop(key="density", value=1.0 * Unit("g/ml"),
               cond=[Cond(key="temp", value=4 * Unit("degC"))]
               ),
          Prop(key="bp", value=100 * Unit("degC"),
               cond=[Cond(key="pres", value=1 * Unit("atm"))]
               ),
          Prop(key="mp", value=0 * Unit("degC"),
               cond=[Cond(key="pres", value=1 * Unit("bar"))]
               )
          ],
)

db.save(mat_water, inventory)

mat_cdcl3 = Material(
    iden=Iden(
        name="deuterated chloroform",
        names=["chloroform-d", "deuterochloroform", "trichloro(deuterio)methane"],
        chem_formula="CDCl3",
        smiles="[2H]C(Cl)(Cl)Cl",
        cas="865-49-6",
        pubchem_cid="71583",
        inchi_key="HEDRZPFGACZZDS-MICDWDOJSA-N"
    ),
    prop=[Prop(key="phase", value="liquid"),
          Prop(key="color", value="colorless"),
          Prop(key="molar_mass", value=120.384* Unit("g/mol"), method="prescribed"),
          Prop(key="density", value=1.5 * Unit("g/ml"),
               cond=[Cond(key="temp", value=25 * Unit("degC"))]
               ),
          Prop(key="bp", value=61 * Unit("degC"),
               cond=[Cond(key="pres", value=1 * Unit("bar"))]
               ),
          Prop(key="mp", value=-64 * Unit("degC"),
               cond=[Cond(key="pres", value=1 * Unit("bar"))]
               )
          ],
)

db.save(mat_cdcl3, inventory)


mat_nitrogen = Material(
    iden=Iden(
        name="nitrogen",
        names=["N2", "dinitrogen"],
        chem_formula="N2",
        smiles="N#N",
        cas="7727-37-9",
        pubchem_cid="947",
        inchi_key="IJGRMHOSHXDMSA-UHFFFAOYSA-N"
    ),
    prop=[Prop(key="phase", value="liquid"),
          Prop(key="color", value="colorless"),
          Prop(key="molar_mass", value=28.014 * Unit("g/mol"), method="prescribed"),
          Prop(key="density", value=1.25 * Unit("g/l"),
               cond=[Cond(key="temp", value=4 * Unit("degC"))]
               ),
          Prop(key="bp", value=77.355 * Unit("K"),
               cond=[Cond(key="pres", value=1 * Unit("atm"))]
               ),
          Prop(key="mp", value=63.23 * Unit("K"),
               cond=[Cond(key="pres", value=1 * Unit("bar"))]
               )
          ],
)

db.save(mat_nitrogen, inventory)

mat_argon = Material(
    iden=Iden(
        name="argon",
        names=["Ar"],
        chem_formula="Ar",
        smiles="Ar",
        cas="7440-37-1",
        pubchem_cid="23968",
        inchi_key="XKRFYHLGVUSROY-UHFFFAOYSA-N"
    ),
    prop=[Prop(key="phase", value="gas"),
          Prop(key="color", value="colorless"),
          Prop(key="molar_mass", value=39.95 * Unit("g/mol"), method="prescribed"),
          Prop(key="density", value=1.784 * Unit("g/l"),
               cond=[
                   Cond(key="temp", value=0 * Unit("degC")),
                   Cond(key="pres", value=1 * Unit("bar"))
               ]
               ),
          Prop(key="bp", value=87.3 * Unit("K"),
               cond=[Cond(key="pres", value=1 * Unit("atm"))]
               ),
          Prop(key="mp", value=83.81 * Unit("K"),
               cond=[Cond(key="pres", value=1 * Unit("bar"))]
               )
          ],
)

db.save(mat_argon, inventory)

mat_styrene = Material(
    iden=Iden(
        name="styrene",
        names=["vinylbenzene", "phenylethylene", "ethenylbenzene"],
        chem_formula="C8H8",
        smiles="C=Cc1ccccc1",
        cas="100-42-5",
        pubchem_cid="7501",
        inchi_key="PPBRXRYQALVLMV-UHFFFAOYSA-N"
    ),
    prop=[Prop(key="phase", value="liquid"),
          Prop(key="color", value="colorless"),
          Prop(key="molar_mass", value=104.15 * Unit("g/mol"), method="prescribed"),
          Prop(key="density", value=0.906 * Unit("g/ml"),
               cond=[Cond(key="temp", value=25 * Unit("degC"))]
               ),
          Prop(key="bp", value=145 * Unit("degC"),
               cond=[Cond(key="pres", value=1 * Unit("atm"))]
               ),
          Prop(key="mp", value=-30 * Unit("degC"),
               cond=[Cond(key="pres", value=1 * Unit("bar"))]
               )
          ],
    keywords=["styrene"],
    storage=[
        Cond(key="temp", value=-20 * Unit("degC")),
        Cond(key="atm", value=mat_argon)
    ]
)

mat_toluene = Material(
    iden=Iden(
        name="toluene",
        names=["methylbenzene"],
        chem_formula="C7H8",
        smiles="Cc1ccccc1",
        cas="108-88-3",
        pubchem_cid="1140",
        inchi_key="YXFVVABEGXRONW-UHFFFAOYSA-N"
    ),
    prop=[Prop(key="phase", value="liquid"),
          Prop(key="color", value="colorless"),
          Prop(key="molar_mass", value=92.141 * Unit("g/mol"), method="prescribed"),
          Prop(key="density", value=0.87 * Unit("g/ml"),
               cond=[Cond(key="temp", value=20 * Unit("degC"))]
               ),
          Prop(key="bp", value=111 * Unit("degC"),
               cond=[Cond(key="pres", value=1 * Unit("atm"))]
               ),
          Prop(key="mp", value=-95 * Unit("degC"),
               cond=[Cond(key="pres", value=1 * Unit("bar"))]
               ),
          Prop(key="solubility", value=0.52 * Unit("g/L"),
               cond=[
                   Cond(key="temp", value=20 * Unit("degC")),
                   Cond(key="solvent", value=mat_water)
               ]
               ),
          ])

mat_thf = Material(
    iden=Iden(
        name="tetrahydrofuran",
        names=["oxolane", "1,4-epoxybutane", "oxacyclopentane", "THF", "butylene oxide", "cyclotetramethylene oxide"],
        chem_formula="C4H8O",
        smiles="C1CCOC1",
        cas="109-99-9",
        pubchem_cid="8028",
        inchi_key="WYURNTSHIVDZCO-UHFFFAOYSA-N"
    ),
    prop=[Prop(key="phase", value="liquid"),
          Prop(key="color", value="colorless"),
          Prop(key="molar_mass", value=72.107 * Unit("g/mol"), method="prescribed"),
          Prop(key="density", value=0.8876 * Unit("g/ml"),
               cond=[Cond(key="temp", value=20 * Unit("degC"))]
               ),
          Prop(key="bp", value=66 * Unit("degC"),
               cond=[Cond(key="pres", value=1 * Unit("atm"))]
               ),
          Prop(key="mp", value=-108 * Unit("degC"),
               cond=[Cond(key="pres", value=1 * Unit("bar"))]
               ),
          Prop(key="solubility", value="miscible",
               cond=[
                   Cond(key="temp", value=20 * Unit("degC")),
                   Cond(key="solvent", value=mat_water)
               ]
               ),
          ])

mat_nBuOH = Material(
    iden=Iden(
        name="1-butanol",
        names=["n-butanol", "n-butyl alcohol", "1-butyl alcohol", "nBuOH"],
        chem_formula="C4H10O",
        smiles="OCCCC",
        cas="71-36-3",
        pubchem_cid="263",
        inchi_key="LRHPLDYGYMQRHN-UHFFFAOYSA-N"
    ),
    prop=[Prop(key="phase", value="liquid"),
          Prop(key="color", value="colorless"),
          Prop(key="molar_mass", value=74.123 * Unit("g/mol"), method="prescribed"),
          Prop(key="density", value=0.81 * Unit("g/ml"),
               cond=[Cond(key="temp", value=20 * Unit("degC"))]
               ),
          Prop(key="bp", value=117.7 * Unit("degC"),
               cond=[Cond(key="pres", value=1 * Unit("atm"))]
               ),
          Prop(key="mp", value=-89.8 * Unit("degC"),
               cond=[Cond(key="pres", value=1 * Unit("bar"))]
               ),
          Prop(key="solubility", value=73 * Unit("g/L"),
               cond=[
                   Cond(key="temp", value=25 * Unit("degC")),
                   Cond(key="solvent", value=mat_water)
               ]
               ),
          ])

mat_MeOH = Material(
    iden=Iden(
        name="methanol",
        names=["Methyl alcohol", "CH3OH", "MeOH"],
        chem_formula="CH4O",
        smiles="CO",
        cas="67-56-1",
        pubchem_cid="887",
        inchi_key="OKKJLVBELUTLKV-UHFFFAOYSA-N"
    ),
    prop=[Prop(key="phase", value="liquid"),
          Prop(key="color", value="colorless"),
          Prop(key="molar_mass", value=32.04 * Unit("g/mol"), method="prescribed"),
          Prop(key="density", value=0.792 * Unit("g/ml"),
               cond=[Cond(key="temp", value=20 * Unit("degC"))]
               ),
          Prop(key="bp", value=64.7 * Unit("degC"),
               cond=[Cond(key="pres", value=1 * Unit("atm"))]
               ),
          Prop(key="mp", value=-97.6 * Unit("degC"),
               cond=[Cond(key="pres", value=1 * Unit("bar"))]
               ),
          Prop(key="solubility", value="miscible",
               cond=[
                   Cond(key="temp", value=25 * Unit("degC")),
                   Cond(key="solvent", value=mat_water)
               ]
               ),
          ])

mat_cHex = Material(
    iden=Iden(
        name="cyclohexane",
        chem_formula="C6H12",
        smiles="C1CCCCC1",
        cas="110-82-7",
        pubchem_cid="8078",
        inchi_key="XDTMQSROBMDMFD-UHFFFAOYSA-N"
    ),
    prop=[Prop(key="phase", value="liquid"),
          Prop(key="color", value="colorless"),
          Prop(key="molar_mass", value=84.162 * Unit("g/mol"), method="prescribed"),
          Prop(key="density", value=0.7739 * Unit("g/ml"),
               cond=[Cond(key="temp", value=20 * Unit("degC"))]
               ),
          Prop(key="bp", value=80.74 * Unit("degC"),
               cond=[Cond(key="pres", value=1 * Unit("atm"))]
               ),
          Prop(key="mp", value=6.47 * Unit("degC"),
               cond=[Cond(key="pres", value=1 * Unit("bar"))]
               ),
          Prop(key="solubility", value="immiscible",
               cond=[
                   Cond(key="temp", value=25 * Unit("degC")),
                   Cond(key="solvent", value=mat_water)
               ]
               ),
          ])

mat_sBuLi = Material(
    iden=Iden(
        name="sec-butyllithium",
        names=["butan-2-yllithium", "sBuLi", "secBuLi", "s-butyllithium"],
        chem_formula="C4H9Li",
        smiles="[Li]C(C)CC",
        cas="598-30-1",
        inchi_key="VATDYQWILMGLEW-UHFFFAOYSA-N"
    ),
    prop=[Prop(key="molar_mass", value=64.06 * Unit("g/mol"), method="prescribed")
          ])

db.save(mat_styrene, [expt, inventory])
db.save(mat_toluene, [expt, inventory])
db.save(mat_thf, [expt, inventory])
db.save(mat_nBuOH, [expt, inventory])
db.save(mat_MeOH, [expt, inventory])
db.save(mat_cHex, [expt, inventory])
db.save(mat_sBuLi, [expt, inventory])

mat_solution = Material(
    name="SecBuLi solution 1.4M cHex",
    iden=[mat_cHex, mat_sBuLi],
    prop=[
        Prop(key="phase", value="liquid"),
        Prop(key="density", value=0.769 * Unit("g/ml"),
             cond=Cond(key="pres", value=1 * Unit("bar"))
             ),
        Prop(mat_id=2, key="molar_conc", value=1.4 * Unit("M"))
    ],
    storage=[
        Cond(key="temp", value=2 * Unit("degC")),
        Cond(key="atm", value=mat_argon)
    ]
)

db.save(mat_solution, [expt, inventory])

########################################################################


# Generate node
process = Process(
    name="Anionic of Styrene",
    ingr=Ingr(
        [expt.get("SecBuLi solution 1.4M cHex"), 0.17 * Unit("mol"), "initiator", {"mat_id": "secBuLi"}],
        [expt.get("toluene"), 10 * Unit("ml"), "solvent"],
        [expt.get("styrene"), 0.455 * Unit("g"), "monomer"],
        [expt.get("1BuOH"), 5, "quench", {"eq_mat": "secBuLi"}],
        [expt.get("MeOH"), 100 * Unit("ml"), "workup"]
    ),
    procedure="In an argon filled glovebox, a round bottom flask was filled with 216 ml of dried toluene. The "
              "solution of secBuLi (3 ml, 3.9 mmol) was added next, followed by styrene (22.3 g, 176 mmol) to "
              "initiate the polymerization. The reaction mixture immediately turned orange. After 30 min, "
              "the reaction was quenched with the addition of 3 ml of methanol. The polymer was isolated by "
              "precipitation in methanol 3 times and dried under vacuum.",
    cond=[
        Cond("temp", 25 * Unit("degC")),
        Cond("time", 60 * Unit("min")),
        Cond(key="atm", value=mat_argon)
    ],
    prop=[
        Prop("yield_mass", 0.47 * Unit("g"), 0.02 * Unit("g"), method="scale")
    ],
    keywords=["polymerization", "living_poly", "anionic", "solution"]
)

db.save(process, expt)

###########################################################


sec_data_path = tutorial.tutorial_data_part2["polystyrene_sec"]["path"]
cal_path = tutorial.tutorial_data_part2["sec_calibration_curve"]["path"]
nmr1h_path = tutorial.tutorial_data_part2["polystyrene_1hnmr"]["path"]

sec_data = Data(
    name="Crude SEC of polystyrene",
    _type="sec_trace",
    file=File(sec_data_path),
    sample_prep="5 mg of polymer in 1 ml of THF, filtered 0.45um pores.",
    cond=[
        Cond("temp", 30 * Unit("degC")),
        Cond("time", 60 * Unit("min")),
        Cond("solvent", value=expt.get("THF")),
        Cond("+flow_rate", 1 * Unit("ml/min"))
    ],
    calibration=File(cal_path)
)

nmr_data = Data(
    name="Crude 1H NMR of polystyrene",
    _type="nmr_h1",
    file=File(nmr1h_path),
    cond=[
        Cond("temp", 25 * Unit("degC")),
        Cond("solvent", value=inventory.get("CDCl3")),
    ]
)

db.save(sec_data, expt)
db.save(nmr_data, expt)

###########################################################

mat_poly = Material(
    iden=Iden(
        name="polystyrene",
        names=["poly(styrene)", "poly(vinylbenzene)"],
        chem_repeat="C8H8",
        bigsmiles="[H]{[>][<]C(C[>])c1ccccc1[<]}C(C)CC",
        cas="100-42-5"
    ),
    c_process=process,
    prop=[
        Prop(key="phase", value="solid"),
        Prop(key="color", value="white"),
        Prop(key="m_n", method="nmr", value=4800 * Unit("g/mol"), uncer=400 * Unit("g/mol"), c_data=nmr_data),
        Prop(key="m_n", method="sec", value=5200 * Unit("g/mol"), uncer=100 * Unit("g/mol"), c_data=sec_data),
        Prop(key="d", method="sec", value=1.03, uncer=0.02, c_data=sec_data)
    ]
)

db.save(mat_poly, expt)
