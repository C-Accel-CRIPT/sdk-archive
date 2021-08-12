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
    identifier=C.Iden(
        preferred_name="styrene",
        names=["vinylbenzene", "phenylethylene", "ethenylbenzene"],
        chem_formula="C8H8",
        smiles="C=Cc1ccccc1",
        cas="100-42-5",
        pubchem_cid="7501",
        inchi_key="PPBRXRYQALVLMV-UHFFFAOYSA-N"
    ),
    properties=[C.Prop(key="phase", value="liquid"),
                C.Prop(key="color", value="colorless"),
                C.Prop(key="mw", value=104.15, unit=C.Unit("g/mol"), method="prescribed"),
                C.Prop(key="density", value=0.906, unit=C.Unit("g/ml"),
                       conditions=[C.Cond(key="temp", value=25, unit=C.Unit("degC"))]
                       ),
                C.Prop(key="bp", value=145, unit=C.Unit("degC"),
                       conditions=[C.Cond(key="pressure", value=1, unit=C.Unit("atm"))]
                       ),
                C.Prop(key="mp", value=-30, unit=C.Unit("degC"),
                       conditions=[C.Cond(key="pressure", value=1, unit=C.Unit("bar"))]
                       )
                ],
    keywords=["styrene"],
    storage=[
        C.Cond(key="temp", value=-20, unit=C.Unit("degC")),
        C.Cond(key="atm", value="argon")
    ]
)

mat_toluene = C.Material(
    identifier=C.Iden(
        preferred_name="toluene",
        names=["methylbenzene"],
        chem_formula="C7H8",
        smiles="Cc1ccccc1",
        cas="108-88-3",
        pubchem_cid="1140",
        inchi_key="YXFVVABEGXRONW-UHFFFAOYSA-N"
    ),
    properties=[C.Prop(key="phase", value="liquid"),
                C.Prop(key="color", value="colorless"),
                C.Prop(key="mw", value=92.141, unit=C.Unit("g/mol"), method="prescribed"),
                C.Prop(key="density", value=0.87, unit=C.Unit("g/ml"),
                       conditions=[C.Cond(key="temp", value=20, unit=C.Unit("degC"))]
                       ),
                C.Prop(key="bp", value=111, unit=C.Unit("degC"),
                       conditions=[C.Cond(key="pressure", value=1, unit=C.Unit("atm"))]
                       ),
                C.Prop(key="mp", value=-95, unit=C.Unit("degC"),
                       conditions=[C.Cond(key="pressure", value=1, unit=C.Unit("bar"))]
                       ),
                C.Prop(key="solubility", value=0.52, unit=C.Unit("g/L"),
                       conditions=[
                           C.Cond(key="temp", value=20, unit=C.Unit("degC")),
                           C.Cond(key="solvent", value="water")
                       ]
                       ),
                ])

mat_thf = C.Material(
    identifier=C.Iden(
        preferred_name="tetrahydrofuran",
        names=["oxolane", "1,4-epoxybutane", "oxacyclopentane", "THF", "butylene oxide", "cyclotetramethylene oxide"],
        chem_formula="C4H8O",
        smiles="C1CCOC1",
        cas="109-99-9",
        pubchem_cid="8028",
        inchi_key="WYURNTSHIVDZCO-UHFFFAOYSA-N"
    ),
    properties=[C.Prop(key="phase", value="liquid"),
                C.Prop(key="color", value="colorless"),
                C.Prop(key="mw", value=72.107, unit=C.Unit("g/mol"), method="prescribed"),
                C.Prop(key="density", value=0.8876, unit=C.Unit("g/ml"),
                       conditions=[C.Cond(key="temp", value=20, unit=C.Unit("degC"))]
                       ),
                C.Prop(key="bp", value=66, unit=C.Unit("degC"),
                       conditions=[C.Cond(key="pressure", value=1, unit=C.Unit("atm"))]
                       ),
                C.Prop(key="mp", value=-108, unit=C.Unit("degC"),
                       conditions=[C.Cond(key="pressure", value=1, unit=C.Unit("bar"))]
                       ),
                C.Prop(key="solubility", value="miscible",
                       conditions=[
                           C.Cond(key="temp", value=20, unit=C.Unit("degC")),
                           C.Cond(key="solvent", value="water")
                       ]
                       ),
                ])

mat_nBuOH = C.Material(
    identifier=C.Iden(
        preferred_name="1-butanol",
        names=["n-butanol", "n-butyl alcohol", "1-butyl alcohol"],
        chem_formula="C4H10O",
        smiles="OCCCC",
        cas="71-36-3",
        pubchem_cid="263",
        inchi_key="LRHPLDYGYMQRHN-UHFFFAOYSA-N"
    ),
    properties=[C.Prop(key="phase", value="liquid"),
                C.Prop(key="color", value="colorless"),
                C.Prop(key="mw", value=74.123, unit=C.Unit("g/mol"), method="prescribed"),
                C.Prop(key="density", value=0.81, unit=C.Unit("g/ml"),
                       conditions=[C.Cond(key="temp", value=20, unit=C.Unit("degC"))]
                       ),
                C.Prop(key="bp", value=117.7, unit=C.Unit("degC"),
                       conditions=[C.Cond(key="pressure", value=1, unit=C.Unit("atm"))]
                       ),
                C.Prop(key="mp", value=-89.8, unit=C.Unit("degC"),
                       conditions=[C.Cond(key="pressure", value=1, unit=C.Unit("bar"))]
                       ),
                C.Prop(key="solubility", value=73, unit=C.Unit("g/L"),
                       conditions=[
                           C.Cond(key="temp", value=25, unit=C.Unit("degC")),
                           C.Cond(key="solvent", value="water")
                       ]
                       ),
                ])

mat_MeOH = C.Material(
    identifier=C.Iden(
        preferred_name="Methanol",
        names=["Methyl alcohol", "CH3OH", "MeOH"],
        chem_formula="CH4O",
        smiles="CO",
        cas="67-56-1",
        pubchem_cid="887",
        inchi_key="OKKJLVBELUTLKV-UHFFFAOYSA-N"
    ),
    properties=[C.Prop(key="phase", value="liquid"),
                C.Prop(key="color", value="colorless"),
                C.Prop(key="mw", value=32.04, unit=C.Unit("g/mol"), method="prescribed"),
                C.Prop(key="density", value=0.792, unit=C.Unit("g/ml"),
                       conditions=[C.Cond(key="temp", value=20, unit=C.Unit("degC"))]
                       ),
                C.Prop(key="bp", value=64.7, unit=C.Unit("degC"),
                       conditions=[C.Cond(key="pressure", value=1, unit=C.Unit("atm"))]
                       ),
                C.Prop(key="mp", value=-97.6, unit=C.Unit("degC"),
                       conditions=[C.Cond(key="pressure", value=1, unit=C.Unit("bar"))]
                       ),
                C.Prop(key="solubility", value="miscible",
                       conditions=[
                           C.Cond(key="temp", value=25, unit=C.Unit("degC")),
                           C.Cond(key="solvent", value="water")
                       ]
                       ),
                ])

mat_cHex = C.Material(
    identifier=C.Iden(
        preferred_name="Cyclohexane",
        chem_formula="C6H12",
        smiles="C1CCCCC1",
        cas="110-82-7",
        pubchem_cid="8078",
        inchi_key="XDTMQSROBMDMFD-UHFFFAOYSA-N"
    ),
    properties=[C.Prop(key="phase", value="liquid"),
                C.Prop(key="color", value="colorless"),
                C.Prop(key="mw", value=84.162, unit=C.Unit("g/mol"), method="prescribed"),
                C.Prop(key="density", value=0.7739, unit=C.Unit("g/ml"),
                       conditions=[C.Cond(key="temp", value=20, unit=C.Unit("degC"))]
                       ),
                C.Prop(key="bp", value=80.74, unit=C.Unit("degC"),
                       conditions=[C.Cond(key="pressure", value=1, unit=C.Unit("atm"))]
                       ),
                C.Prop(key="mp", value=6.47, unit=C.Unit("degC"),
                       conditions=[C.Cond(key="pressure", value=1, unit=C.Unit("bar"))]
                       ),
                C.Prop(key="solubility", value="immiscible",
                       conditions=[
                           C.Cond(key="temp", value=25, unit=C.Unit("degC")),
                           C.Cond(key="solvent", value="water")
                       ]
                       ),
                ])

mat_sBuLi = C.Material(
    identifier=C.Iden(
        preferred_name="sec-butyllithium",
        names=["butan-2-yllithium", "sBuLi", "secBuLi", "s-butyllithium"],
        chem_formula="C4H9Li",
        smiles="[Li]C(C)CC",
        cas="598-30-1",
        inchi_key="VATDYQWILMGLEW-UHFFFAOYSA-N"
    ),
    properties=[C.Prop(key="mw", value=64.06, unit=C.Unit("g/mol"), method="prescribed")
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
    identifier=[mat_cHex, mat_sBuLi],
    properties=[
        C.Prop(key="phase", value="liquid"),
        C.Prop(key="density", value=0.769, unit=C.Unit("g/ml"),
               conditions=C.Cond(key="pressure", value=1, unit=C.Unit("bar"))
               ),
        C.Prop(mat_id=2, key="conc", value=1.4, unit=C.Unit("M"))
    ],
    storage=[
        C.Cond(key="temp", value=2, unit=C.Unit("degC")),
        C.Cond(key="atm", value="argon")
    ]
)

db.save(mat_solution, [expt, inventory])

########################################################################


ingr = [
    C.Ingredient(mat_id=expt.get("secBuLi"), type_="initiator", qty=C.Qty(0.17, C.Unit("ml"))),
    C.Ingredient(mat_id=inventory.get("toluene"), type_="solvent", qty=C.Qty(10, C.Unit("ml"))),
    C.Ingredient(mat_id=mat_styrene, type_="monomer", qty=C.Qty(0.455, C.Unit("g"))),
    C.Ingredient(mat_id=mat_nBuOH, type_="quench", qty=C.Qty(5, "Eq", mat_id="secBuLi")),
    C.Ingredient(mat_id=mat_MeOH, type_="workup", qty=C.Qty(100, C.Unit("ml")))
]

# Generate node
process = C.Process(
    name="Anionic of Styrene",
    ingredients=ingr,
    procedure="In an argon filled glovebox, a round bottom flask was filled with 216 ml of dried toluene. The "
              "solution of secBuLi (3 ml, 3.9 mmol) was added next, followed by styrene (22.3 g, 176 mmol) to "
              "initiate the polymerization. The reaction mixture immediately turned orange. After 30 min, "
              "the reaction was quenched with the addition of 3 ml of methanol. The polymer was isolated by "
              "precipitation in methanol 3 times and dried under vacuum.",
    conditions=[
        C.Cond("temp", 25, C.Unit("degC")),
        C.Cond("time", 60, C.Unit("min"))
    ],
    properties=[
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
    identifier=C.Iden(
        preferred_name="polystyrene",
        names=["poly(styrene)", "poly(vinylbenzene)"],
        chem_repeat="C8H8",
        bigsmiles="[H]{[>][<]C(C[>])c1ccccc1[<]}C(C)CC",
        cas="100-42-5"
    ),
    c_process=process,
    properties=[
        C.Prop(key="phase", value="solid"),
        C.Prop(key="color", value="white"),
        C.Prop(key="m_n", method="nmr", value=4800, uncer=400, unit=C.Unit("g/mol")),
        C.Prop(key="m_n", method="sec", value=5200, uncer=100, unit=C.Unit("g/mol")),
        C.Prop(key="d", method="sec", value=1.03, uncer=0.02)
    ]
)

db.save(mat_poly, expt)


