"""
Process Node

"""
from typing import Union
from warnings import warn

from fuzzywuzzy import process

from . import Unit, Quantity, CRIPTError
from .cond import Cond
from .prop import Prop
from .material import Material
from .base import BaseModel, load
from .utils.printing import KeyPrinting
from .keys.process import Ingr_keys, Qty_keys, Process_keys
from .utils.ingr_calc import unit_check_bool, ingr_calc_mass_vol_mole, unit_to_qty_key, \
    ingr_equiv_molarity_mass_frac, scale_one


class ProcessError(CRIPTError):
    def __init__(self, *msg):
        super().__init__(*msg)


class IngrError(CRIPTError):
    def __init__(self, *msg):
        super().__init__(*msg)


class Ingr(KeyPrinting):
    keys = Ingr_keys
    keys_Qty = Qty_keys
    _error = IngrError

    def __init__(self, *args, **kwargs):
        """
        Functions: add, remove, scale, scale_one
        __init__ calls add

        :param see add function
        """

        self._ingr = []

        # Load existing ingr
        # if _key:
        #     value = self._loading(value, uncer)

        # add ingrs
        for arg in args:
            kwarg = {}
            if isinstance(arg, list):
                for i, a in enumerate(arg):  # get keyword arguments
                    if isinstance(a, dict) and len(a.keys()) == 1:
                        kwarg = kwarg | arg.pop(i)
                self.add(*arg, **kwarg)

    def __repr__(self):
        return self._table()

    def __str__(self):
        return self._table()

    def add(self, mat: Union[Material], qty: Union[int, float, Quantity], keyword: str = None,
            eq_mat=None, mat_id=None):
        """
        Adds mat to Ingr and performs calculations for the other quantities.
        :param mat:
        :param qty:
        :param keyword:
        :param eq_mat:
        :param mat_id:
        :return:
        """

        # check if Material is valid input
        if isinstance(mat, Material):
            mat_ref = mat.reference()
        elif isinstance(mat, dict) and "class_" in mat.keys() and isinstance(node := load(mat), Material):
            mat = node
            mat_ref = mat.reference()
        else:
            mes = "Invalid 'mat'"
            raise self._error(mes)

        # check if Material already added
        if mat_ref["uid"] in [i["uid"] for i in self._ingr]:
            mes = f"'{mat_ref['name']}' is already an ingredient."
            raise self._error(mes)

        # Add material
        new_ingr = mat_ref

        # Add material properties
        new_ingr = new_ingr | self._get_mat_prop(mat, mat_id)

        # Add keywords
        if keyword in self.keys.keys():
            new_ingr["keyword"] = keyword
        else:
            mes = f"'{keyword}' is an invalid keyword. Valid keywords are: {list[self.keys.keys()]}"
            raise self._error(mes)

        # Add mass, vol, mole
        if isinstance(qty, Quantity) and unit_check_bool(qty, Unit("kPa")) and eq_mat is None:
            new_ingr["pres"] = qty
            self._ingr.append(new_ingr)

        elif isinstance(qty, Quantity) and eq_mat is None:
            key = unit_to_qty_key(qty)
            new_ingr[key] = qty
            new_ingr = ingr_calc_mass_vol_mole(new_ingr)
            self._ingr.append(new_ingr)
            self._ingr = ingr_equiv_molarity_mass_frac(self._ingr)

        elif isinstance(qty, (float, int)) and eq_mat is not None:
            if isinstance(eq_mat, int):  # given the material index
                qty = self._ingr[eq_mat]["mole"] * qty
            elif isinstance(eq_mat, str):  # get material index based on name
                mat_index = self.get_mat_index(eq_mat)
                qty = self._ingr[mat_index]["mole"] * qty
            elif isinstance(eq_mat, Material):
                target = eq_mat.name
                mat_index = self.get_mat_index(target)
                qty = self._ingr[mat_index]["mole"] * qty
            else:
                pass

            key = unit_to_qty_key(qty)
            new_ingr[key] = qty
            new_ingr = ingr_calc_mass_vol_mole(new_ingr)
            self._ingr.append(new_ingr)
            self._ingr = ingr_equiv_molarity_mass_frac(self._ingr)

        else:
            mes = "Invaid"
            raise self._error(mes)

    def remove(self, mat: Union[int, str]):
        """
        Removes mat from ingr
        :param mat: material to be removed
        """
        if isinstance(mat, int) and mat <= len(self._ingr):
            del self._ingr[mat]
        elif isinstance(mat, str):
            mat = self.get_mat_index(mat)
            del self._ingr[mat]
        else:
            mes = f"'{mat}' invalid"
            raise self._error(mes)

    def scale(self, factor: Union[int, float]):
        """
        Scales all ingredients' mass, volume, moles by a factor.
        :param factor: scale factor
        """
        for i in range(len(self._ingr)):
            self.scale_one(i, factor)

    def scale_one(self, mat: Union[int, str], factor: Union[int, float]):
        """
        Scales one ingredient's mass, volume, moles by a factor.
        :param mat: material to be scaled
        :param factor: scale factor
        """
        if isinstance(mat, int) and mat <= len(self._ingr):
            self._ingr[mat] = scale_one(self._ingr[mat], factor)
        elif isinstance(mat, str):
            mat = self.get_mat_index(mat)
            self._ingr[mat] = scale_one(self._ingr[mat], factor)

    def as_dict(self, **kwargs) -> list[dict]:
        out = []
        keys = ["uid", "name"] + list(self.keys_Qty.keys())
        for ingr in self._ingr:
            ingr_dict = {}
            for k in keys:
                if k in ingr.keys():
                    value = ingr[k]
                    if isinstance(value, Quantity):
                        value = value.to(self.keys_Qty[k]["unit"]).magnitude
                    ingr_dict[k] = value

            out.append(ingr_dict)

        return out

    @staticmethod
    def _get_mat_prop(mat, mat_id=None) -> dict:
        mat_prop = Ingr._get_prop_from_mat_id(mat, ["phase", "molar_mass", "m_n", "molar_conc", "density"])
        if mat_id is not None:
            if isinstance(mat_id, str):
                mat_id = mat._get_mat_id(mat_id)
            elif isinstance(mat_id, int) and mat_id in mat.iden.keys():
                pass  # Good mat_id provided
            else:
                mes = "Invalid mat_id."
                raise IngrError(mes)
            # this can add or overwrite bulk props
            mat_prop_2 = Ingr._get_prop_from_mat_id(mat, ["molar_mass", "m_n", "molar_conc", "density"], mat_id)
            if mat_prop_2 == {}:
                mes = f"'mat_id' for {mat.name} found no properties to assist with ingredient calculations."
                warn(mes)
            else:
                mat_prop = mat_prop | mat_prop_2

        return mat_prop

    @staticmethod
    def _get_prop_from_mat_id(mat: Material, prop: list[str], mat_id: str = "0") -> dict:
        out = {}
        mat_props = [[p.key, p.value] for p in mat.prop if p.mat_id == mat_id]
        for p in mat_props:
            if p[0] in prop:
                out[p[0]] = p[1]
        return out

    def _table(self) -> str:

        if len(self._ingr) == 0:
            return "No ingredients."

        headers = self._table_headers()
        row_format = ""
        for i in headers:
            row_format = row_format + self._label_length(i)
        text_out = row_format.format(*headers)
        text_out = text_out + "\n" + "-" * 150
        for ingr in self._ingr:
            entries = []
            for k in headers:
                if k in ingr.keys():
                    entries.append(self._length_limit(k, str(ingr[k])))
                else:
                    entries.append("-")

            text_out = text_out + "\n" + row_format.format(k, *entries)

        return text_out

    def _table_headers(self):
        headers = list(Qty_keys.keys())
        for ingr in self._ingr:
            for k in ingr.keys():
                if k not in headers:
                    headers.append(k)

        return headers

    def get_mat_index(self, target: str):
        names = [i["name"] for i in self._ingr]
        closest_name, score = process.extractOne(target, names,)
        if score < 0.5:
            mes = f"No match to '{target}' found in ingredients. Try a different writing of the chemical name."
            raise IngrError(mes)

        return names.index(closest_name)


class Process(KeyPrinting, BaseModel, _error=ProcessError):
    _class = "Process"
    keys = Process_keys

    def __init__(
            self,
            name: str,
            ingr: Ingr,
            procedure: str,
            cond: list[Cond],
            prop: list[Prop] = None,
            keywords: list[str] = None,
            notes: str = None,
            **kwargs
    ):
        """

        :param name: The name of the user.
        :param ingr:
        :param procedure:
        :param cond:
        :param prop:
        :param keywords:
        :param notes: Any miscellaneous notes related to the user.

        :param _class: class of node.
        :param uid: The unique ID of the material.
        :param model_version: Version of CRIPT data model.
        :param version_control: Link to version control node.
        :param last_modified_date: Last date the node was modified.
        :param created_date: Date it was created.
        """
        super().__init__(name=name, _class=self._class, notes=notes, **kwargs)

        self._ingr = None
        self.ingr = ingr

        self._procedure = None
        self.procedure = procedure

        self._prop = None
        self.prop = prop

        self._keywords = None
        self.keywords = keywords

        self._cond = None
        self.cond = cond

    @property
    def ingr(self):
        return self._ingr

    @ingr.setter
    def ingr(self, ingr):
        self._ingr = ingr

    @property
    def procedure(self):
        return self._procedure

    @procedure.setter
    def procedure(self, procedure):
        self._procedure = procedure

    @property
    def prop(self):
        return self._prop

    @prop.setter
    def prop(self, prop):
        self._prop = prop

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        self._keywords = keywords

    @property
    def cond(self):
        return self._cond

    @cond.setter
    def cond(self, cond):
        self._cond = cond
