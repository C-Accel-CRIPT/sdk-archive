"""
Property Keywords

"""

from . import float_limit, str_limit

prop_keys_rxn = {
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
}

prop_keys_mat = {
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
    "density": {
        "type": float,
        "range": [0, 23],  # Osmium is densest element at 22 g/cm^3
        "unit": "g/ml",
        "method": [],
        "cond": ["pres", "temp"],
        "required": [],
        "descr": "quantity of mass per unit volume",
        "names": ["specific mass"]
    },
    "molar_mass": {
        "type": float,
        "range": [0, float_limit],
        "unit": "g/mol",
        "method": ["prescribed"],
        "cond": [],
        "required": [],
        "descr": "mass of one mole of a compound; computed from the standard atomic weights and is thus a "
                 "terrestrial average.",
        "names": []
    },
    "mass_conc": {
        "type": float,
        "range": [0, float_limit],
        "unit": "g/ml",
        "method": [],
        "cond": [],
        "required": ["mat_id"],
        "descr": "mass of constituent divided by the volume of mixture",
        "names": ["concentration"]
    },
    "molar_conc": {
        "type": float,
        "range": [0, float_limit],
        "unit": "M",
        "method": [],
        "cond": [],
        "required": ["mat_id"],
        "descr": "moles of constituent divided by the volume of mixture",
        "names": ["concentration"]
    },
    "number_conc": {
        "type": float,
        "range": [0, float_limit],
        "unit": "1/ml",
        "method": [],
        "cond": [],
        "required": ["mat_id"],
        "descr": "number of entities of a constituent divided by the volume of mixture",
        "names": ["concentration"]
    },
    "vol_conc": {
        "type": float,
        "range": [0, float_limit],
        "unit": "",
        "method": [],
        "cond": [],
        "required": ["mat_id"],
        "descr": "volume of constituent divided by the volume of mixture",
        "names": ["concentration"]
    },
    "bp": {
        "type": float,
        "range": [0, float_limit],
        "unit": "degC",
        "method": [],
        "cond": ["pres"],
        "required": [],
        "descr": "temperature where a liquid turns into a gas",
        "names": ["boiling point", "boiling temperature"]
    },
    "mp": {
        "type": float,
        "range": [0, float_limit],
        "unit": "degC",
        "method": [],
        "cond": ["pres"],
        "required": [],
        "descr": "temperature where a solid turns into a liquid",
        "names": ["melting point", "melting temperature"]
    },
    "ref_index": {
        "type": float,
        "range": [0, float_limit],
        "unit": "",
        'methods': [],
        "cond": ["temp"],
        "required": [],
        'descr': "A dimensionless number that describes how fast light travels through the material.",
        "names": ["refractive index"]
    },
    "solubility": {
        "type": float,
        "range": [0, float_limit],
        "unit": "g/ml",
        'methods': [],
        "cond": ["temp", "solvent"],
        "required": [],
        'descr': "A dimensionless number that describes how fast light travels through the material.",
        "names": ["refractive index"]
    },
}

prop_keys_poly = {
    "m_n": {
        "type": float,
        "range": [0, float_limit],
        "unit": "g/mol",
        'methods': ['nmr', 'sec', 'maldi', 'osmtic_pres'],
        "cond": [],
        "required": [],
        'descr': "Average molecular weight on the bases of moles or first moment of the molecular weight distribution.",
        "names": ["number average molecular weight", "number average molar molecular"]
    },
    "m_w": {
        "type": float,
        "range": [0, float_limit],
        "unit": "g/mol",
        'methods': ['nmr', 'sec', 'maldi', 'ls'],
        "cond": [],
        "required": [],
        'descr': "Average molecular weight on the bases of weight.",
        "names": ["weight average molecular weight", "weight average molar molecular"]
    },
    "m_z": {
        "type": float,
        "range": [0, float_limit],
        "unit": "g/mol",
        'methods': ['nmr', 'sec', 'maldi', 'osmtic_pres'],
        "cond": [],
        "required": [],
        'descr': "z average molecular weight",
        "names": ["Z Average Molecular Weight"]
    },
    "d": {
        "type": float,
        "range": [1, float_limit],
        "unit": "",
        'methods': ['nmr', 'sec', 'maldi'],
        "cond": [],
        "required": [],
        'descr': "Ratio of weight averaged molecular weight over number average molecular weight.",
        "names": ["dispersity", "pdi", "polydispersity index", "molecular weight dispersity"]
    },
    "m_v": {
        "type": float,
        "range": [0, float_limit],
        "unit": "g/mol",
        'methods': ['viscometer'],
        "cond": [],
        "required": [],
        'descr': "Average molecular weight determined from viscosity",
        "names": ["viscosity average molecular weight"]
    },
    "mw_std_dev": {
        "type": float,
        "range": [0, float_limit],
        "unit": "g/mol",
        'methods': ['nmr', 'sec', 'maldi'],
        "cond": [],
        "required": [],
        'descr': 'Standard deviation of molecular weight distribution or square root of the second moment of the'
                 ' molecular weight distribution',
        "names": ["molecular weight standard deviation"]
    },
    "mw_var": {
        "type": float,
        "range": [0, float_limit],
        "unit": "g/mol",
        'methods': ['nmr', 'sec', 'maldi'],
        "cond": [],
        "required": [],
        'descr': 'Variance of molecular weight distribution or the second moment of the molecular weight'
                 ' distribution',
        "names": ["molecular weight variance"]
    },
    "mw_skew": {
        "type": float,
        "range": [0, float_limit],
        "unit": "g/mol",
        'methods': ['nmr', 'sec', 'maldi'],
        "cond": [],
        "required": [],
        'descr': 'skewness of molecular weight distribution or the third moment of the molecular weight'
                 ' distribution',
        "names": ["molecular weight skewness"]
    },
    "mw_kurtosis": {
        "type": float,
        "range": [0, float_limit],
        "unit": "g/mol",
        'methods': ['nmr', 'sec', 'maldi'],
        "cond": [],
        "required": [],
        'descr': 'Kurtosis of molecular weight distribution or the fourth moment of the molecular weight'
                 ' distribution',
        "names": ["molecular weight kurtosis"]
    },

    # Thermal Properties
    "t_m": {
        "type": float,
        "range": [-273.15, float_limit],
        "unit": "degC",
        'methods': ['dsc'],
        "cond": [],
        "required": [],
        'descr': 'The transition temperature where crystal structures are destroyed.',
        "names": ["melting temperature"]
    },
    "t_g": {
        "type": float,
        "range": [-273.15, float_limit],
        "unit": "degC",
        'methods': ['dsc'],
        "cond": [],
        "required": [],
        'descr': 'The transition temperature where a substances turns into a glass; vitrification.',
        "names": ["glass transition temperature"]
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
    "enth_crys": {
        "type": float,
        "range": [-float_limit, float_limit],
        "unit": "J/mol",
        'methods': ['dsc'],
        "cond": [],
        "required": [],
        'descr': 'Enthalpy of crystallization, molar basis',
        "names": ["enthalpy of crystallization"]
    },
    "entr_crys": {
        "type": float,
        "range": [-float_limit, float_limit],
        "unit": "J/mol/K",
        'methods': ['dsc'],
        "cond": [],
        "required": [],
        'descr': 'Entropy of crystallization, molar basis',
        "names": ["entropy of crystallization"]
    },
    "therm_cond": {
        "type": float,
        "range": [-float_limit, float_limit],
        "unit": "W/m/k",
        'methods': [],
        "cond": [],
        "required": [],
        'descr': 'Measure of a materials ability to conduct heat',
        "names": ["specific thermal conductivity"]
    },
    "therm_expand_v": {
        "type": float,
        "range": [-float_limit, float_limit],
        "unit": "1/k",
        'methods': [],
        "cond": [],
        "required": [],
        'descr': 'A change in volume in response to a change in temperature (not including phase transitions)',
        "names": ["volumetric thermal expansion"]
    },
    "therm_expand_l": {
        "type": float,
        "range": [-float_limit, float_limit],
        "unit": "1/k",
        'methods': [],
        "cond": [],
        "required": [],
        'descr': 'A change in dimension in response to a change in temperature (not including phase transitions)',
        "names": ["linear thermal expansion"]
    },
    "c_p": {
        "type": float,
        "range": [-float_limit, float_limit],
        "unit": "J/mol/K",
        'methods': ['calorimetry', 'dsc'],
        "cond": [],
        "required": [],
        'descr': 'The amount of heat needed to be supplied to a given mole (based on repeat unit) to produce a '
                 'change in temperature at constant pressure',
        "names": ["molar heat capacity constant pressure"]
    },
    "c_v": {
        "type": float,
        "range": [-float_limit, float_limit],
        "unit": "J/mol/K",
        'methods': ['calorimetry', 'dsc'],
        "cond": [],
        "required": [],
        'descr': 'The amount of heat needed to be supplied to a given mole (based on repeat unit) to produce a '
                 'change in temperature at constant volume',
        "names": ["molar heat capacity constant volume"]
    },
    "therm_diff": {
        "type": float,
        "range": [-float_limit, float_limit],
        "unit": "m**2/s",
        'methods': ['calorimetry', 'dsc'],
        "cond": [],
        "required": [],
        'descr': 'A measures the rate of transfer of heat of a material from the hot end to the cold end.',
        "names": ["thermal diffusivity"]
    },
    
    # Physical Properties
    
}

keys_methods = {
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
