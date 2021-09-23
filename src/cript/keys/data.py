
data_keys = {
    # 1D generic - Generics should only be used when specific key does not exist
    "vector": {
        "x": "",
        "x_unit": "",
        "descr": "Generic 1D object",
    },
    "matrix": {
        "x": "",
        "x_unit": "",
        "y": "",
        "y_unit": "",
        "descr": "Generic 2D object",
    },
    "tensor3": {
        "x": "",
        "x_unit": "",
        "y": "",
        "y_unit": "",
        "z": "",
        "z_unit": "",
        "descr": "Generic 3D object",
    },
    # "tensor": {
    #     "labels": [],
    #     "units": [],
    #     "descr": "Generic nD object",
    # },

    # 2D data
    "rxn_conv": {
        "x": "time",
        "x_unit": "min",
        "y": "conversion",
        "y_unit": "",
        "descr": "reaction conversion vs time",
    },
    "mn_conv": {
        "x": "conversion",
        "x_unit": "",
        "y": "m_n",
        "y_unit": "mol",
        "descr": "M_n vs monomer conversion",
    },
    "sec_trace": {
        "x": "retention time",
        "x_unit": "min",
        "y": "signal",
        "y_unit": "",
        "descr": "SEC trace (by retention time)",
    },
    "sec_trace_vol": {
        "x": "elution volume",
        "x_unit": "ml",
        "y": "signal",
        "y_unit": "",
        "descr": "SEC trace (by elution volume)",
    },
    "mwd": {
        "x": "molecular weight",
        "x_unit": "g/mol",
        "y": "population",
        "y_unit": "mol frac",
        "descr": "molecular weight distribution (by mole)",
    },
    "mwd_wt": {
        "x": "molecular weight",
        "x_unit": "g/mol",
        "y": "population",
        "y_unit": "wt frac",
        "descr": "molecular weight distribution (by weight)",
    },
    "nmr": {
        "x": "time",
        "x_unit": "us",
        "y": "voltage",
        "y_unit": "V",
        "descr": "Free induction decay",
    },
    "nmr_h1": {
        "x": "chemical shift",
        "x_unit": "ppm",
        "y": "signal",
        "y_unit": "",
        "descr": "proton NMR (H1 NMR)",
    },
    "nmr_c13": {
        "x": "chemical shift",
        "x_unit": "ppm",
        "y": "signal",
        "y_unit": "",
        "descr": "carbon NMR (C13 NMR)",
    },
    "nmr_n15": {
        "x": "chemical shift",
        "x_unit": "ppm",
        "y": "signal",
        "y_unit": "",
        "descr": "nitrogen NMR (N15 NMR)",
    },
    "nmr_o17": {
        "x": "chemical shift",
        "x_unit": "ppm",
        "y": "signal",
        "y_unit": "",
        "descr": "oxygen NMR (O17 NMR)",
    },
    "nmr_f19": {
        "x": "chemical shift",
        "x_unit": "ppm",
        "y": "signal",
        "y_unit": "",
        "descr": "fluorine NMR (F19 NMR)",
    },
    "nmr_si29": {
        "x": "chemical shift",
        "x_unit": "ppm",
        "y": "signal",
        "y_unit": "",
        "descr": "silicon NMR (Si29 NMR)",
    },
    "nmr_p31": {
        "x": "chemical shift",
        "x_unit": "ppm",
        "y": "signal",
        "y_unit": "",
        "descr": "phosphorous NMR (P31 NMR)",
    },
    "nmr_noe": {
        "x": "chemical shift",
        "x_unit": "ppm",
        "y": "signal",
        "y_unit": "",
        "descr": "nuclear Overhauser effect NMR",
    },
    "nmr_tocsy": {
        "x": "chemical shift",
        "x_unit": "ppm",
        "y": "signal",
        "y_unit": "",
        "descr": "total correlation spectroscopy NMR",
    },
    "ir": {
        "x": "wavenumber",
        "x_unit": "cm**-1",
        "y": "signal",
        "y_unit": "",
        "descr": "infrared spectroscopy",
    },
    "stess_strain": {
        "x": "stess",
        "x_unit": "kPa",
        "y": "strain",
        "y_unit": "",
        "descr": "stress strain curve",
    },
    "waxs": {
        "x": "q",
        "x_unit": "angstrom**-1",
        "y": "signal",
        "y_unit": "",
        "descr": "wide angle light scattering",
    },
    "saxs": {
        "x": "q",
        "x_unit": "angstrom**-1",
        "y": "signal",
        "y_unit": "",
        "descr": "small angle light scattering",
    },
    "g_prime": {
        "x": "frequency",
        "x_unit": "rad/s",
        "y": "stress",
        "y_unit": "Pa",
        "descr": "storage modulus",
    },
    "g_doub_prime": {
        "x": "frequency",
        "x_unit": "rad/s",
        "y": "stress",
        "y_unit": "Pa",
        "descr": "loss modulus",
    },

    # 3D data
    "photo": {
        "x": "",
        "x_unit": "",
        "y": "",
        "y_unit": "",
        "z": "",
        "z_unit": "",
        "descr": "Generic Photograph",
    },
    "nmr_cosy": {
        "x": "chemical shift",
        "x_unit": "ppm",
        "y": "chemical shift",
        "y_unit": "ppm",
        "z": "signal",
        "z_unit": "",
        "descr": "correlation spectroscopy NMR (H - H)",
    },
    "nmr_hsqc": {
        "x": "chemical shift",
        "x_unit": "ppm",
        "y": "chemical shift",
        "y_unit": "ppm",
        "z": "signal",
        "z_unit": "",
        "descr": "heteronuclear single-quantum correlation spectroscopy NMR (H - C)",
    },
    "nmr_hmbc": {
        "x": "chemical shift",
        "x_unit": "ppm",
        "y": "chemical shift",
        "y_unit": "ppm",
        "z": "signal",
        "z_unit": "",
        "descr": "heteronuclear multiple-bond correlation spectroscopy NMR (H - C)",
    },
    "nmr_dosy": {
        "x": "chemical shift",
        "x_unit": "ppm",
        "y": "diffusion coefficient",
        "y_unit": "m**2/s",
        "z": "signal",
        "z_unit": "",
        "descr": "Diffusion NMR",
    },
    "nmr_kinetic": {
        "x": "chemical shift",
        "x_unit": "ppm",
        "y": "time",
        "y_unit": "min",
        "z": "signal",
        "z_unit": "",
        "descr": "NMR kinetic array",
    },
    "waxs_i": {
        "x": "distance",
        "x_unit": "nm**-1",
        "y": "distance",
        "y_unit": "nm**-1",
        "z": "signal",
        "z_unit": "",
        "descr": "wide angle light scattering image",
    },
    "saxs_i": {
        "x": "distance",
        "x_unit": "nm**-1",
        "y": "distance",
        "y_unit": "nm**-1",
        "z": "signal",
        "z_unit": "",
        "descr": "small angle light scattering image",
    },
    "s_neutron": {
        "x": "distance",
        "x_unit": "nm**-1",
        "y": "distance",
        "y_unit": "nm**-1",
        "z": "signal",
        "z_unit": "",
        "descr": "small angle neutron scattering image",
    },
    "tem_height": {
        "x": "distance",
        "x_unit": "nm",
        "y": "distance",
        "y_unit": "nm",
        "z": "height",
        "z_unit": "nm",
        "descr": "transmission electron microscopy height map",
    },
    "afm_height": {
        "x": "distance",
        "x_unit": "nm",
        "y": "distance",
        "y_unit": "nm",
        "z": "height",
        "z_unit": "nm",
        "descr": "atomic force microscope height map",
    },
    "afm_amp": {
        "x": "distance",
        "x_unit": "nm",
        "y": "distance",
        "y_unit": "nm",
        "z": "amplitude",
        "z_unit": "nm",
        "descr": "atomic force microscope amplitude map",
    },
    "afm_phase": {
        "x": "distance",
        "x_unit": "nm",
        "y": "distance",
        "y_unit": "nm",
        "z": "phase",
        "z_unit": "deg",
        "descr": "atomic force microscope phase map",
    },

    # n-D data
    # "": {
    #     "labels": ["", "", "", ""],
    #     "units": ["", "", "", ""],
    #     "descr": "atomic force microscope phase map",
    # }
}