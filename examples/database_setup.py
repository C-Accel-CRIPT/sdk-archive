import cript as C

# Connect to database
db_username = "DW_cript"
db_password = "YXMaoE1"
db_project = "cript_testing"
db_database = "test"

db = C.CriptDB(db_username, db_password, db_project, db_database)

# Generate your User node
user_node = C.User(
    name="Dylan Walsh",
    email="dylanwal@mit.edu",
    organization="Mass. Institute of Technology",
    position="Postdoc"
)
db.save(user_node)

#####################################################
new_group = C.Group(
    name="CRIPT_development_team"
)
db.save(new_group)

new_group = C.Group(
    name="Mass. Institute of Technology"
)
db.save(new_group)

new_group = C.Group(
    name="Brad Olsen Research Group",
    website="https://olsenlab.mit.edu/"
)
db.save(new_group)

new_group = C.Group(
    name="Klavs Jensen Research Group",
    website="https://jensenlab.mit.edu/"
)
db.save(new_group)

new_group = C.Group(
    name="CRIPT_community"
)
db.save(new_group)

#####################################################

collection = C.Collection("Tutorial Examples")
db.save(collection, new_group)

expt = C.Experiment("Anionic Polymerization of Styrene with SecBuLi")
db.save(expt, collection)

inventory = C.Inventory("Tutorial Materials")
db.save(inventory, collection)

mat_styrene = C.Material(
    iden=C.Iden(
        name="styrene",
        names=["vinylbenzene", "phenylethylene", "ethenylbenzene"],
        chem_formula="C8H8",
        smiles="C=Cc1ccccc1",
        cas="100-42-5",
        pubchem_cid="7501",
        inchi_key="PPBRXRYQALVLMV-UHFFFAOYSA-N"
    ),
    prop=[C.Prop(key="phase", value="liquid"),
          C.Prop(key="color", value="colorless"),
          C.Prop(key="molar_mass", value=104.15 * C.Unit("g/mol"), method="prescribed"),
          C.Prop(key="density", value=0.906 * C.Unit("g/ml"),
                 cond=[C.Cond(key="temp", value=25 * C.Unit("degC"))]
                 ),
          C.Prop(key="bp", value=145 * C.Unit("degC"),
                 cond=[C.Cond(key="pressure", value=1 * C.Unit("atm"))]
                 ),
          C.Prop(key="mp", value=-30 * C.Unit("degC"),
                 cond=[C.Cond(key="pressure", value=1 * C.Unit("bar"))]
                 )
          ],
    keywords=["styrene"],
    storage=[
        C.Cond(key="temp", value=-20 * C.Unit("degC")),
        C.Cond(key="atm", value="argon")
    ]
)

mat_toluene = C.Material(
    iden=C.Iden(
        name="toluene",
        names=["methylbenzene"],
        chem_formula="C7H8",
        smiles="Cc1ccccc1",
        cas="108-88-3",
        pubchem_cid="1140",
        inchi_key="YXFVVABEGXRONW-UHFFFAOYSA-N"
    ),
    prop=[C.Prop(key="phase", value="liquid"),
          C.Prop(key="color", value="colorless"),
          C.Prop(key="molar_mass", value=92.141 * C.Unit("g/mol"), method="prescribed"),
          C.Prop(key="density", value=0.87 * C.Unit("g/ml"),
                 cond=[C.Cond(key="temp", value=20 * C.Unit("degC"))]
                 ),
          C.Prop(key="bp", value=111 * C.Unit("degC"),
                 cond=[C.Cond(key="pressure", value=1 * C.Unit("atm"))]
                 ),
          C.Prop(key="mp", value=-95 * C.Unit("degC"),
                 cond=[C.Cond(key="pressure", value=1 * C.Unit("bar"))]
                 ),
          C.Prop(key="solubility", value=0.52 * C.Unit("g/L"),
                 cond=[
                     C.Cond(key="temp", value=20 * C.Unit("degC")),
                     C.Cond(key="solvent", value="water")
                 ]
                 ),
          ])

mat_thf = C.Material(
    iden=C.Iden(
        name="tetrahydrofuran",
        names=["oxolane", "1,4-epoxybutane", "oxacyclopentane", "THF", "butylene oxide", "cyclotetramethylene oxide"],
        chem_formula="C4H8O",
        smiles="C1CCOC1",
        cas="109-99-9",
        pubchem_cid="8028",
        inchi_key="WYURNTSHIVDZCO-UHFFFAOYSA-N"
    ),
    prop=[C.Prop(key="phase", value="liquid"),
          C.Prop(key="color", value="colorless"),
          C.Prop(key="molar_mass", value=72.107 * C.Unit("g/mol"), method="prescribed"),
          C.Prop(key="density", value=0.8876 * C.Unit("g/ml"),
                 cond=[C.Cond(key="temp", value=20 * C.Unit("degC"))]
                 ),
          C.Prop(key="bp", value=66 * C.Unit("degC"),
                 cond=[C.Cond(key="pressure", value=1 * C.Unit("atm"))]
                 ),
          C.Prop(key="mp", value=-108 * C.Unit("degC"),
                 cond=[C.Cond(key="pressure", value=1 * C.Unit("bar"))]
                 ),
          C.Prop(key="solubility", value="miscible",
                 cond=[
                     C.Cond(key="temp", value=20 * C.Unit("degC")),
                     C.Cond(key="solvent", value="water")
                 ]
                 ),
          ])

mat_nBuOH = C.Material(
    iden=C.Iden(
        name="1-butanol",
        names=["n-butanol", "n-butyl alcohol", "1-butyl alcohol"],
        chem_formula="C4H10O",
        smiles="OCCCC",
        cas="71-36-3",
        pubchem_cid="263",
        inchi_key="LRHPLDYGYMQRHN-UHFFFAOYSA-N"
    ),
    prop=[C.Prop(key="phase", value="liquid"),
          C.Prop(key="color", value="colorless"),
          C.Prop(key="molar_mass", value=74.123 * C.Unit("g/mol"), method="prescribed"),
          C.Prop(key="density", value=0.81 * C.Unit("g/ml"),
                 cond=[C.Cond(key="temp", value=20 * C.Unit("degC"))]
                 ),
          C.Prop(key="bp", value=117.7 * C.Unit("degC"),
                 cond=[C.Cond(key="pres", value=1 * C.Unit("atm"))]
                 ),
          C.Prop(key="mp", value=-89.8 * C.Unit("degC"),
                 cond=[C.Cond(key="pres", value=1 * C.Unit("bar"))]
                 ),
          C.Prop(key="solubility", value=73 * C.Unit("g/L"),
                 cond=[
                     C.Cond(key="temp", value=25 * C.Unit("degC")),
                     C.Cond(key="solvent", value="water")
                 ]
                 ),
          ])

mat_MeOH = C.Material(
    iden=C.Iden(
        name="Methanol",
        names=["Methyl alcohol", "CH3OH", "MeOH"],
        chem_formula="CH4O",
        smiles="CO",
        cas="67-56-1",
        pubchem_cid="887",
        inchi_key="OKKJLVBELUTLKV-UHFFFAOYSA-N"
    ),
    prop=[C.Prop(key="phase", value="liquid"),
          C.Prop(key="color", value="colorless"),
          C.Prop(key="molar_mass", value=32.04 * C.Unit("g/mol"), method="prescribed"),
          C.Prop(key="density", value=0.792 * C.Unit("g/ml"),
                 cond=[C.Cond(key="temp", value=20 * C.Unit("degC"))]
                 ),
          C.Prop(key="bp", value=64.7 * C.Unit("degC"),
                 cond=[C.Cond(key="pres", value=1 * C.Unit("atm"))]
                 ),
          C.Prop(key="mp", value=-97.6 * C.Unit("degC"),
                 cond=[C.Cond(key="pres", value=1 * C.Unit("bar"))]
                 ),
          C.Prop(key="solubility", value="miscible",
                 cond=[
                     C.Cond(key="temp", value=25 * C.Unit("degC")),
                     C.Cond(key="solvent", value="water")
                 ]
                 ),
          ])

mat_cHex = C.Material(
    iden=C.Iden(
        name="Cyclohexane",
        chem_formula="C6H12",
        smiles="C1CCCCC1",
        cas="110-82-7",
        pubchem_cid="8078",
        inchi_key="XDTMQSROBMDMFD-UHFFFAOYSA-N"
    ),
    prop=[C.Prop(key="phase", value="liquid"),
          C.Prop(key="color", value="colorless"),
          C.Prop(key="molar_mass", value=84.162 * C.Unit("g/mol"), method="prescribed"),
          C.Prop(key="density", value=0.7739 * C.Unit("g/ml"),
                 cond=[C.Cond(key="temp", value=20 * C.Unit("degC"))]
                 ),
          C.Prop(key="bp", value=80.74 * C.Unit("degC"),
                 cond=[C.Cond(key="pres", value=1 * C.Unit("atm"))]
                 ),
          C.Prop(key="mp", value=6.47 * C.Unit("degC"),
                 cond=[C.Cond(key="pres", value=1 * C.Unit("bar"))]
                 ),
          C.Prop(key="solubility", value="immiscible",
                 cond=[
                     C.Cond(key="temp", value=25 * C.Unit("degC")),
                     C.Cond(key="solvent", value="water")
                 ]
                 ),
          ])

mat_sBuLi = C.Material(
    iden=C.Iden(
        name="sec-butyllithium",
        names=["butan-2-yllithium", "sBuLi", "secBuLi", "s-butyllithium"],
        chem_formula="C4H9Li",
        smiles="[Li]C(C)CC",
        cas="598-30-1",
        inchi_key="VATDYQWILMGLEW-UHFFFAOYSA-N"
    ),
    prop=[C.Prop(key="molar_mass", value=64.06 * C.Unit("g/mol"), method="prescribed")
          ])

db.save(mat_styrene, [expt, inventory])
db.save(mat_toluene, [expt, inventory])
db.save(mat_thf, [expt, inventory])
db.save(mat_nBuOH, [expt, inventory])
db.save(mat_MeOH, [expt, inventory])
db.save(mat_cHex, [expt, inventory])
db.save(mat_sBuLi, [expt, inventory])

mat_solution = C.Material(
    name="SecBuLi solution 1.4M cHex",
    iden=[mat_cHex, mat_sBuLi],
    prop=[
        C.Prop(key="phase", value="liquid"),
        C.Prop(key="density", value=0.769 * C.Unit("g/ml"),
               cond=C.Cond(key="pres", value=1 * C.Unit("bar"))
               ),
        C.Prop(mat_id=2, key="molar_conc", value=1.4 * C.Unit("M"))
    ],
    storage=[
        C.Cond(key="temp", value=2 * C.Unit("degC")),
        C.Cond(key="atm", value="argon")
    ]
)

db.save(mat_solution, [expt, inventory])

########################################################################


ingr = [
    C.Ingr(mat_id=expt.get("SecBuLi solution"), type_="initiator", qty=C.Qty(0.17, C.Unit("ml"))),
    C.Ingr(mat_id=inventory.get("toluene"), type_="solvent", qty=C.Qty(10, C.Unit("ml"))),
    C.Ingr(mat_id=mat_styrene, type_="monomer", qty=C.Qty(0.455, C.Unit("g"))),
    C.Ingr(mat_id=mat_nBuOH, type_="quench", qty=C.Qty(5, "Eq", mat_id="secBuLi")),
    C.Ingr(mat_id=mat_MeOH, type_="workup", qty=C.Qty(100, C.Unit("ml")))
]

# Generate node
process = C.Process(
    name="Anionic of Styrene",
    ingr=ingr,
    procedure="In an argon filled glovebox, a round bottom flask was filled with 216 ml of dried toluene. The "
              "solution of secBuLi (3 ml, 3.9 mmol) was added next, followed by styrene (22.3 g, 176 mmol) to "
              "initiate the polymerization. The reaction mixture immediately turned orange. After 30 min, "
              "the reaction was quenched with the addition of 3 ml of methanol. The polymer was isolated by "
              "precipitation in methanol 3 times and dried under vacuum.",
    cond=[
        C.Cond("temp", 25, C.Unit("degC")),
        C.Cond("time", 60, C.Unit("min"))
    ],
    prop=[
        C.Prop("yield_mass", 0.47, C.Unit("g"), 0.02, method="scale")
    ],
    keywords=["polymerization", "living_poly", "anionic", "solution"]
)

db.save(process, expt)

###########################################################

# sec_data = C.Data(
#
# )


mat_poly = C.Material(
    iden=C.Iden(
        name="polystyrene",
        names=["poly(styrene)", "poly(vinylbenzene)"],
        chem_repeat="C8H8",
        bigsmiles="[H]{[>][<]C(C[>])c1ccccc1[<]}C(C)CC",
        cas="100-42-5"
    ),
    c_process=process,
    prop=[
        C.Prop(key="phase", value="solid"),
        C.Prop(key="color", value="white"),
        C.Prop(key="m_n", method="nmr", value=4800, uncer=400 * C.Unit("g/mol")),
        C.Prop(key="m_n", method="sec", value=5200, uncer=100 * C.Unit("g/mol")),
        C.Prop(key="d", method="sec", value=1.03, uncer=0.02)
    ]
)

db.save(mat_poly, expt)
