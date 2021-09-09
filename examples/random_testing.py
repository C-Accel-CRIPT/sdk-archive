from cript import *


db_username = "DW_cript"
db_password = "YXMaoE1"
db_project = "cript_testing"
db_database = "test"
user = "dylanwal@mit.edu"
db = CriptDB(db_username, db_password, db_project, db_database, user)

expt_doc = db.view(Experiment)

expt = load(expt_doc[0])

inv_doc = db.view(Inventory)

inv = load(inv_doc[0])

# process = Process(
#     name="Anionic of Styrene",
#     ingr=[
#         [expt.get("SecBuLi solution 1.4M cHex"), 0.017 * Unit("ml"), "initiator", {"mat_id": "secBuLi"}],
#         [expt.get("toluene"), 10 * Unit("ml"), "solvent"],
#         [expt.get("styrene"), 0.455 * Unit("g"), "monomer"],
#         [expt.get("1BuOH"), 5, "quench", {"eq_mat": "SecBuLi solution"}],
#         [expt.get("MeOH"), 100 * Unit("ml"), "workup"]
#     ],
#     procedure="In an argon filled glovebox, a round bottom flask was filled with 216 ml of dried toluene. The "
#               "solution of secBuLi (3 ml, 3.9 mmol) was added next, followed by styrene (22.3 g, 176 mmol) to "
#               "initiate the polymerization. The reaction mixture immediately turned orange. After 30 min, "
#               "the reaction was quenched with the addition of 3 ml of methanol. The polymer was isolated by "
#               "precipitation in methanol 3 times and dried under vacuum.",
#     cond=[
#         Cond("temp", 25 * Unit("degC")),
#         Cond("time", 60 * Unit("min"))    ],
#     prop=[
#         Prop("yield_mass", 0.47 * Unit("g"), 0.02 * Unit("g"), method="scale")
#     ],
#     keywords=["polymerization", "living_poly", "anionic", "solution"]
# )



a = db.view(expt.c_process[0]["uid"])
b = load(a)


e = export(db.user, depth=4)

print(e)
print("hi")

