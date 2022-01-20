"""
Official Control language support by CRIPT.
For Cond Node

Notes
-----
* unit: is what will be stored in the database (SI units)
* unit_prefer: is the preferred unit to find the value
"""

from .. import cript_types, float_limit


cond_keys = {
    "time": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "second",
        "unit_prefer": "min",
        "descr": "Time"
    },
    "temp": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "kelvin",
        "unit_prefer": "degC",
        "descr": "Temperature"
    },
    "pres": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "kilogram / meter / second ** 2",
        "unit_prefer": "kPa",
        "descr": "Absolute pressure"
    },
    "light_power": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "kilogram * meter ** 2 / second ** 3",
        "unit_prefer": "watt",
        "descr": "Light power hitting a surface (Not electrical power)"
    },
    "light_power_e": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "kilogram * meter ** 2 / second ** 3",
        "unit_prefer": "watt",
        "descr": "Electric power driving the light"
    },
    "light_irradiance": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "kilogram / second ** 3",
        "unit_prefer": "mW/cm**2",
        "descr": "Light power per area"
    },
    "light_wlength": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "meter",
        "unit_prefer": "nm",
        "descr": "max wave length of light"
    },
    "stirring": {
        "type": float,
        "range": [0, float_limit],
        "unit": "radian / second",
        "unit_prefer": "rpm",
        "descr": "rate of stirrer"
    },
    "potential": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "kilogram * meter ** 2 / ampere / second ** 3",
        "unit_prefer": "V",
        "descr": "electrical potential"
    },

    # bools




    # nodes
    "solvent": {
        "type": cript_types["Material"],
        "range": [],
        "unit": "",
        "unit_prefer": "",
        "descr": "Material relevant to condition"
    },
    "atm": {
        "type": cript_types["Material"],
        "range": [],
        "unit": "",
        "unit_prefer": "",
        "descr": "Reaction occurred under an inert atmosphere (N2, Ar)."
    },
}
