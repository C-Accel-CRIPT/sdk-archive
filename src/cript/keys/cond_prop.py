

from .. import cript_types

max_limit = 1.79E308

cond_keys = {
    "time": {
        "type": float,
        "range": [0, max_limit],
        "unit": "min",
        "descr": "Time"
    },
    "temp": {
        "type": float,
        "range": [-273.15, max_limit],
        "unit": "degC",
        "descr": "Temperature"
    },
    "pres": {
        "type": float,
        "range": [0, max_limit],
        "unit": "kPa",
        "descr": "Absolute pressure"
    },
    "light_power": {
        "type": float,
        "range": [0, max_limit],
        "unit": "watt",
        "descr": "light power hitting a surface. (Not electrical power)"
    },
    "light_power_e": {
        "type": float,
        "range": [0, max_limit],
        "unit": "watt",
        "descr": "Electric powering the light."
    },
    "light_irradiance": {
        "type": float,
        "range": [0, max_limit],
        "unit": "mW/cm**2",
        "descr": "Light power per area"
    },
    "light_wlength": {
        "type": float,
        "range": [0, max_limit],
        "unit": "nm",
        "descr": "wave length of light"
    },
    "stirring": {
        "type": float,
        "range": [0, max_limit],
        "unit": "rpm",
        "descr": "revolutions per minute for stirrer"
    },
    "potential": {
        "type": float,
        "range": [0, max_limit],
        "unit": "V",
        "descr": "electrical potential"
    },

    # bools


    # nodes
    "solvent": {
        "type": cript_types["Material"],
        "descr": "Reaction occurred under an inert atmosphere (N2, Ar). [1 - inert, 0 - Not inert]"
    },
    "atm": {
        "type": cript_types["Material"],
        "descr": "Reaction occurred under an inert atmosphere (N2, Ar)."
    },
}



prop_keys_rxn = {
    "conv": {
        "type": float,
        "range": [0, 1.2],
        "unit": "",
        "method": ["nmr", "sec"],
        "cond": [],
        "required": ["id"],
        "descr": "Conversion; (moles consumed)/(initial moles) = conv"
    },
    "init_eff": {
        "type": float,
        "range": [0, max_limit],
        "unit": "",
        "method": ["nmr", "sec"],
        "cond": [],
        "required": [],
        "descr": "Initiator efficiency; The proportion of initiators that result in an active propagating species."
    },
    "selectivity": {
        "type": float,
        "range": [0, max_limit],
        "unit": "",
        "method": ["nmr", "sec"],
        "cond": [],
        "required": ["id"],
        "descr": "Selectivity; (final moles)/(moles consumed) = selectivity"
    },
    "yield": {
        "type": float,
        "range": [0, 1.2],
        "unit": "",
        "method": ["nmr", "sec"],
        "cond": [],
        "required": ["id"],
        "descr": "Yield; (final moles)/(initial moles) = yield"
    },
    "yield_mass": {
        "type": float,
        "range": [0, max_limit],
        "unit": "g",
        "method": ["scale"],
        "cond": [],
        "required": ["id"],
        "descr": "Yield; mass of product recovered = yield_mass"
    },
}

prop_keys_mat_poly = {

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
