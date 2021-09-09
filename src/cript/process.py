"""
Process Node

"""
from typing import Union
from warnings import warn

from . import Unit, Quantity, CRIPTError
from .base import BaseModel
from .cond import Cond
from .prop import Prop
from .doc_tools import load, loading_with_units
from .material import Material
from .utils.printing import TablePrinting
from .utils.ingr_calc import IngredientCalculator
from .utils.external_database_code import GetObject
from .keys.process import Process_keys, Ingr_keys


class ProcessError(CRIPTError):
    def __init__(self, *msg):
        super().__init__(*msg)


class IngrError(CRIPTError):
    def __init__(self, *msg):
        super().__init__(*msg)


class Ingr(IngredientCalculator, TablePrinting):
    keys = Ingr_keys
    _error = IngrError

    def __init__(self, *args):
        """
        Functions: add, remove, scale, scale_one
        __init__ calls add

        :param see add function
        """
        super().__init__()

        if all([isinstance(i, dict) for i in args[0]]):  # loading from doc
            self._loading(args[0])
            return

        self._init_with_args(*args)

    @property
    def ingr(self):
        return self.as_dict()

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
        new_ingr = self._get_material_data(mat, mat_id)
        new_ingr.update(self._get_keyword(keyword))
        if eq_mat:
            equivalence = [qty, eq_mat]
        else:
            new_ingr[self._q_calc._qty_to_key(qty)] = qty
            equivalence = None
        super().add(new_ingr, equivalence)

    def _get_material_data(self, mat: Union[dict, Material], mat_id) -> dict:
        """
        Gets data for material.
        """
        mat = self._pre_checks_for_material(mat)
        mat_data = mat.reference()
        prop_data = self._get_mat_prop(mat, mat_id)
        return mat_data | prop_data

    def _pre_checks_for_material(self, mat):
        """
        Check if Material is valid input type and loads material if needed.
        """
        if isinstance(mat, Material):
            pass
        elif isinstance(mat, dict) and "_id" in mat.keys() and isinstance(node := load(mat), Material):
            mat = node
        elif isinstance(mat, str):
            mat = load(GetObject.get_from_uid("Material", mat)[0])
        else:
            mes = f"Invalid object for 'material'. {mat}"
            raise self._error(mes)

        self._material_in_list_check(mat)
        return mat

    def _material_in_list_check(self, mat: Material) -> bool:
        """
        Check if Material already added to self._ingr.
        """
        if mat.uid in [i["uid"] for i in self._ingr]:
            mes = f"'{mat.name}' is already an ingredient."
            raise self._error(mes)

        return True

    def _get_mat_prop(self, mat, mat_id=None) -> dict:
        mat_prop = self._get_prop_from_mat_id(mat, ["phase", "molar_mass", "m_n", "molar_conc", "density"])
        if mat_id is not None:
            if isinstance(mat_id, str):
                if mat_id.isdigit():
                    pass
                else:
                    mat_id = mat._get_mat_id(mat_id)
            elif isinstance(mat_id, int) and mat_id in mat.iden.keys():
                mat_id = str(mat_id)  # Good mat_id provided
            else:
                mes = "Invalid mat_id."
                raise self._error(mes)
            # this can add or overwrite bulk props
            mat_prop_2 = self._get_prop_from_mat_id(mat, ["molar_mass", "m_n", "molar_conc", "density"], mat_id)
            if mat_prop_2 == {}:
                mes = f"'mat_id' for {mat.name} found no properties to assist with ingredient calculations."
                warn(mes)
            else:
                mat_prop = mat_prop | mat_prop_2 | {"mat_id": mat_id}

        return mat_prop

    @staticmethod
    def _get_prop_from_mat_id(mat: Material, prop: list[str], mat_id: str = "0") -> dict:
        out = {}
        mat_props = [[p.key, p.value] for p in mat.prop if p.mat_id == mat_id]
        for p in mat_props:
            if p[0] in prop:
                out[p[0]] = p[1]
        return out

    def _get_keyword(self, keyword: str) -> dict:
        """
        Returns keyword if valid.
        """
        if keyword in self.keys.keys():
            return {"keyword": keyword}
        elif keyword is None:
            return {}
        else:
            mes = f"'{keyword}' is an invalid keyword. Valid keywords are: {list[self.keys.keys()]}"
            raise self._error(mes)

    def as_dict(self, save=True) -> list[dict]:
        """
        Only saves absolute quantities (mass, vol, mole, pres) and NOT relative quantities.
        """
        out = []
        keys = ["uid", "name", "class_", "keyword", "mat_id"] + list(self._q_calc.keys_qty.keys())
        for ingr in self._ingr:
            ingr_dict = {}
            for k in keys:
                if k in ingr.keys():
                    value = ingr[k]
                    if isinstance(value, Quantity):
                        if save:
                            value = value.to(self._q_calc.keys_qty[k]["unit"]).magnitude
                        else:
                            value = str(value.to(self._q_calc.keys_qty[k]["unit"]))
                    ingr_dict[k] = value

            out.append(ingr_dict)

        return out

    def _loading(self, ingrs: list[dict]):
        """Loading a data back into Ingr from Mongodb document"""
        for ingr in ingrs:
            keyword = None
            mat_id = None
            qty = None
            for k, v in ingr.items():
                if k in self._q_calc.keys_qty:
                    qty = v * Unit(self._q_calc.keys_qty[k]["unit"])
                if k == "keyword":
                    keyword = ingr[k]
                if k == "mat_id":
                    mat_id = ingr[k]

            if qty is None:
                mes = f"Error loading ingr. {ingr['name']}"
                raise self._error(mes)

            self.add(ingr["uid"], qty, keyword=keyword, mat_id=mat_id)


class Process(TablePrinting, BaseModel, _error=ProcessError):
    class_ = "Process"
    keys = Process_keys

    def __init__(
            self,
            name: str,
            ingr,
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
        super().__init__(name=name, class_=self.class_, notes=notes, **kwargs)

        self._procedure = None
        self.procedure = procedure

        self._prop = None
        self.prop = prop

        self._keywords = None
        self.keywords = keywords

        self._cond = None
        self.cond = cond

        if isinstance(ingr, Ingr):
            self.ingr = ingr
        else:
            self.ingr = Ingr(ingr)

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
        prop = loading_with_units(prop, Prop)
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
        cond = loading_with_units(cond, Cond)
        self._cond = cond
