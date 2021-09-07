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

from cript.tutorial import tutorial_data_part2

sec_data_path = tutorial_data_part2["polystyrene_sec"]["path"]
cal_path = tutorial_data_part2["sec_calibration_curve"]["path"]
nmr1h_path = tutorial_data_part2["polystyrene_1hnmr"]["path"]

sec_data = Data(
    name="Crude SEC of polystyrene",
    _type="sec_trace",
    file=File(sec_data_path),
    sample_prep="5 mg of polmyer in 1 ml of THF, filtered 0.45um pores.",
    cond=[
        Cond("temp", 30 * Unit("degC")),
        Cond("time", 60 * Unit("min")),
        Cond("solvent", value=inv.get("THF")),
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
        Cond("solvent", value=inv.get("CDCl3")),
    ]
)


db.save(sec_data, expt)
db.save(nmr_data, expt)













print("hi")

