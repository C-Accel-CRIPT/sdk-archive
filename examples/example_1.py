"""
Anionic Polymerization of styrene


"""
import cript as c


# Permission and Organization nodes
user_node = c.User(
    username="Dylan Walsh",
    email="dylanwal@cript.edu",
    organization="Mass. Institute of Technology",
    position="Postdoc",
    orcid_id=""
)

group = c.Group(name=__file__, users=[user_node])
collection = c.Collection(group=group, name="Tutorial Examples")
expt = c.Experiment(group=group, name="Anionic Polymerization of Styrene with SecBuLi", collection=collection)
collection.experiments = [expt]

from create_materials import define_materials
materials = define_materials(group)

inventory = c.Inventory(group=group, name="Tutorial Materials", materials=materials)

###########################################################

ingr_secBuLi = c.Ingredient(material=inventory["secBuLi"], quantities= None, keyword="initiator")  # {"mat_id": "secBuLi"}
ingr_tol = c.Ingredient(material=inventory["toluene"], keyword="solvent",
                        quantities=[c.Quantity(key="volume", value=10, unit="ml")])
ingr_st = c.Ingredient(material=inventory["styrene"], quantities=[c.Quantity(key="mass", value=0.455, unit="g")],
                       keyword="monomer")
ingr_meoh = c.Ingredient(material=inventory["methanol"], quantities=None,
                       keyword="workup")  # 5, "quench", {"eq_mat": "SecBuLi solution"}
ingr_meoh2 = c.Ingredient(material=inventory["methanol"], quantities=[c.Quantity(key="volume", value=100, unit="ml")],
                       keyword="quench")

process = c.Process(
    group=group,
    experiment=expt,
    name="Anionic of Styrene",
    ingredients=[ingr_secBuLi, ingr_tol, ingr_st, ingr_meoh, ingr_meoh, ingr_meoh2],
    description="In an argon filled glovebox, a round bottom flask was filled with 216 ml of dried toluene. The "
              "solution of secBuLi (3 ml, 3.9 mmol) was added next, followed by styrene (22.3 g, 176 mmol) to "
              "initiate the polymerization. The reaction mixture immediately turned orange. After 30 min, "
              "the reaction was quenched with the addition of 3 ml of methanol. The polymer was isolated by "
              "precipitation in methanol 3 times and dried under vacuum.",
    conditions=[
        c.Condition(key="temperature", value=25, unit="degC"),
        c.Condition(key="time", value=60, unit="min"),
        c.Condition(key="atm", value=mat_argon)
    ],
    properties=[
        c.Property(key="yield_mass", value=0.47, unit="g", uncertainty=0.02, uncertainty_type="stdev", method="scale")
    ],
    keywords=["polymerization", "living_poly", "anionic", "solution"]
)


###########################################################

sec_data = c.Data(
    group=group,
    experiment=expt,
    name="Crude SEC of polystyrene",
    type="sec_trace",
    files=[
        c.File(group=group, name="sec_data", source="path\\to\\file\\sec.csv"),
        c.File(group=group, name="calibration", source="path\\to\\file\\calibration.xlx", type="calibration")
    ],
    sample_prep="5 mg of polymer in 1 ml of THF, filtered 0.45um pores.",
)

nmr_data = c.Data(
    group=group,
    name="Crude 1H NMR of polystyrene",
    type="nmr_h1",
    sample_prep="10 mg dissolved in 0.5 ml CDCl3",
    files=[c.File(group=group, name="sec_data", source="path\\to\\file\\nmr.csv")],
)

###########################################################

mat_poly = c.Material(
    identifiers=[
        c.Identifier(key="name", value="polystyrene"),
        c.Identifier(key="names", value=["poly(styrene)", "poly(vinylbenzene)"]),
        c.Identifier(key="chem_repeat", value="C8H8"),
        c.Identifier(key="bigsmiles", value="[H]{[>][<]C(C[>])c1ccccc1[<]}C(C)CC"),
        c.Identifier(key="cas", value="100-42-5"),
    ],
    process=process,
    properties=[
        c.Property(key="phase", value="solid"),
        c.Property(key="color", value="white"),
        c.Property(key="m_n", method="nmr", value=4800, unit="g/mol", uncer=400, data=nmr_data),
        c.Property(key="m_n", method="sec", value=5200, unit="g/mol", uncer=100, data=sec_data),
        c.Property(key="d", method="sec", value=1.03, uncer=0.02, c_data=sec_data)
    ]
)
