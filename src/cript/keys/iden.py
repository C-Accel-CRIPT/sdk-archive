"""

identity keys

"""

import rxnpy.chemical.molecular_formula as rxnpy_


identifier_keys = {
    "mat_id": {
        "type": int,
        "validator": None,
        "descr": "id used for assigning properties"
    },
    "name": {
        "type": str,
        "validator": None,
        "descr": "preferred name"
    },
    "names": {
        "type": list[str],
        "validator": None,
        "descr": "additional names, abbreviations, short hands for the material"
    },
    "cas": {
        "type": str,
        "validator": None,
        "descr": "CAS number"
    },
    "bigsmiles": {
        "type": str,
        "validator": None,
        "descr": "bigSMILES Line Notation"
    },
    "smiles": {
        "type": str,
        "validator": None,
        "descr": "simplified molecular-input line-entry system (SMILES)"
    },
    "chem_formula": {
        "type": str,
        "validator": rxnpy_.MolecularFormula,
        "descr": "chemical formula"
    },
    "chem_repeat": {
        "type": str,
        "validator": rxnpy_.MolecularFormula,
        "descr": "chemical formula of repeating unit"
    },
    "pubchem_cid": {
        "type": int,
        "validator": None,
        "descr": "PubChem CID"
    },
    "inchi": {
        "type": str,
        "validator": None,
        "descr": "IUPAC International Chemical Identifier"
    },
    "inchi_key": {
        "type": str,
        "validator": None,
        "descr": "a hashed version of the full InChI"
    },
}