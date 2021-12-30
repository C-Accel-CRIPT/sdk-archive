"""
Official Control language support by CRIPT.
For Property node

"""

from .. import cript_types, float_limit, str_limit, degC_lower_limit


property_process_keys = {
    "conv": {
        "type": float,
        "range": [0, 1.2],
        "unit": "",
        "method": ["nmr", "sec"],
        "cond": ["mat_uid"],
        "required": [],
        "descr": "Conversion; (moles consumed)/(initial moles) = conv",
        "names": []
    },
    "init_eff": {
        "type": float,
        "range": [0, float_limit],
        "unit": "",
        "method": ["nmr", "sec"],
        "cond": [],
        "required": [],
        "descr": "Initiator efficiency; The proportion of initiators that result in an active propagating species.",
        "names": []
    },
    "selectivity": {
        "type": float,
        "range": [0, float_limit],
        "unit": "",
        "method": ["nmr", "sec"],
        "cond": [],
        "required": ["mat_id"],
        "descr": "Selectivity; (final moles)/(moles consumed) = selectivity",
        "names": []
    },
    "yield": {
        "type": float,
        "range": [0, 1.2],
        "unit": "",
        "method": ["nmr", "sec"],
        "cond": [],
        "required": ["mat_id"],
        "descr": "Yield; (final moles)/(initial moles) = yield",
        "names": []
    },
    "yield_mass": {
        "type": float,
        "range": [0, float_limit],
        "unit": "g",
        "method": ["scale"],
        "cond": [],
        "required": ["mat_id"],
        "descr": "Yield; mass of product recovered = yield_mass",
        "names": []
    },
    "rate_const": {
        "type": float,
        "range": [-float_limit, float_limit],
        "unit": "",
        "method": [],
        "cond": [],
        "required": ["mat_id"],
        "descr": "Rate constant",
        "names": []
    },
}

property_material_keys = {
    "color": {
        "type": str,
        "range": [0, str_limit],
        "unit": None,
        "method": ["visual"],
        "cond": [],
        "required": [],
        "descr": "visual appearance of substance",
        "names": []
    },
    "color_RGB": {
        "type": list[float],
        "range": [0, 255],
        "unit": None,
        "method": [],
        "cond": [],
        "required": [],
        "descr": "visual appearance of substance on Red-Green-Blue scale",
        "names": []
    },
    "conc_mass": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "g/ml",
        "method": [],
        "cond": [],
        "required": ["mat_id"],
        "descr": "mass of constituent divided by the volume of mixture",
        "names": ["concentration"]
    },
    "conc_molar": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "M",
        "method": [],
        "cond": [],
        "required": ["mat_id"],
        "descr": "moles of constituent divided by the volume of mixture",
        "names": ["concentration"]
    },
    "conc_number": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "1/ml",
        "method": [],
        "cond": [],
        "required": ["mat_id"],
        "descr": "number of entities of a constituent divided by the volume of mixture",
        "names": ["concentration"]
    },
    "conc_vol": {
        "type": float,
        "range": [0, float_limit],
        "unit": "",
        "method": [],
        "cond": [],
        "required": ["mat_id"],
        "descr": "volume of constituent divided by the volume of mixture",
        "names": ["concentration"]
    },
    "contact_angle": {
        "type": cript_types["Quantity"],
        "range": [0, 360],
        "unit": "deg",
        "method": [],
        "cond": [],
        "required": [],
        "descr": "angle between the liquid drop and a surface",
        "names": []
    },
    "crys_frac": {
            "type": float,
            "range": [0, 1.2],
            "unit": "",
            'methods': ['dsc'],
            "cond": [],
            "required": [],
            'descr': 'Fraction of crystallinity by weight',
            "names": ["fraction crystallinity by weight"]
        },
    "density": {
        "type": cript_types["Quantity"],
        "range": [0, 23],  # Osmium is densest element at 22 g/cm^3
        "unit": "g/ml",
        "method": [],
        "cond": ["pres", "temp"],
        "required": [],
        "descr": "quantity of mass per unit volume",
        "names": ["specific mass"]
    },

    "enth_crys": {
        "type": cript_types["Quantity"],
        "range": [-float_limit, float_limit],
        "unit": "J/mol",
        'methods': ['dsc'],
        "cond": [],
        "required": [],
        'descr': 'Enthalpy of crystallization, molar basis',
        "names": ["enthalpy of crystallization"]
    },
    "entr_crys": {
        "type": cript_types["Quantity"],
        "range": [-float_limit, float_limit],
        "unit": "J/mol/K",
        'methods': ['dsc'],
        "cond": [],
        "required": [],
        'descr': 'Entropy of crystallization, molar basis',
        "names": ["entropy of crystallization"]
    },
    "heat_combustion_molar": {
        "type": cript_types["Quantity"],
        "range": [-float_limit, float_limit],
        "unit": "J/mol",
        "method": [],
        "cond": [],
        "required": [],
        "descr": "The amount heat released during the combustion of a specific amount of material",
        "names": []
    },
    "heat_combustion_mass": {
        "type": cript_types["Quantity"],
        "range": [-float_limit, float_limit],
        "unit": "J/g",
        "method": [],
        "cond": [],
        "required": [],
        "descr": "The amount heat released during the combustion of a specific amount of material",
        "names": []
    },
    "heat_combustion_volume": {
        "type": cript_types["Quantity"],
        "range": [-float_limit, float_limit],
        "unit": "J/ml",
        "method": [],
        "cond": [],
        "required": [],
        "descr": "The amount heat released during the combustion of a specific amount of material",
        "names": []
    },
    "heat_vaporization_molar": {
        "type": cript_types["Quantity"],
        "range": [-float_limit, float_limit],
        "unit": "J/mol",
        "method": [],
        "cond": [],
        "required": [],
        "descr": "The amount heat required to transform a liquid into a gas",
        "names": ["enthalpy of vaporization", "heat_vaporization", "latent heat of vaporization",
                  "heat of evaporation"]
    },
    "heat_vaporization_mass": {
        "type": cript_types["Quantity"],
        "range": [-float_limit, float_limit],
        "unit": "J/g",
        "method": [],
        "cond": [],
        "required": [],
        "descr": "The amount heat required to transform a liquid into a gas",
        "names": ["enthalpy of vaporization", "heat_vaporization", "latent heat of vaporization",
                  "heat of evaporation"]
    },
    "heat_capacity_pres": {
        "type": cript_types["Quantity"],
        "range": [-float_limit, float_limit],
        "unit": "J/mol/K",
        'methods': ['calorimetry', 'dsc'],
        "cond": [],
        "required": [],
        'descr': 'The amount of heat needed to be supplied to a given mole (based on repeat unit) to produce a '
                 'change in temperature at constant pressure',
        "names": ["molar heat capacity constant pressure"]
    },
    "heat_capacity_vol": {
        "type": cript_types["Quantity"],
        "range": [-float_limit, float_limit],
        "unit": "J/mol/K",
        'methods': ['calorimetry', 'dsc'],
        "cond": [],
        "required": [],
        'descr': 'The amount of heat needed to be supplied to a given mole (based on repeat unit) to produce a '
                 'change in temperature at constant volume',
        "names": ["molar heat capacity constant volume"]
    },
    "magnetic_sus_mass": {
        "type": cript_types["Quantity"],
        "range": [-float_limit, float_limit],
        "unit": "m**3/kg",
        "method": [],
        "cond": ["temp", "pres"],
        "required": [],
        "descr": "magnetic susceptibility",
        "names": []
    },
    "magnetic_sus_molar": {
        "type": cript_types["Quantity"],
        "range": [-float_limit, float_limit],
        "unit": "m**3/mol",
        "method": [],
        "cond": ["temp", "pres"],
        "required": [],
        "descr": "magnetic susceptibility",
        "names": []
    },
    "magnetic_sus_vol": {
        "type": cript_types["Quantity"],
        "range": [-float_limit, float_limit],
        "unit": "",
        "method": [],
        "cond": ["temp", "pres"],
        "required": [],
        "descr": "magnetic susceptibility",
        "names": []
    },
    "molar_mass": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "g/mol",
        "method": ["prescribed"],
        "cond": [],
        "required": [],
        "descr": "mass of one mole of a compound; computed from the standard atomic weights and is thus a "
                 "terrestrial average.",
        "names": []
    },
    "mw_d": {
        "type": cript_types["Quantity"],
        "range": [1, float_limit],
        "unit": "",
        'methods': ['nmr', 'sec', 'maldi'],
        "cond": [],
        "required": [],
        'descr': "Ratio of weight averaged molecular weight over number average molecular weight.",
        "names": ["dispersity", "pdi", "polydispersity index", "molecular weight dispersity"]
    },
    "mw_kurtosis": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "g/mol",
        'methods': ['nmr', 'sec', 'maldi'],
        "cond": [],
        "required": [],
        'descr': 'Kurtosis of molecular weight distribution or the fourth moment of the molecular weight'
                 ' distribution',
        "names": ["molecular weight kurtosis"]
    },
    "mw_n": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "g/mol",
        'methods': ['nmr', 'sec', 'maldi', 'osmtic_pres'],
        "cond": [],
        "required": [],
        'descr': "Average molecular weight on the bases of moles or first moment of the molecular weight distribution.",
        "names": ["number average molecular weight", "number average molar molecular"]
    },
    "mw_skew": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "g/mol",
        'methods': ['nmr', 'sec', 'maldi'],
        "cond": [],
        "required": [],
        'descr': 'skewness of molecular weight distribution or the third moment of the molecular weight'
                 ' distribution',
        "names": ["molecular weight skewness"]
    },
    "mw_std_dev": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "g/mol",
        'methods': ['nmr', 'sec', 'maldi'],
        "cond": [],
        "required": [],
        'descr': 'Standard deviation of molecular weight distribution or square root of the second moment of the'
                 ' molecular weight distribution',
        "names": ["molecular weight standard deviation"]
    },
    "mw_v": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "g/mol",
        'methods': ['viscometer'],
        "cond": [],
        "required": [],
        'descr': "Average molecular weight determined from viscosity",
        "names": ["viscosity average molecular weight"]
    },
    "mw_var": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "g/mol",
        'methods': ['nmr', 'sec', 'maldi'],
        "cond": [],
        "required": [],
        'descr': 'Variance of molecular weight distribution or the second moment of the molecular weight'
                 ' distribution',
        "names": ["molecular weight variance"]
    },
    "mw_w": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "g/mol",
        'methods': ['nmr', 'sec', 'maldi', 'ls'],
        "cond": [],
        "required": [],
        'descr': "Average molecular weight on the bases of weight.",
        "names": ["weight average molecular weight", "weight average molar molecular"]
    },
    "mw_z": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "g/mol",
        'methods': ['nmr', 'sec', 'maldi', 'osmtic_pres'],
        "cond": [],
        "required": [],
        'descr': "z average molecular weight",
        "names": ["Z Average Molecular Weight"]
    },
    "odor": {
        "type": str,
        "range": [],
        "unit": None,
        "method": [],
        "cond": [],
        "required": [],
        "descr": "scent of chemical",
        "names": []
    },
    "phase": {
        "type": str,
        "range": ["gas", "liquid", "solution", "suspension", "plasma"],
        "unit": None,
        "method": ["visual"],
        "cond": ["pres", "temp"],
        "required": [],
        "descr": "phase of matter",
        "names": ["phase of matter"]
    },
    "pka": {
        "type": float,
        "range": [-float_limit, float_limit],
        "unit": None,
        "method": [],
        "cond": [],
        "required": [],
        "descr": "acid",
        "names": []
    },
    "pkb": {
        "type": float,
        "range": [-float_limit, float_limit],
        "unit": None,
        "method": [],
        "cond": [],
        "required": [],
        "descr": "base",
        "names": []
    },
    "ref_index": {
        "type": float,
        "range": [0, float_limit],
        "unit": "",
        'method': [],
        "cond": ["temp"],
        "required": [],
        'descr': "A dimensionless number that describes how fast light travels through the material.",
        "names": ["refractive index"]
    },
    "solubility": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "g/ml",
        'method': [],
        "cond": ["temp", "solvent"],
        "required": [],
        'descr': "A dimensionless number that describes how fast light travels through the material.",
        "names": ["refractive index"]
    },
    "surface_tension": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "J/m**2",
        'method': [],
        "cond": ["temp", "pres"],
        "required": [],
        'descr': "The tension formed on the surface of a liquid",
        "names": []
    },
    "temp_autoignition": {
        "type": cript_types["Quantity"],
        "range": [degC_lower_limit, float_limit],
        "unit": "degC",
        "method": [],
        "cond": ["pres"],
        "required": [],
        "descr": "The temperature where a chemical ca spontaneously ignite",
        "names": ["autoignition point", "autoignition temperature", "kindling point"]
    },
    "temp_boil": {
        "type": cript_types["Quantity"],
        "range": [degC_lower_limit, float_limit],
        "unit": "degC",
        "method": [],
        "cond": ["pres"],
        "required": [],
        "descr": "temperature where a liquid turns into a gas",
        "names": ["boiling point", "boiling temperature", "bp"]
    },
    "temp_flash": {
        "type": cript_types["Quantity"],
        "range": [degC_lower_limit, float_limit],
        "unit": "degC",
        "method": [],
        "cond": [],
        "required": [],
        "descr": "The temperature where vapors from a volatile material can ignite",
        "names": []
    },
    "temp_melt": {
        "type": cript_types["Quantity"],
        "range": [degC_lower_limit, float_limit],
        "unit": "degC",
        "method": ["dsc"],
        "cond": ["pres"],
        "required": [],
        "descr": "temperature where a solid turns into a liquid",
        "names": ["melting point", "melting temperature", "tm"]
    },
    "temp_glass": {
        "type": cript_types["Quantity"],
        "range": [degC_lower_limit, float_limit],
        "unit": "degC",
        'methods': ['dsc'],
        "cond": [],
        "required": [],
        'descr': 'The transition temperature where a substances turns into a glass; vitrification.',
        "names": ["glass transition temperature"]
    },
    "therm_cond": {
        "type": cript_types["Quantity"],
        "range": [-float_limit, float_limit],
        "unit": "W/m/k",
        'methods': [],
        "cond": [],
        "required": [],
        'descr': 'Measure of a materials ability to conduct heat',
        "names": ["specific thermal conductivity"]
    },
    "therm_diff": {
        "type": cript_types["Quantity"],
        "range": [-float_limit, float_limit],
        "unit": "m**2/s",
        'methods': ['calorimetry', 'dsc'],
        "cond": [],
        "required": [],
        'descr': 'A measures the rate of transfer of heat of a material from the hot end to the cold end.',
        "names": ["thermal diffusivity"]
    },
    "therm_expand_l": {
        "type": cript_types["Quantity"],
        "range": [-float_limit, float_limit],
        "unit": "1/k",
        'methods': [],
        "cond": [],
        "required": [],
        'descr': 'A change in dimension in response to a change in temperature (not including phase transitions)',
        "names": ["linear thermal expansion"]
    },
    "therm_expand_v": {
        "type": cript_types["Quantity"],
        "range": [-float_limit, float_limit],
        "unit": "1/k",
        'methods': [],
        "cond": [],
        "required": [],
        'descr': 'A change in volume in response to a change in temperature (not including phase transitions)',
        "names": ["volumetric thermal expansion"]
    },
    "vapor_pres": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "kPa",
        "method": [],
        "cond": ["temp"],
        "required": [],
        "descr": "the pressure at which the vapor is in thermodynamic equilibrium with the condensed phase",
        "names": ["vapor pressure", "equilibrium vapor pressure"]
    },
    "viscosity_dynamic": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "Pa*s",
        "method": [],
        "cond": ["temp"],
        "required": [],
        "descr": "the resistance to movement of a fluid",
        "names": ["viscosity"]
    },
    "viscosity_kinematic": {
        "type": cript_types["Quantity"],
        "range": [0, float_limit],
        "unit": "cSt",
        "method": [],
        "cond": ["temp"],
        "required": [],
        "descr": "the dynamic viscosity over the density of the fluid",
        "names": ["viscosity", "momentum diffusivity"]
    },
}

method_keys = {
    'prescribed': 'a value that can be defined, (Ex. calculating MW from molecular formula)',
    'comp': 'computation or simulation',
    'nmr': 'nuclear magnetic resonance',
    'sec': 'size exclusion chromatography / gel permeation chromatography (GPC)',
    'gc': 'gas chromatography',
    'chrom': 'general chromatography',
    'ms': 'general mass spectrometry',
    'maldi': 'matrix assisted laser desorption ionization',
    'ultra_centr': 'ultra centrifugation',
    'osmtic_pres': 'osmotic pressure',
    'calorimetry': 'calorimetry',
    'cryoscopy': 'cryoscopy',
    'ebullioscopy': 'ebullioscopy',
    'viscometer': 'viscometer',
    'utm': 'universal testing machine',
    'dma': 'dynamic mechanical analysis',
    'dsc': 'differential scanning calorimetry',
    'tga': 'thermogravimetric analysis',
    'raman': 'raman spectroscopy',
    'ir': 'infrared spectroscopy',
    'uv_vis': 'ultraviolet–visible spectroscopy',
    'x_ray': 'x-ray spectroscopy',
    'saxs': 'small-angle x-ray scattering',
    'waxs': 'wide-angle x-ray scattering',
    'neutron': 'neutron scattering',
    'ls': 'static light scattering',
    'dls': 'dynamic light scattering',
    'confocal': 'confocal microscopy',
    'afm': 'atomic force microscopy',
    'tem': 'transmission electron microscopy',
    'sem': 'scanning electron microscopy',
    'scale': 'scale',
}
