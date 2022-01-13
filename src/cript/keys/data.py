"""
Official Control language support by CRIPT.
For Data Node

Notes
-----
* formatting should follow with 'main_technique' followed by 'labels' separated by an underscore.
* "None" in `labels` or `units` allows users to overwrite   
* Order is important in the `labels` and `units`. index: 0 = x-axis; index: 1 = y-axis; index: 2 = z-axis; etc. 

"""

data_keys = {
    # generic - (here  just as a template)
    # "vector": {
    #     "labels": [None],
    #     "units": [None],
    #     "descr": "Generic 1D object",
    # },
    # "matrix": {
    #     "labels": [None, None],
    #     "units": [None, None],
    #     "descr": "Generic 2D object",
    # },
    # "tensor3": {
    #     "labels": [None, None, None],
    #     "units": [None, None, None],
    #     "descr": "Generic 3D object",
    # },
    # "tensor": {
    #     "labels": None,
    #     "units": None,
    #     "descr": "Generic nD object",
    # },

    # 2D data
    ###################################################################################################################
    "rxn_conv": {
        "labels": ["time", "conversion"],
        "units": ["min", ""],
        "descr": "reaction conversion vs time",
    },
    "mn_conv": {
        "labels": ["conversion", "m_n"],
        "units": ["", "mol"],
        "descr": "M_n vs monomer conversion",
    },
    "sec_trace": {
        "labels": ["retention time", "signal"],
        "units": ["min", ""],
        "descr": "SEC trace (by retention time)",
    },
    "sec_trace_vol": {
        "labels": ["elution volume", "signal"],
        "units": ["ml", ""],
        "descr": "SEC trace (by elution volume)",
    },
    "mwd": {
        "labels": ["molecular weight", "population"],
        "units": ["g/mol", "mol frac"],
        "descr": "molecular weight distribution (by mole)",
    },
    "mwd_wt": {
        "labels": ["molecular weight", "population"],
        "units": ["g/mol", "wt frac"],
        "descr": "molecular weight distribution (by weight)",
    },
    "nmr": {
        "labels": ["time", "voltage"],
        "units": ["us", "V"],
        "descr": "Free induction decay",
    },
    "nmr_h1": {
        "labels": ["chemical shift", "signal"],
        "units": ["ppm", ""],
        "descr": "proton NMR (H1 NMR)",
    },
    "nmr_c13": {
        "labels": ["chemical shift", "signal"],
        "units": ["ppm", ""],
        "descr": "carbon NMR (C13 NMR)",
    },
    "nmr_n15": {
        "labels": ["chemical shift", "signal"],
        "units": ["ppm", ""],
        "descr": "nitrogen NMR (N15 NMR)",
    },
    "nmr_o17": {
        "labels": ["chemical shift", "signal"],
        "units": ["ppm", ""],
        "descr": "oxygen NMR (O17 NMR)",
    },
    "nmr_f19": {
        "labels": ["chemical shift", "signal"],
        "units": ["ppm", ""],
        "descr": "fluorine NMR (F19 NMR)",
    },
    "nmr_si29": {
        "labels": ["chemical shift", "signal"],
        "units": ["ppm", ""],
        "descr": "silicon NMR (Si29 NMR)",
    },
    "nmr_p31": {
        "labels": ["chemical shift", "signal"],
        "units": ["ppm", ""],
        "descr": "phosphorous NMR (P31 NMR)",
    },
    "nmr_noe": {
        "labels": ["chemical shift", "signal"],
        "units": ["ppm", ""],
        "descr": "nuclear Overhauser effect NMR",
    },
    "nmr_tocsy": {
        "labels": ["chemical shift", "signal"],
        "units": ["ppm", ""],
        "descr": "total correlation spectroscopy NMR",
    },
    "ir": {
        "labels": ["wavenumber", "signal"],
        "units": ["cm**-1", ""],
        "descr": "infrared spectroscopy",
    },
    "stess_strain": {
        "labels": ["stess", "strain"],
        "units": ["kPa", ""],
        "descr": "stress strain curve",
    },
    "waxs": {
        "labels": ["q", "strain"],
        "units": ["angstrom**-1", ""],
        "descr": "wide angle light scattering",
    },
    "saxs": {
        "labels": ["q", "strain"],
        "units": ["angstrom**-1", ""],
        "descr": "small angle light scattering",
    },
    "g_prime": {
        "labels": ["frequency", "rad/s"],
        "units": ["stress", "Pa"],
        "descr": "storage modulus",
    },
    "g_doub_prime": {
        "labels": ["frequency", "rad/s"],
        "units": ["stress", "Pa"],
        "descr": "loss modulus",
    },
    "photo_gray": {
        "labels": ["", ""],
        "units": ["", ""],
        "descr": "Single value photograph (like gray scale)",
    },
    
    # 3D data
    ###################################################################################################################
    "photo_rgb": {
        "labels": ["x", "y", "rgb"],
        "units": ["", "", ""],
        "descr": "photo with the dimension 1 being rows, dimension 2 being columns, "
                 "and dimension 3 being  [red, green, blue]",
    },
    "nmr_cosy": {
        "labels": ["chemical shift", "chemical shift", "signal"],
        "units": ["ppm", "ppm", ""],
        "descr": "correlation spectroscopy NMR (H - H)",
    },
    "nmr_hsqc": {
        "labels": ["chemical shift", "chemical shift", "signal"],
        "units": ["ppm", "ppm", ""],
        "descr": "heteronuclear single-quantum correlation spectroscopy NMR (H - C)",
    },
    "nmr_hmbc": {
        "labels": ["chemical shift", "chemical shift", "signal"],
        "units": ["ppm", "ppm", ""],
        "descr": "heteronuclear multiple-bond correlation spectroscopy NMR (H - C)",
    },
    "nmr_dosy": {
        "labels": ["chemical shift", "diffusion coefficient", "signal"],
        "units": ["ppm", "m**2/s", ""],
        "descr": "Diffusion NMR",
    },
    "nmr_kinetic": {
        "labels": ["chemical shift", "time", "signal"],
        "units": ["ppm", "min", ""],
        "descr": "NMR kinetic array",
    },
    "waxs_i": {
        "labels": ["distance", "distance", "signal"],
        "units": ["nm**-1", "nm**-1", ""],
        "descr": "wide angle light scattering image",
    },
    "saxs_i": {
        "labels": ["distance", "distance", "signal"],
        "units": ["nm**-1", "nm**-1", ""],
        "descr": "small angle light scattering image",
    },
    "s_neutron": {
        "labels": ["distance", "distance", "signal"],
        "units": ["nm**-1", "nm**-1", ""],
        "descr": "small angle neutron scattering image",
    },
    "tem_height": {
        "labels": ["distance", "distance", "height"],
        "units": ["nm", "nm", "nm"],
        "descr": "transmission electron microscopy height map",
    },
    "afm_height": {
        "labels": ["distance", "distance", "height"],
        "units": ["nm", "nm", "nm"],
        "descr": "atomic force microscope height map",
    },
    "afm_amp": {
        "labels": ["distance", "distance", "amplitude"],
        "units": ["nm", "nm", "nm"],
        "descr": "atomic force microscope amplitude map",
    },
    "afm_phase": {
        "labels": ["distance", "distance", "phase"],
        "units": ["nm", "nm", "deg"],
        "descr": "atomic force microscope phase map",
    },

    # n-D data
    ###################################################################################################################
}
