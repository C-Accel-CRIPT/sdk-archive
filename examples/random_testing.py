#from cript import *
import cript as C

db_username = "DW_cript"
db_password = "YXMaoE1"
db_project = "cript_testing"
db_database = "test"
user = "dylanwal@mit.edu"
db = C.CriptDB(db_username, db_password, db_project, db_database, user)

expt_doc = db.view(C.Experiment)

expt = C.load(expt_doc[0])

inv_doc = db.view(C.Inventory)
#
inv = C.load(inv_doc[0])

# ingr = [
#     C.Ingr(expt.get("SecBuLi solution"), C.Qty(0.17 * C.Unit("mol"), mat_uid=1), "initiator"),
#     C.Ingr(expt.get("toluene"), C.Qty(10 * C.Unit("ml")), "solvent"),
#     C.Ingr(expt.get("styrene"), C.Qty(0.455 * C.Unit("g")), "monomer"),
#     C.Ingr(expt.get("nBuOH"), C.Qty(5, equiv="secBuLi"), "quench"),
#     C.Ingr(expt.get("MeOH"), C.Qty(100 * C.Unit("ml")), "workup")
# ]

# ingr = C.Ingr(
#         [expt.get("SecBuLi solution 1.4"), 0.17 * C.Unit("mol"), "initiator", {"mat_id": "secBuLi"}],
#         [expt.get("toluene"), 10 * C.Unit("ml"), "solvent"],
#         [expt.get("styrene"), 0.455 * C.Unit("g"), "monomer"],
#         [expt.get("1BuOH"), 5, "quench", {"eq_mat": "secBuLi"}],
#         [expt.get("MeOH"), 100 * C.Unit("ml"), "workup"]
# )

# sec_buLi = db.view(expt.c_material[7]["uid"])
#
# ingr.add(sec_buLi, 0.17 * C.Unit("ml"), "initiator", mat_id="secBuLi")
# ingr.remove("MeOH")
# ingr.scale(2)
# ingr.scale_one("styrene", 2)


# Generate node
# process = C.Process(
#     name="Anionic of Styrene",
#     ingr=ingr,
#     procedure="In an argon filled glovebox, a round bottom flask was filled with 216 ml of dried toluene. The "
#               "solution of secBuLi (3 ml, 3.9 mmol) was added next, followed by styrene (22.3 g, 176 mmol) to "
#               "initiate the polymerization. The reaction mixture immediately turned orange. After 30 min, "
#               "the reaction was quenched with the addition of 3 ml of methanol. The polymer was isolated by "
#               "precipitation in methanol 3 times and dried under vacuum.",
#     cond=[
#         C.Cond("temp", 25 * C.Unit("degC")),
#         C.Cond("time", 60 * C.Unit("min")),
#         C.Cond(key="atm", value=inv.get("argon"))
#     ],
#     prop=[
#         C.Prop("yield_mass", 0.47 * C.Unit("g"), 0.02 * C.Unit("g"), method="scale")
#     ],
#     keywords=["polymerization", "living_poly", "anionic", "solution"]
# )


# print(process)

from cript.tutorial import tutorial_data_part2

sec_data_path = tutorial_data_part2["polystyrene_sec"]["path"]
cal_path = tutorial_data_part2["sec_calibration_curve"]["path"]
sample_prep_text = "5 mg of polmyer in 1 ml of THF, filtered 0.45um pores."


sec_data = C.Data(
    name="Crude SEC of polystyrene",
    _type="sec_trace",
    file=C.File(sec_data_path),
    sample_prep=sample_prep_text,
    cond=[
        C.Cond("temp", 30 * C.Unit("degC")),
        C.Cond("time", 60 * C.Unit("min")),
        C.Cond("solvent", value=inv.get("THF")),
        # C.Cond("flow_rate", 1 * C.Unit("ml/min"))
    ],
    calibration=C.File(cal_path)
)

db.save(sec_data, expt)

print("hi")

