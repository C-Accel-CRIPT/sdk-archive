
data_keys = {
    #### 1D data
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
        "x": "retention time ",
        "x_unit": "min",
        "y": "signal",
        "y_unit": "",
        "descr": "SEC trace (by retention time)",
    },
}


# `mwd`            | molecular weight  | g/mol         | population       | mol frac    | molecular weight distribution (by mole)
# `mwd_wt`         | molecular weight  | g/mol         | population       | wt frac     | molecular weight distribution (by weight)
# `sec_trace_vol`  | elution vol.      | ml            | signal           |             | SEC trace (by elution volume)
# `nmr`            | time              | us            | voltage          | V           | Free induction decay
# `nmr_h1`         | chemical shift    | ppm           | signal           |             | proton NMR (H1 NMR)
# `nmr_c13`        | chemical shift    | ppm           | signal           |             | carbon NMR (C13 NMR)
# `nmr_n15`        | chemical shift    | ppm           | signal           |             | nitrogen NMR (N15 NMR)
# `nmr_o17`        | chemical shift    | ppm           | signal           |             | oxygen NMR (O17 NMR)
# `nmr_f19`        | chemical shift    | ppm           | signal           |             | fluorine NMR (F19 NMR)
# `nmr_si29`       | chemical shift    | ppm           | signal           |             | silicon NMR (Si29 NMR)
# `nmr_p31`        | chemical shift    | ppm           | signal           |             | phosphorous NMR (P31 NMR)
# `nmr_noe`        | chemical shift    | ppm           | signal           |             | nuclear Overhauser effect NMR
# `nmr_tocsy`      | chemical shift    | ppm           | signal           |             | total correlation spectroscopy NMR
# `ir`             | wavenumber        | cm**-1        | signal           |             | infrared spectroscopy
# `stess_st`       | stess             | kPa           | strain           |             | stress strain curve
# `waxs`           | q                 | angstrom**-1  | intensity        |             | wide angle light scattering
# `saxs`           | q                 | angstrom**-1  | intensity        |             | small angle light scattering
# `g_prime`        | frequency         | rad/s         | stress           | Pa          | storage modulus
# `g_doub_prime`   | frequency         | rad/s         | stress           | Pa          | loss modulus
#
#
# #### 2D data
#
# `type`           | x-axis            | x-axis unit   | y-axis           | y-axis unit | z-axis           | z-axis unit | Description
# ------           |-------            | ---------     | -------          |---------    | -------          |---------    | --------
# `nmr_cosy`       | chemical shift    | ppm           | chemical shift   | ppm         | signal           |             | correlation spectroscopy NMR (H - H)
# `nmr_hsqc`       | chemical shift    | ppm           | chemical shift   | ppm         | signal           |             | heteronuclear single-quantum correlation spectroscopy NMR (H - C)
# `nmr_hmbc`       | chemical shift    | ppm           | chemical shift   | ppm         | signal           |             | heteronuclear multiple-bond correlation spectroscopy NMR (H - C)
# `nmr_dosy`       | chemical shift    | ppm           | diffusion coeff. | m**2/s      | signal           |             | Diffusion NMR
# `nmr_kinetics`   | chemical shift    | ppm           | time             | min         | signal           |             | NMR kinetic array
# `waxs_i`         | distance          | nm**-1        | distance         | nm**-1      | signal           |             | wide angle light scattering image
# `saxs_i`         | distance          | nm**-1        | distance         | nm**-1      | signal           |             | small angle light scattering image
# `s_neutron`      | distance          | nm**-1        | distance         | nm**-1      | signal           |             | small angle neutron scattering image
# `tem_height`     | distance          | nm            | distance         | nm          | height           | nm          | Transmission electron microscopy height map
# `afm_height`     | distance          | nm            | distance         | nm          | height           | nm          | Atomic Force Microscope height map
# `afm_amp`        | distance          | nm            | distance         | nm          | amplitude        | nm          | Atomic Force Microscope amplitude map
# `afm_phase`      | distance          | nm            | distance         | nm          | phase            | deg         | Atomic Force Microscope phase map
#
#
# #### n-D data
#
# `type`         | x-axis            | x-axis unit   | y-axis           | y-axis unit | Description
# ------         |-------            | ---------     | -------          |---------    | --------
#
#
# #### Other data
#
# `type`         | Description
# ------         |-------
# `photo`        | general images
