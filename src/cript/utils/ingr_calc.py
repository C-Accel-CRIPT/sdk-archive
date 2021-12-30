from typing import Union
from warnings import warn
from difflib import SequenceMatcher

from .. import Quantity, Unit, float_limit


quantity_keys = {
    "mass": {
        "type": float,
        "range": [0, float_limit],
        "unit": "g",
        "descr": "mass"
    },
    "volume": {
        "type": float,
        "range": [0, float_limit],
        "unit": "ml",
        "descr": "volume"
    },
    "pressure": {
        "type": float,
        "range": [0, float_limit],
        "unit": "kPa",
        "descr": "pressure"
    },
    "mole": {
        "type": float,
        "range": [0, float_limit],
        "unit": "mmole",
        "descr": "mole"
    }
}

relative_quantity_keys = {
    "equivalence": {
        "type": float,
        "range": [0, float_limit],
        "unit": "",
        "descr": "equivalence"
    },
    "molarity": {
        "type": float,
        "range": [0, float_limit],
        "unit": "M",
        "descr": "molarity"
    },
    "mass_fraction": {
        "type": float,
        "range": [0, 1],
        "unit": "",
        "descr": "mass fraction"
    }
}


class IngrCalculatorError(Exception):
    def __init__(self, *msg):
        super().__init__(*msg)


class QuantityCalculator:
    """
    Material data structure:
    {
            # required
        "name": str,

            # provide one of these
        "mass": Quantity,
        "volume": Quantity,
        "mole": Quantity,
        "pressure": Quantity,

            # will be used for calculations
        "density": Quantity,
        "conc_molar": Quantity,
        "molar_mass": Quantity,

        other key-value pairs will be ignored
    }
    """
    keys_calc = None
    keys_qty = quantity_keys
    keys_rel = relative_quantity_keys
    keys = None
    _error = IngrCalculatorError

    def __init__(self):
        self._init_()

    def calc_mass_volume_mole(self, mat: dict) -> dict:
        self._mat_check(mat)

        if "pressure" in mat.keys() and mat["pressure"] is not None:
            return mat  # nothing to be done with pressure

        if "mass" in mat.keys():
            if "density" in mat.keys():
                volume = self._mass_to_volume(mat["mass"], mat["density"])
                self._approx_same_in_dict(mat, volume, "volume")
                mat["volume"] = volume
            if "molar_mass" in mat.keys():
                mole = self._mass_to_mole(mat["mass"], mat["molar_mass"])
                self._approx_same_in_dict(mat, mole, "mole")
                mat["mole"] = mole

        elif "mole" in mat.keys():
            if "conc_molar" in mat.keys():
                volume = self._mole_to_volume(mat["mole"], mat["conc_molar"])
                self._approx_same_in_dict(mat, volume, "volume")
                mat["volume"] = volume
            if "molar_mass" in mat.keys():
                mass = self._mole_to_mass(mat["mole"], mat["molar_mass"])
                self._approx_same_in_dict(mat, mass, "mass")
                mat["mass"] = mass
            if "density" in mat.keys() and "mass" in mat.keys():
                volume = self._mass_to_volume(mat["mass"], mat["density"])
                self._approx_same_in_dict(mat, volume, "volume")
                mat["volume"] = volume

        elif "volume" in mat.keys():
            if "conc_molar" in mat.keys():
                mole = self._vol_to_mole_conc(mat["volume"], mat["conc_molar"])
                self._approx_same_in_dict(mat, mole, "mole")
                mat["mole"] = mole
            elif "density" in mat.keys():
                mass = self._vol_to_mass(mat["volume"], mat["density"])
                self._approx_same_in_dict(mat, mass, "mass")
                mat["mass"] = mass
                if "molar_mass" in mat.keys():
                    mole = self._mass_to_mole(mat["mass"], mat["molar_mass"])
                    self._approx_same_in_dict(mat, mole, "mole")
                    mat["mole"] = mole

        return mat

    @staticmethod
    def scale(mat: dict, factor: Union[int, float]) -> dict:
        if "pressure" in mat.keys() and mat["pressure"] is not None:
            mat["pressure"] = mat["pressure"] * factor

        keys = ["mass", "mole", "volume"]
        for k in keys:
            if k in mat.keys():
                mat[k] = mat[k] * factor

        return mat

    def _mat_check(self, mat):
        """ Check all values in material dict for correct unit dimensions and range."""
        if self.keys is None:
            self._init_()

        keys = [k for k in self.keys.keys() if k in mat.keys()]
        for k in keys:
            self._unit_and_range_check(mat[k])

    def _unit_and_range_check(self, qty: Quantity):
        """ Checks to make sure value is in the acceptable range."""
        key = self._qty_to_key(qty)
        range_ = self.keys[key]["range"]
        unit_ = self.keys[key]["unit"]
        self._unit_check(qty, Unit(unit_), key)
        if range_[0] <= qty.to(unit_).magnitude <= range_[1]:
            return
        else:
            mes = f"{key} outside valid range. Valid range: {range_} {unit_}; Received: {qty.to(unit_)} ({qty})"
            raise self._error(mes)

    def _qty_to_key(self, qty: Quantity) -> str:
        """Given a qty, use the units to find dict key in self.key and self.keys_calc"""
        if self.keys is None:
            self._init_()

        result = [k for k, v in self.keys.items() if self._unit_check_bool(qty, Unit(v["unit"]))]
        if result is []:
            mes = f"{qty} has no corresponding key. See Qty_key or Calc_key."
            raise self._error(mes)

        return result[0]

    def _unit_check(self, value: Quantity, expected: Unit, name: str):
        """ Checks to make sure unit dimensionality is correct"""
        if value.dimensionality != expected.dimensionality:
            mes = f"Invalid {name} dimensionality. Expected: {expected.dimensionality}, " \
                  f"Received: {value.dimensionality}."
            raise self._error(mes)

    def _unit_check_bool(self, value: Quantity, expected: Unit) -> True:
        """ Checks to make sure unit dimensionality is correct"""
        try:
            self._unit_check(value, expected, "")
            return True
        except self._error:
            return False

    def _approx_same(self, qty1: Quantity, qty2: Quantity, error: float = 0.01) -> bool:
        """Checks if two quantities are approximately the same"""
        if qty1.dimensionality == qty2.dimensionality:
            if abs((qty1 - qty2) / qty1) < error:
                return True
            else:
                return False
        else:
            mes = f"Dimensions don't match. {qty1.dimensionality}, {qty2.dimensionality}"
            raise self._error(mes)
        
    def _approx_same_in_dict(self, mat: dict, qty: Quantity, param: str):
        if param in mat.keys():
            if not self._approx_same(mat[param], qty):
                mes = f"Calculated '{param}' don't match the given one. Calculated: {qty}, Given: {mat[param]}"
                raise self._error(mes)

    @staticmethod
    def _vol_to_mass(volume: Quantity, density: Quantity) -> Quantity:
        """ Returns mass"""
        return volume * density

    @staticmethod
    def _mass_to_volume(mass: Quantity, density: Quantity) -> Quantity:
        """ Returns volume"""
        return mass / density

    @staticmethod
    def _mass_to_mole(mass: Quantity, molar_mass: Quantity) -> Quantity:
        """ Returns mole"""
        return mass / molar_mass

    @staticmethod
    def _mole_to_mass(mole: Quantity, molar_mass: Quantity) -> Quantity:
        """ Returns mass"""
        return mole * molar_mass

    @staticmethod
    def _vol_to_mole_conc(volume: Quantity, molarity: Quantity) -> Quantity:
        """ Returns moles"""
        return volume * molarity

    @staticmethod
    def _mole_to_volume(mole: Quantity, molarity: Quantity) -> Quantity:
        """ Returns volume"""
        return mole / molarity

    @staticmethod
    def _mole_to_equiv(mole: Quantity, base: Quantity) -> Quantity:
        """ Returns equivalence"""
        return mole / base

    @classmethod
    def _init_(cls):
        from cript.keys.prop import property_material_keys
        calc_names = ["density", "conc_molar", "molar_mass"]
        cls.keys_calc = {k: property_material_keys[k] for k in calc_names}
        cls.keys = cls.keys_qty | cls.keys_rel | cls.keys_calc


class RelativeCalculator:
    _error = IngrCalculatorError
    default_density = 1 * Unit("g/ml")
    """
    Material data structure:
    {
            # required
        "name": str,

            # provide  these
        "mass": Quantity,
        "volume": Quantity,
        "mole": Quantity,
        "pressure": Quantity,
        
            # these will be calculated
        "equivalence": Quantity,
        "molarity": Quantity,
        "mass_fraction": Quantity,

            # will be used for calculations
        "density": Quantity,

        "keywords": str   # used to calculate base

        other key-value pairs will be ignored
    }
    """
    def calc_equiv_molarity_mass_fraction(self, mats: list[dict], defaults=True) -> list[dict]:
        """
        Calculates equivalence, molarity and mass fraction if possible
        """
        mats = self._calc_equivalence(mats)
        mats = self._calc_molarity(mats, defaults)
        mats = self._calc_mass_fraction(mats, defaults)

        return mats

    def _calc_equivalence(self, mats: list[dict]) -> list[dict]:
        """ Calculates molar equivalence for all materials with moles."""
        if not self._check_calc_possible(mats, "mole"):
            return mats

        base = self._get_mole_basis(mats)
        for i_, i in enumerate(mats):
            if "mole" in i.keys():
                mats[i_]["equivalence"] = i["mole"] / mats[base]["mole"]

        return mats

    @staticmethod
    def _check_calc_possible(mats, key: str, required_num: int = 2) -> bool:
        """ Needs at least 2 materials to calculate relative quantities."""
        gas_mat = len([True for mat in mats if "pressure" in mat.keys() and mat["pressure"] is not None])
        adjusted_num = max([2, required_num-gas_mat])
        if len([True for mat in mats if key in mat.keys()]) >= adjusted_num:
            return True
        else:
            return False

    @staticmethod
    def _get_mole_basis(mats) -> int:
        """ Returns the index for the material that is the base."""
        base = None
        fall_back_base = None
        for index, i in enumerate(mats):
            if "mole" in i.keys():
                if "keyword" in i.keys():
                    if i["keyword"] == "initiator":
                        base = index
                        break
                    elif i["keyword"] == "catalyst":
                        base = index
                elif "equivalence" in i.keys() and i["equivalence"] == 1:
                    base = index

                if fall_back_base is None:
                    fall_back_base = index

        if base is None:
            base = fall_back_base

        return base

    def _calc_molarity(self, mats: list[dict], default: bool) -> list[dict]:
        if not self._check_calc_possible(mats, "volume", len(mats)):
            if default:
                pass
            else:
                return mats

        total_volume, mat_skipped = self._get_total_volume(mats, default)

        for i_, i in enumerate(mats):
            if "mole" in i.keys() and i["name"] not in mat_skipped:
                mats[i_]["molarity"] = i["mole"] / total_volume

        return mats

    def _get_total_volume(self, mats, default: bool):
        total_volume = 0
        mat_skipped = []
        for i in mats:
            if "keyword" in i.keys():
                if i["keyword"] in ["workup", "quench"]:
                    mat_skipped.append(i['name'])
                    continue
            if "volume" in i.keys():
                total_volume += i["volume"]
            elif default:
                if "mass" in i.keys():
                    total_volume += i["mass"] / self.default_density
                    warn(f"Default density used for '{i['name']}' when calculating molarity.")
            else:
                mat_skipped.append(i['name'])
                warn(f"'{i['name']}' not included in molarity calculation.")

        return total_volume, mat_skipped

    def _calc_mass_fraction(self, mats: list[dict], default: bool) -> list[dict]:
        if not self._check_calc_possible(mats, "mass", len(mats)):
            if default:
                pass
            else:
                return mats

        total_mass, mat_skipped = self._get_total_mass(mats, default)
        
        for i_, i in enumerate(mats):
            if "mass" in i.keys() and i["name"] not in mat_skipped:
                mats[i_]["mass_fraction"] = i["mass"] / total_mass
    
        return mats

    def _get_total_mass(self, mats, default: bool):
        total_mass = 0
        mat_skipped = []
        for i in mats:
            if i["keyword"] in ["workup", "quench"]:
                mat_skipped.append(i['name'])
                continue
            if "mass" in i.keys():
                total_mass += i["mass"]
            elif default:
                if "volume" in i.keys():
                    total_mass += i["volume"] * self.default_density
                    warn(f"Default density used for '{i['name']}' when calculating mass fraction.")
            else:
                mat_skipped.append(i['name'])
                warn(f"'{i['name']}' not included in mass fraction calculation.")

        return total_mass, mat_skipped


class IngredientCalculator:
    _error = IngrCalculatorError
    _label_length = 12

    def __init__(self, *args):
        """
        Functions: add, remove, scale, scale_one
        __init__ calls add

        :param see add function
        """

        self._ingr = []
        self._q_calc = QuantityCalculator()
        self._r_calc = RelativeCalculator()

        self._init_with_args(*args)

    def __repr__(self):
        return self._table()

    def __str__(self):
        return self._table()

    def __call__(self):
        return self._ingr

    def __len__(self):
        return len(self._ingr)

    def __getitem__(self, item):
        index = self._get_mat_index(item)
        return self._ingr[index]

    def __iter__(self):
        for ingr in self._ingr:
            yield ingr

    def _init_with_args(self, *args):
        if args:
            for arg in args[0]:
                # get keyword arguments
                kwarg = {}
                for i, a in enumerate(arg):
                    if isinstance(a, dict) and len(a.keys()) == 1:
                        kwarg = kwarg | arg.pop(i)

                try:
                    self.add(*arg, **kwarg)
                except KeyError as e:
                    warn(f"Material skipped: '{arg}'. {e}")

    def add(self, mat: dict, equivalence: list[Union[float, int], Union[int, str]] = None):
        """
        Adds mat to Ingr and performs calculations for the other quantities.
        :param mat:
        :param equivalence: [equivalence, "material"] "material" is the equivalence is in respect to
        """
        if equivalence is not None:
            index = self._get_mat_index(equivalence[1])
            if "mole" in self._ingr[index].keys():
                mat["mole"] = self._ingr[index]["mole"] * equivalence[0]
            else:
                mes = f"The equivalence material({self._ingr[index]['name']}) has no moles."
                raise self._error(mes)

        self._ingr.append(self._q_calc.calc_mass_volume_mole(mat))
        self._ingr = self._r_calc.calc_equiv_molarity_mass_fraction(self._ingr)

    def remove(self, mat: Union[int, str]):
        """
        Removes mat from ingr
        :param mat: material to be removed
        """
        if isinstance(mat, int) and mat <= len(self._ingr):
            del self._ingr[mat]
        elif isinstance(mat, str):
            mat = self._get_mat_index(mat)
            del self._ingr[mat]
        else:
            mes = f"'{mat}' invalid input."
            raise self._error(mes)

        self._ingr = self._r_calc.calc_equiv_molarity_mass_fraction(self._ingr)

    def scale(self, factor: Union[int, float]):
        """
        Scales all ingredients' mass, volume, moles by a factor.
        :param factor: scale factor
        """
        for i in range(len(self._ingr)):
            self._ingr[i] = self._q_calc.scale(self._ingr[i], factor)

    def scale_one(self, mat: Union[int, str], factor: Union[int, float]):
        """
        Scales one ingredient's mass, volume, moles by a factor.
        :param mat: material to be scaled
        :param factor: scale factor
        """
        index = self._get_mat_index(mat)

        self._ingr[index] = self._q_calc.scale(self._ingr[index], factor)
        self._ingr = self._r_calc.calc_equiv_molarity_mass_fraction(self._ingr)

    def _get_mat_index(self, target: Union[str, int]):
        if isinstance(target, int):
            if target <= len(self._ingr):
                return target

        possible_names = [i["name"] for i in self._ingr]
        scores = {v: SequenceMatcher(None, target, v).ratio() * 100 for v in possible_names}
        best_match = max(scores, key=scores.get)
        best_score = scores[best_match]
        if best_score < 75:
            mes = f"No match to '{target}' found in ingredients. Try a different writing of the chemical name."
            raise self._error(mes)

        return possible_names.index(best_match)

    def _table(self) -> str:
        """
        Creates a nice viewable table.
        """
        if len(self._ingr) == 0:
            return "No ingredients."

        headers, units = self._table_headers()
        headers.insert(0, "#")
        units.insert(0, "")
        row_format = "{:<3}" + ("{:<" + str(self._label_length) + "}") * (len(headers)-1)
        text_out = row_format.format(*[self._length_limit_header(h) for h in headers])
        text_out += "\n" + row_format.format(*[f"({u})" if u != "" else "" for u in units])
        text_out += "\n" + "-" * self._label_length * len(headers)
        for i, ingr in enumerate(self._ingr):
            entries = []
            for k, u in zip(headers, units):
                if k in ingr.keys():
                    v = ingr[k]
                    if u != "":
                        value = self.sig_figs(v.to(u).m)
                    elif isinstance(v, Quantity):
                        value = self.sig_figs(v.to_base_units().m)
                    else:
                        value = str(v)
                    entries.append(self._length_limit_header(value))
                elif k == "#":
                    entries.append(f"{i}")
                else:
                    entries.append("---")

            text_out += "\n" + row_format.format(*entries)

        text_out += "\n" * 2
        return text_out

    def _table_headers(self):
        headers = []
        back_headers = []
        units = []
        back_units = []
        divide = 0
        divide2 = 0
        for ingr in self._ingr:
            for k in ingr.keys():
                if k not in headers + back_headers:
                    if k == "name":
                        headers.insert(0, k)
                        units.insert(0, "")
                        divide += 1
                    elif k in self._q_calc.keys_qty.keys():
                        headers.insert(divide, k)
                        units.insert(divide, self._q_calc.keys_qty[k]["unit"])
                        divide += 1
                    elif k in self._q_calc.keys_rel.keys():
                        headers.insert(divide + divide2, k)
                        units.insert(divide + divide2, self._q_calc.keys_rel[k]["unit"])
                        divide2 += 1
                    elif k in self._q_calc.keys_calc.keys():
                        headers.insert(divide + divide2 + 1, k)
                        units.insert(divide + divide2 + 1, self._q_calc.keys_calc[k]["unit"])
                    else:
                        back_headers.append(k)
                        back_units.append("")

        return headers + back_headers, units + back_units

    def _length_limit_header(self, entry) -> str:
        length_limit = self._label_length
        if len(entry) > length_limit:
            return entry[0:length_limit - 2]

        return entry

    @staticmethod
    def sig_figs(number: float, significant_figures: int = 3) -> str:
        """
        Given a number return a string rounded to the desired significant digits.
        :param number:
        :param significant_figures:
        :return:
        """
        try:
            return '{:g}'.format(float('{:.{p}g}'.format(number, p=significant_figures)))
        except Exception:
            return str(number)


# if __name__ == "__main__":
#     from cript import Quantity, Unit
#     from cript.keys.process import Qty_keys, Rel_Qty_keys
#     calc = IngredientCalculator()
#     calc.add({
#         "name": "secbuLi",
#         "volume": 0.0172 * Unit("ml"),
#         "molar_mass": 64.06 * Unit("g/mol"),
#         "density": 0.768 * Unit("g/ml"),
#         "conc_molar": 1.3 * Unit("M")
#     })
#     calc.add({
#         "name": "styrene",
#         "mass": 0.455 * Unit("g"),
#         "molar_mass": 104.15 * Unit("g/mol"),
#         "density": 0.909 * Unit("g/ml")
#     })
#     calc.add({
#         "name": "toluene",
#         "volume": 10 * Unit("ml"),
#         "molar_mass": 92.141 * Unit("g/mol"),
#         "density": 0.87 * Unit("g/ml")
#     })
#     calc.add({
#         "name": "THF",
#         "mole": 45.545 * Unit("mmol"),
#         "molar_mass": 72.107 * Unit("g/mol"),
#         "density": .8876 * Unit("g/ml"),
#     })
#     print(calc)
#     calc.scale(2)
#     print(calc)
#     calc.remove("toluene")
#     print(calc)
#     calc.scale_one("styrene", 0.5)
#     print(calc)
