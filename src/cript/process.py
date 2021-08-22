"""
Process Node

"""
from typing import Union


from pint.errors import DimensionalityError

from . import BaseModel, Cond, Prop, Unit, Quantity, CRIPTError, CRIPTWarning, Material, load
from .utils.serializable import Serializable, SerializableSub
from .utils.printing import KeyPrinting
from .keys.process import *
from .utils.ingr_calc import unit_check_bool, ingr_calc_mass_vol_mole, unit_to_qty_key, ingr_equiv_molarity_mass_frac

# class Qty(SerializableSub, KeyPrinting):
#     keys = Qty_keys
#
#     def __init__(
#             self,
#             value: Union[Quantity, int, float],
#             uncer: Union[Quantity, int, float] = None,
#             equiv: str = None,
#             mat_uid: int = None,
#             _key: str = None
#     ):
#         """
#
#         :param value:
#         :param uncer:
#         """
#
#         self._equiv = None
#         self.equiv = equiv
#
#         self._mat_uid = None
#         self.mat_uid = mat_uid
#
#         self._value = None
#         self.value = value
#
#         self._uncer = None
#         self.uncer = uncer
#
#         self._key = None
#         if _key:
#             if isinstance(_key, str) and _key in self.keys.keys():
#                 self.key = _key
#         else:
#             self.key = self._get_key()
#
#     def __repr__(self):
#         return self._create_str()
#
#     def __str__(self):
#         return self._create_str()
#
#     @property
#     def value(self):
#         return self._value
#
#     @value.setter
#     def value(self, value):
#         if isinstance(value, (int, float)):
#             if self.equiv is None:
#                 mes = "You must add units or use 'equiv'."
#                 raise CRIPTError(mes)
#         self._value = value
#
#     @property
#     def uncer(self):
#         return self._uncer
#
#     @uncer.setter
#     def uncer(self, uncer):
#         self._uncer = uncer
#
#     @property
#     def equiv(self):
#         return self._equiv
#
#     @equiv.setter
#     def equiv(self, equiv):
#         self._equiv = equiv
#
#     @property
#     def mat_uid(self):
#         return self._mat_uid
#
#     @mat_uid.setter
#     def mat_uid(self, mat_uid):
#         self._mat_uid = mat_uid
#
#     @property
#     def key(self):
#         return self._key
#
#     @key.setter
#     def key(self, key):
#         self._key = key
#
#     def _loading(self, value, uncer):
#         return value, uncer
#
#     def _get_key(self) -> str:
#         """
#         It will use the units on self.value to determine the key for self.keys.
#         """
#         if isinstance(self.value, Quantity):
#             for k, v in self.keys.items():
#                 try:
#                     if u := v["unit"]:
#                         self.value.to(u)
#                     return k
#                 except DimensionalityError:
#                     pass
#
#     def _create_str(self) -> str:
#         """
#         Creates a nice string print out.
#         """
#         text_out = ""
#         if isinstance(self.value, Quantity):
#             text_out += f"{self.value.magnitude}"
#             if self.uncer is not None:
#                 text_out += f" +-{self.uncer.to(self.value.units).magnitude}"
#             text_out += f" {self.value.units}"
#
#         elif isinstance(self.value, (float, int)):
#             text_out += f"{self.value}"
#             if self.uncer is not None:
#                 text_out += f" +-{self.uncer}"
#             if self.equiv is not None:
#                 text_out += f" '{self.equiv}'"
#
#         if self.mat_uid is not None:
#             text_out += f" (mat: {self.mat_uid})"
#
#         return text_out


class Ingr(Serializable, KeyPrinting):
    keys = Ingr_keys
    keys_Qty = Qty_keys

    def __init__(
            self,
            *args,
            **kwargs
    ):
        """

        """

        # if _key:
        #     value = self._loading(value, uncer)

        self._ingr = []

        for arg in args:
            if isinstance(arg, list):
                self.add(*arg)

    def __repr__(self):
        return ""

    def __str__(self):
        return self.table()

    def add(
            self,
            mat: Union[Material],
            qty: Union[int, float, Quantity],
            keyword: str = None,
            eq_mat=None,
            mat_id=None,
            ):
        """

        :param mat:
        :param qty:
        :param keyword:
        :param eq_mat:
        :param mat_id:
        :return:
        """

        # check if Material is valid input
        if isinstance(mat, Material):
            mat_ref = mat._referance()
        elif isinstance(mat, dict) and isinstance(mat := load(mat), Material):
                mat_ref = mat._reference()
        else:
            mes = "Invalid 'mat'"
            raise CRIPTError(mes)

        # check if Material already added
        if mat_ref["uid"] in [i["uid"] for i in self._ingr]:
            mes = f"'{mat_ref['name']}' is already an ingredient."
            raise CRIPTError(mes)

        # Add material
        new_ingr = mat_ref

        # Add material properties
        new_ingr = new_ingr | self._get_mat_prop(mat, mat_id)

        # Add keywords
        if keyword in self.keys.keys():
            new_ingr["keyword"] = keyword
        else:
            mes = f"'{keyword}' is an invalid keyword. Valid keywords are: {list[self.keys.keys()]}"
            CRIPTError(mes)

        # Add mass, vol, mole
        if isinstance(qty, Quantity) and unit_check_bool(qty, Unit("kPa")) and eq_mat is None:
            new_ingr["pres"] = qty
            self._ingr.append(new_ingr)
            return

        elif isinstance(qty, Quantity) and eq_mat is None:
            key = unit_to_qty_key(qty)
            new_ingr[key] = qty
            new_ingr = ingr_calc_mass_vol_mole(new_ingr)
            self._ingr.append(new_ingr)
            self._ingr = ingr_equiv_molarity_mass_frac(self._ingr)
            return

        elif isinstance(qty, (float, int)) and eq_mat is None:
            if isinstance(eq_mat, int):
                qty = self._ingr[eq_mat]["moles"] * qty
            elif isinstance(eq_mat, str):
                pass
                qty = self._ingr[eq_mat]["moles"] * qty
            elif isinstance(eq_mat, Material):
                pass
            else:
                pass

            self._ingr.append(new_ingr)
            return

        else:
            mes = "Invaid"
            CRIPTError(mes)

    @staticmethod
    def _get_mat_prop(mat, mat_id=None) -> dict:
        mat_prop = Ingr._get_prop_from_mat_id(mat, ["phase", "molar_mass", "m_n", "conc", "density"])
        if mat_id is not None:
            if isinstance(mat_id, str):
                mat_id = mat._get_mat_id(mat_id)
            elif isinstance(mat_id, int) and mat_id in mat.iden.keys():
                pass  # Good mat_id provided
            else:
                mes = "Invalid mat_id."
                raise CRIPTError(mes)
            # this can add or overwrite bulk props
            mat_prop_2 = Ingr._get_prop_from_mat_id(mat, ["molar_mass", "m_n", "conc", "density"], mat_id)
            if mat_prop_2 == {}:
                mes = f"'mat_id' for {mat.name} found no properties to assist with ingredient calculations."
                CRIPTWarning(mes)
            else:
                mat_prop = mat_prop | mat_prop_2

        return mat_prop

    @staticmethod
    def _get_prop_from_mat_id(mat: Material, prop: list[str], mat_id: int = 0) -> dict:
        out = {}
        mat_props = [[p.key, p.value] for p in mat.prop if p.mat_id == mat_id]
        for p in mat_props:
            if p[0] in prop:
                out[p[0]] = p[1]
        return out

    def table(self) -> str:
        headers_list = list(Qty_keys.keys())
        row_format = "{:<30}" * len(headers_list)
        text_out = row_format.format(*headers_list)
        for k, v in self.qty:
            text_out += "\n"

        return text_out


class Process(BaseModel):
    keys = Process_keys
    _class = "Process"

    def __init__(
            self,
            name: str,
            ingr: list[Ingr],
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
