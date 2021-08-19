"""
Official Control language support by CRIPT.

"""

from .. import cript_types
from . import float_limit, str_limit


cond_keys = {
    "time": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "min",
        "descr": "Time"
    },
    "temp": {
        "type": cript_types["Quantity"],
        "range": [-273.15, float_limit],
        "unit": "degC",
        "descr": "Temperature"
    },
    "pres": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "kPa",
        "descr": "Absolute pressure"
    },
    "light_power": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "watt",
        "descr": "Light power hitting a surface (Not electrical power)"
    },
    "light_power_e": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "watt",
        "descr": "Electric power driving the light"
    },
    "light_irradiance": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "mW/cm**2",
        "descr": "Light power per area"
    },
    "light_wlength": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "nm",
        "descr": "wave length of light"
    },
    "stirring": {
        "type": float,
        "range": [0, float_limit],
        "unit": "rpm",
        "descr": "rate of stirrer"
    },
    "potential": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "V",
        "descr": "electrical potential"
    },

    # bools




    # nodes
    "solvent": {
        "type": cript_types["Material"],
        "range": [],
        "unit": "",
        "descr": "Material relevant to condition"
    },
    "atm": {
        "type": cript_types["Material"],
        "range": [],
        "unit": "",
        "descr": "Reaction occurred under an inert atmosphere (N2, Ar)."
    },
}
