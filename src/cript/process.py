"""
Process Node

"""
from typing import Union

from pint.unit import Unit

from .base import BaseModel, Cond, Prop
from .keywords.process import *
from .utils.serializable import Serializable


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


class Ingredient(Serializable):
    keywords = keywords_Ingredients

    def __init__(
            self,
            mat_id,
            type_: str,
            qty: list[Qty]
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
            ingredients: list[Ingredient],
            procedure: str,
            conditions: list[Cond],
            properties: list[Prop] = None,
            keywords: list[str] = None,
            notes: str = None,
            **kwargs
    ):
        """

        :param name: The name of the user.
        :param ingredients:
        :param procedure:
        :param conditions:
        :param properties:
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

        self._ingredients = None
        self.ingredients = ingredients

        self._procedure = None
        self.procedure = procedure

        self._properties = None
        self.properties = properties

        self._keywords = None
        self.keywords = keywords

        self._conditions = None
        self.conditions = conditions

    @property
    def ingredients(self):
        return self._ingredients

    @ingredients.setter
    def ingredients(self, ingredients):
        self._ingredients = ingredients

    @property
    def procedure(self):
        return self._procedure

    @procedure.setter
    def procedure(self, procedure):
        self._procedure = procedure

    @property
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, properties):
        self._properties = properties

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        self._keywords = keywords

    @property
    def conditions(self):
        return self._conditions

    @conditions.setter
    def conditions(self, conditions):
        self._conditions = conditions
