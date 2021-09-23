from cript import Path

__all__ = ["tutorial_data_part2"]

tutorial_path = Path(__file__).parent
tutorial_data_part2 = {
    "polystyrene_sec": {
        "path": Path(r"../tutorial/Polystyrene_SEC.csv"),
        "descr": ""
    },
    "polystyrene_1hnmr": {
        "path": Path(r"../tutorial/Polystyrene_1HNMR.zip"),
        "descr": ""
    },
    "sec_calibration_curve": {
        "path": Path(r"../tutorial/sec_calibration_curve.xlsx"),
        "descr": ""
    },

}

for k in tutorial_data_part2.keys():
    tutorial_data_part2[k]["path"] = (tutorial_path / tutorial_data_part2[k]["path"]).resolve()

