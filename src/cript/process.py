"""
Process Node

"""

from . import BaseModel, Cond, Prop, Unit
from .utils.serializable import Serializable
from .utils.type_check import type_check_property, type_check, id_type_check
from .keys.process import *

class Qty(Serializable):
    def __init__(
            self,
            value: Union[float, int],
            unit: Union[Unit, str],
            uncer: Union[float, str] = None,
            mat_id=None
    ):
        """

        :param value:
        :param unit:
        :param uncer:
        """
        self._value = None
        self.value = value

        self._unit = None
        self.unit = unit

        self._uncer = None
        self.uncer = uncer

        self._mat_id = None
        self.mat_id = mat_id

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def uncer(self):
        return self._uncer

    @uncer.setter
    def uncer(self, uncer):
        self._uncer = uncer

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, unit):
        self._unit = unit

    @property
    def mat_id(self):
        """User specific name of the node."""
        return self._mat_id

    @mat_id.setter
    def mat_id(self, mat_id):
        self._mat_id = mat_id


class Ingr(Serializable):
    keywords = keywords_Ingredients

    def __init__(
            self,
            mat_id,
            type_: str,
            qty: Union[list[Qty], Qty]
    ):
        """

        :param mat_id:
        :param type_:
        :param qty:
        """

        self._mat_id = None
        self.mat_id = mat_id

        self._type_ = None
        self.type_ = type_

        self._qty = None
        self.qty = qty

    @property
    def mat_id(self):
        """User specific name of the node."""
        return self._mat_id

    @mat_id.setter
    def mat_id(self, mat_id):
        self._mat_id = mat_id

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


class Process(BaseModel):
    op_keywords = keywords_Process
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
