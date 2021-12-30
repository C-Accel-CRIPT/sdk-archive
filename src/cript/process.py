"""
Process Node

"""
from typing import Union
from warnings import warn

from . import Unit, Quantity, CRIPTError
from .base import BaseModel
from .load_export import load, loading_with_units
from .cond import Cond
from .prop import Prop
from .material import Material
from .utils import TablePrinting, IngredientCalculator, GetObject, freeze_class
from .keys.process import process_keywords, ingredient_keywords


class ProcessError(CRIPTError):
    pass


class IngrError(CRIPTError):
    pass


@freeze_class
class Ingr(IngredientCalculator, TablePrinting):
    """
    Adds mat to Ingr and performs calculations for the other quantities.
    :param mat:
    :param qty:
    :param keyword:
    :param eq_mat:
    :param mat_id:
    :param method: used to select proper from specific method; example "nmr" vs "sec"
    :return:
    """
    keys = ingredient_keywords
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
            eq_mat=None, mat_id=None, method: str = None):

        new_ingr = self._get_material_data(mat, mat_id, method)
        new_ingr.update(self._get_keyword(keyword))
        if eq_mat:
            equivalence = [qty, eq_mat]
        else:
            new_ingr[self._q_calc._qty_to_key(qty)] = qty
            equivalence = None
        super().add(new_ingr, equivalence)

    def _get_material_data(self, mat: Union[dict, Material], mat_id, method) -> dict:
        """
        Gets data for material.
        """
        mat = self._pre_checks_for_material(mat)
        mat_data = mat.reference()
        prop_data = self._get_mat_prop(mat, mat_id, method)
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

    def _get_mat_prop(self, mat, mat_id, method) -> dict:
        mat_prop = self._get_prop_from_mat_id(mat, ["phase", "molar_mass", "m_n", "conc_molar", "density", "m_n"],
                                              method=method)
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
            mat_prop_2 = self._get_prop_from_mat_id(mat, ["molar_mass", "m_n", "conc_molar", "density", "m_n"],
                                                    mat_id, method)
            if mat_prop_2 == {}:
                mes = f"'mat_id' for {mat.name} found no properties to assist with ingredient calculations."
                warn(mes)
            else:
                mat_prop = mat_prop | mat_prop_2 | {"mat_id": mat_id}

        return mat_prop

    @staticmethod
    def _get_prop_from_mat_id(mat: Material, prop: list[str], mat_id: int = 0, method: str = None) -> dict:
        warn_mes = None
        out = {}
        mat_props = [[p.key, p.value, p.method] for p in mat.prop if p.mat_id == mat_id]
        for p in mat_props:
            if p[0] in prop:
                if p[0] in out.keys():
                    if method is not None:
                        if p[3] == method:
                            out[p[0]] = p[1]
                        else:
                            for pp in mat.prop:
                                if pp.mat_id == mat_id and pp.value == out[p[0]]:
                                    if pp.method == method:
                                        warn_mes = None
                                    else:
                                        warn_mes = f"'{p[0]}' determined from {method} does not exist for {mat.name}."
                    else:
                        warn_mes = f"'{p[0]}' has two or more values found for {mat.name}. {p[0]}={out[p[0]]} " \
                                   f"used for calculations. Add 'method' to get specify a specific '{p[0]}'."
                else:
                    out[p[0]] = p[1]

        if warn_mes is not None:
            warn(warn_mes)

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


@freeze_class
class Process(TablePrinting, BaseModel, _error=ProcessError):
    class_ = "Process"
    keys = process_keywords

    def __init__(
            self,
            name: str,
            ingr,
            procedure: str,
            cond: list[Cond] = None,
            prop: list[Prop] = None,
            keywords: list[str] = None,
            notes: str = None,
            **kwargs
    ):
        """

        :param name: The user-defined name for the process.
        :param ingr: See help(Ingr.__init__)
        :param procedure: Text write up of procedure
        :param cond: Condition. See help(Cond.__init__) and Cond.key_table()
        :param prop: Property. See help(Prop.__init__) and Prop.key_table()
        :param keywords: See Process.key_table()
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
