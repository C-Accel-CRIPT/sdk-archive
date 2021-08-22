
from .. import Quantity, Unit, CRIPTError, CRIPTWarning
from ..keys.process import Qty_keys

default_density = 1 * Unit("g/ml")

class UnitError(Exception):
    def __init__(self, opt1, opt2=None):
        if opt2 is None:
            self.message = opt1
        else:
            self.message = f"Units not same dimensions. {opt1}:{opt1.dimensionality} ; {opt2}:{opt2.dimensionality}"


def unit_to_qty_key(qty: Quantity) -> str:
    """Given a qty, use the units to find dict key."""
    return [k for k, v in Qty_keys.items() if unit_check_bool(qty, Unit(v["unit"]))][0]


def unit_check_bool(value: Quantity, expected: Unit) -> True:
    """ Checks to make sure unit dimensionality is correct"""
    try:
        _unit_check(value, expected, "")
        return True
    except UnitError:
        return False


def _unit_check(value: Quantity, expected: Unit, name: str):
    """ Checks to make sure unit dimensionality is correct"""
    if value.dimensionality != expected.dimensionality:
        mes = f"Invalid {name} dimensionality. Expected: {expected.dimensionality}, Received: {value.dimensionality}."
        raise UnitError(mes)


def _range_check(qty: Quantity):
    """ Checks to make sure value is in the acceptable range."""
    key = unit_to_qty_key(qty)
    range_ = Qty_keys[key]["range"]
    unit_ = Qty_keys[key]["unit"]
    if range_[0] <= qty.to(unit_).magnitude <= range_[1]:
        return
    else:
        mes = f"{key} outside valid range. Valid range: {range_} {unit_}; Received: {qty.to(unit_)} ({qty})"
        raise CRIPTError(mes)


def approx_same(qty1: Quantity, qty2: Quantity) -> bool:
    """Checks if two quantities are approximately the same"""
    if qty1.dimensionality == qty2.dimensionality:
        if abs((qty1 - qty2)/qty1) < 0.02:
            return True
        else:
            return False
    else:
        raise UnitError(qty1, qty2)


def vol_to_mass(vol: Quantity, density: Quantity) -> Quantity:
    """ Returns mass"""
    _unit_check(vol, Unit("ml"), "volume")
    _unit_check(density, Unit("g/ml"), "density")
    return vol * density


def mass_to_vol(mass: Quantity, density: Quantity) -> Quantity:
    """ Returns volume"""
    _unit_check(mass, Unit("g"), "mass")
    _unit_check(density, Unit("g/ml"), "density")
    return mass / density


def mass_to_mole(mass: Quantity, molar_mass: Quantity) -> Quantity:
    """ Returns mole"""
    _unit_check(mass, Unit("g"), "mass")
    _unit_check(molar_mass, Unit("g/mole"), "molar_mass")
    return mass / molar_mass


def mole_to_mass(mole: Quantity, molar_mass: Quantity) -> Quantity:
    """ Returns mass"""
    _unit_check(mole, Unit("mole"), "mole")
    _unit_check(molar_mass, Unit("g/mole"), "molar_mass")
    return mole * molar_mass


def vol_to_mole_conc(vol: Quantity, molarity: Quantity) -> Quantity:
    """ Returns moles"""
    _unit_check(vol, Unit("ml"), "volume")
    _unit_check(molarity, Unit("M"), "molarity")
    return vol * molarity


def mole_to_vol(mole: Quantity, molarity: Quantity) -> Quantity:
    """ Returns volume"""
    _unit_check(mole, Unit("mole"), "mole")
    _unit_check(molarity, Unit("M"), "molarity")
    return mole / molarity


def mole_to_equiv(mole: Quantity, base: Quantity) -> Quantity:
    """ Returns equivalence"""
    _unit_check(mole, Unit("mole"), "mole")
    _unit_check(base, Unit("mole"), "mole_base")
    return mole / base


def approx_same_in_dict(ingr: dict, qty: Quantity, param: str):
    if param in ingr.keys():
        if not approx_same(ingr[param], qty):
            mes = f"Calculated '{param}' don't match the given one. Calculated: {qty}, Given: {ingr[param]}"
            CRIPTError(mes)


def ingr_calc_mass_vol_mole(ingr: dict) -> dict:

    if "mass" in ingr.keys():
        if "density" in ingr.keys():
            vol = mass_to_vol(ingr["mass"], ingr["density"])
            _range_check(vol)
            approx_same_in_dict(ingr, vol, "vol")
            ingr["vol"] = vol
        if "molar_mass" in ingr.keys():
            mole = mass_to_mole(ingr["mass"], ingr["molar_mass"])
            _range_check(mole)
            approx_same_in_dict(ingr, mole, "mole")
            ingr["mole"] = mole

    elif "mole" in ingr.keys():
        if "conc" in ingr.keys():
            vol = mole_to_vol(ingr["mole"], ingr["conc"])
            _range_check(vol)
            approx_same_in_dict(ingr, vol, "vol")
            ingr["vol"] = vol
        if "molar_mass" in ingr.keys():
            mass = mole_to_mass(ingr["mole"], ingr["molar_mass"])
            _range_check(mass)
            approx_same_in_dict(ingr, mass, "mass")
            ingr["mass"] = mass
        if "density" in ingr.keys() and "mass" in ingr.keys():
            vol = mass_to_vol(ingr["mass"], ingr["density"])
            _range_check(vol)
            approx_same_in_dict(ingr, vol, "vol")
            ingr["vol"] = vol

    elif "vol" in ingr.keys():
        if "conc" in ingr.keys():
            mole = vol_to_mole_conc(ingr["vol"], ingr["conc"])
            _range_check(mole)
            approx_same_in_dict(ingr, mole, "mole")
            ingr["mole"] = mole
        if "density" in ingr.keys():
            mass = vol_to_mass(ingr["vol"], ingr["density"])
            _range_check(mass)
            approx_same_in_dict(ingr, mass, "mass")
            ingr["mass"] = mass
        if "molar_mass" in ingr.keys() and "mass" in ingr.keys():
            mole = mass_to_mole(ingr["mass"], ingr["molar_mass"])
            _range_check(mole)
            approx_same_in_dict(ingr, mole, "mole")
            ingr["mole"] = mole

    return ingr


def calc_equivalence(ingr: list[dict]) -> list[dict]:

    base_moles = None
    fall_back_base_moles = None
    for index, i in enumerate(ingr):
        if "keyword" in i.keys() and "mole" in i.keys():
            if i["keyword"] == "initiator":
                base_moles = i["mole"]
                break
            elif i["keyword"] == "catalyst":
                base_moles = i["mole"]
        if "mole" in i.keys():
            fall_back_base_moles = i["mole"]

    if base_moles is None:
        if fall_back_base_moles is None:
            mes = "No moles on any chemicals so can't calculate equivalence."
            CRIPTWarning(mes)
        else:
            base_moles = fall_back_base_moles

    for i_, i in enumerate(ingr):
        if "mole" in i.keys():
            ingr[i_]["equiv"] = i["mole"]/base_moles

    return ingr


def calc_molarity(ingr: list[dict]) -> list[dict]:
    total_vol = 0
    for i in ingr:
        if "vol" in i.keys():
            total_vol += i["vol"]
        elif "mass" in i.keys():
            total_vol += i["mass"]/default_density
        else:
            pass

    for i_, i in enumerate(ingr):
        if "mole" in i.keys():
            ingr[i_]["molarity"] = i["mole"] / total_vol

    return ingr


def calc_mass_frac(ingr: list[dict]) -> list[dict]:
    total_mass = 0
    for i in ingr:
        if "mass" in i.keys():
            total_mass += i["mass"]
        elif "vol" in i.keys():
            total_mass += i["vol"] * default_density
        else:
            pass

    for i_, i in enumerate(ingr):
        if "mass" in i.keys():
            ingr[i_]["mass_frac"] = i["mass"] / total_mass

    return ingr


def ingr_equiv_molarity_mass_frac(ingr: list[dict]) -> list[dict]:
    if len(ingr) <= 1:
        return ingr

    ingr = calc_equivalence(ingr)
    ingr = calc_molarity(ingr)
    ingr = calc_mass_frac(ingr)

    return ingr


def ingr_generator(ingr: list[dict], minus: list[str] = None):
    for i in ingr:
        if i["keyword"] not in minus:
            yield i
