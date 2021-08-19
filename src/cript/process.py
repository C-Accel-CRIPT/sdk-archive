"""
Process Node

"""
from typing import Union

from pint.errors import DimensionalityError

from . import BaseModel, Cond, Prop, Unit, Quantity, CRIPTError, Material
from .utils.serializable import Serializable, SerializableSub
from .utils.printing import KeyPrinting
from .keys.process import *


class Qty(SerializableSub, KeyPrinting):
    keys = Qty_keys

    def __init__(
            self,
            value: Union[Quantity, int, float],
            uncer: Union[Quantity, int, float] = None,
            equiv: str = None,
            mat_uid: int = None,
            _key: str = None
    ):
        """

        :param value:
        :param uncer:
        """

        self._equiv = None
        self.equiv = equiv

        self._mat_uid = None
        self.mat_uid = mat_uid

        self._value = None
        self.value = value

        self._uncer = None
        self.uncer = uncer

        self._key = None
        if _key:
            if isinstance(_key, str) and _key in self.keys.keys():
                self.key = _key
        else:
            self.key = self._get_key()

    def __repr__(self):
        return self._create_str()

    def __str__(self):
        return self._create_str()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, (int, float)):
            if self.equiv is None:
                mes = "You must add units or use 'equiv'."
                raise CRIPTError(mes)
        self._value = value

    @property
    def uncer(self):
        return self._uncer

    @uncer.setter
    def uncer(self, uncer):
        self._uncer = uncer

    @property
    def equiv(self):
        return self._equiv

    @equiv.setter
    def equiv(self, equiv):
        self._equiv = equiv

    @property
    def mat_uid(self):
        return self._mat_uid

    @mat_uid.setter
    def mat_uid(self, mat_uid):
        self._mat_uid = mat_uid

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    def _loading(self, value, uncer):
        return value, uncer

    def _get_key(self) -> str:
        """
        It will use the units on self.value to determine the key for self.keys.
        """
        if isinstance(self.value, Quantity):
            for k, v in self.keys.items():
                try:
                    if u := v["unit"]:
                        self.value.to(u)
                    return k
                except DimensionalityError:
                    pass

    def _create_str(self) -> str:
        """
        Creates a nice string print out.
        """
        text_out = ""
        if isinstance(self.value, Quantity):
            text_out += f"{self.value.magnitude}"
            if self.uncer is not None:
                text_out += f" +-{self.uncer.to(self.value.units).magnitude}"
            text_out += f" {self.value.units}"

        elif isinstance(self.value, (float, int)):
            text_out += f"{self.value}"
            if self.uncer is not None:
                text_out += f" +-{self.uncer}"
            if self.equiv is not None:
                text_out += f" '{self.equiv}'"

        if self.mat_uid is not None:
            text_out += f" (mat: {self.mat_uid})"

        return text_out


class Ingr(Serializable, KeyPrinting):
    keys = Ingr_keys

    def __init__(
            self,
            c_material: Material,
            qty: Qty,
            type_: str,
            _key: str = None
    ):
        """

        :param c_material:
        :param type_:
        :param qty:
        """

        # if _key:
        #     value, uncer = self._loading(value, uncer)

        self._c_material = None
        self.c_material = c_material

        self._type_ = None
        self.type_ = type_

        self._qty = {k: None for k in Qty_keys}
        self.qty = qty

    def __repr__(self):
        return ""

    def __str__(self):
        return self.table()

    @property
    def c_material(self):
        """User specific name of the node."""
        return self._c_material

    @c_material.setter
    def c_material(self, c_material):
        self._c_material = c_material

    @property
    def type_(self):
        """User specific name of the node."""
        return self._type_

    @type_.setter
    def type_(self, type_):
        self._type_ = type_

    @property
    def qty(self):
        """User specific name of the node."""
        return self._qty

    @qty.setter
    def qty(self, qty):
        self._qty = qty

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
