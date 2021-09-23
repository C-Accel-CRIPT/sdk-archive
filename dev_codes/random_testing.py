from cript import *


db_username = "DW_cript"
db_password = "YXMaoE1"
db_project = "cript_testing"
db_database = "test"
user = "dylanwal@mit.edu"
db = CriptDB(db_username, db_password, db_project, db_database, user)

from src import tutorial_data_part2
sec_data_path = tutorial_data_part2["polystyrene_sec"]["path"]
cal_path = tutorial_data_part2["sec_calibration_curve"]["path"]
nmr1h_path = tutorial_data_part2["polystyrene_1hnmr"]["path"]

sec_data = Data(
    name="Crude SEC of polystyrene",
    type_="sec_trace",
    file=File(sec_data_path),
    sample_prep="5 mg of polymer in 1 ml of THF, filtered 0.45um pores.",
    cond=[
        Cond("temp", 30 * Unit("degC")),
        Cond("time", 60 * Unit("min")),
        Cond("+flow_rate", 1 * Unit("ml/min"))
    ],
    calibration=File(cal_path)
)

expt_doc = db.view(Experiment)
expt = load(expt_doc[0])
a = db.view(expt.c_material[0]["uid"])
b = load(a)

process = Process(
    name="Anionic of Styrene",
    ingr=[
        Ingr(expt.get("SecBuLi solution 1.4M cHex"), 0.017 * Unit("ml"), "initiator", {"mat_id": "secBuLi"}),
        Ingr(expt.get("toluene"), 10 * Unit("ml"), "solvent"),
        Ingr(expt.get("styrene"), 0.455 * Unit("g"), "monomer"),
        Ingr(expt.get("1BuOH"), 5, "quench", {"eq_mat": "SecBuLi solution"}),
        Ingr(expt.get("MeOH"), 100 * Unit("ml"), "workup")
    ],
    procedure="In an argon filled glovebox, a round bottom flask was filled with 216 ml of dried toluene. The "
              "solution of secBuLi (3 ml, 3.9 mmol) was added next, followed by styrene (22.3 g, 176 mmol) to "
              "initiate the polymerization. The reaction mixture immediately turned orange. After 30 min, "
              "the reaction was quenched with the addition of 3 ml of methanol. The polymer was isolated by "
              "precipitation in methanol 3 times and dried under vacuum.",
    cond=[
        Cond("temp", 25 * Unit("degC")),
        Cond("time", 60 * Unit("min")),
    ],
    prop=[
        Prop("yield_mass", 0.47 * Unit("g"), 0.02 * Unit("g"), method="scale")
    ],
    keywords=["polymerization", "living_poly", "anionic", "solution"]
)

print("hi")
