from abc import ABC
from json import dumps
from typing import Union
from datetime import datetime

from pint.unit import Unit

from . import __version__
from .utils.serializable import Serializable
from .validation_tools import *


class BaseModel(Serializable, ABC):
    """Base (abstract) class to represent a data model.
    Parameters
    ----------
    name: str, required
        User specific name of the node.
    notes: str, optional
        A free form space to add non-property information.
    """

    def __init__(
        self,
        name: str,
        _class: str = None,
        notes: str = None,

        uid: str = None,
        model_version: str = None,
        version_control=None,
        last_modified_date: datetime = None,
        created_date: datetime = None
    ):
        """

        :param name: The name of the user.

        :param _class: class of node.
        :param notes: Any miscellaneous notes related to the user.

        :param uid: The unique ID of the material.
        :param model_version: Version of CRIPT data model.
        :param version_control: Link to version control node.
        :param last_modified_date: Last date the node was modified.
        :param created_date: Date it was created.
        """

        self._name = None
        self.name = name

        self._notes = None
        self.notes = notes

        self._class_ = _class

        self._uid = None
        if model_version is None:
            self._model_version = __version__
        else:
            self._model_version = model_version
        self._version_control = None
        self._last_modified_date = None
        self._created_date = None

    def __repr__(self):
        return dumps(self.as_dict(), indent=2, sort_keys=True)

    def __str__(self):
        return dumps(self.dict_remove_none(self.as_dict()), indent=2, sort_keys=True)

    @property
    def name(self):
        """User specific name of the node."""
        return self._name

    @name.setter
    @type_check_property
    def name(self, name):
        self._name = name

    @property
    def notes(self):
        """ A free form space to add non-property information."""
        return self._notes

    @notes.setter
    @type_check_property
    def notes(self, notes):
        self._notes = notes

    @property
    def uid(self):
        """Unique ID of the node."""
        return self._uid

    @uid.setter
    @type_check_property
    def uid(self, uid):
        self._uid = uid

    @property
    def class_(self):
        """Version of the data model."""
        return self._class_

    @property
    def model_version(self):
        """Version of the data model."""
        return self._model_version

    @property
    def version_control(self):
        """Version control reference of the data model."""
        return self._version_control

    @property
    def last_modified_date(self):
        """Date the node was last modified."""
        return self._last_modified_date

    @property
    def created_date(self):
        """Date the node was created."""
        return self._created_date


class Cond(Serializable):
    def __init__(
            self,
            key: str = None,
            value: Union[float, str, int] = None,
            unit: Unit = None,
            uncer: Union[float, str] = None,
            data_uid=None,
    ):
        """

        :param key: time, temp, pres, solvent, standard, relative, atmosphere
        :param unit:
        """

        self._key = None
        self.key = key

        self._value = None
        self.value = value

        self._unit = None
        self.unit = unit

        self._uncer = None
        self.uncer = uncer

        self._data_uid = None
        self.data_uid = data_uid

    @property
    def key(self):
        return self._key

    @key.setter
    @type_check_property
    def key(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    @type_check_property
    def value(self, value):
        self._value = value

    @property
    def unit(self):
        return self._unit

    @unit.setter
    @type_check_property
    def unit(self, unit):
        self._unit = unit

    @property
    def uncer(self):
        return self._uncer

    @uncer.setter
    @type_check_property
    def uncer(self, uncer):
        self._uncer = uncer

    @property
    def data_uid(self):
        return self._data_uid

    @data_uid.setter
    @type_check_property
    def data_uid(self, data_uid):
        self._data_uid = data_uid


class Prop(Serializable):
    def __init__(
            self,
            key: str,
            value: Union[float, int, str],
            unit: Unit = None,
            uncer: Union[float, int, str] = None,
            method: str = None,
            mat_id: int = None,
            component: str = None,
            data_uid: str = None,
            conditions: list[Cond] = None
    ):
        """

        :param mat_id:
        :param key:
        :param value:
        :param uncer:
        :param unit:
        :param component:
        :param method:
        :param data_uid:
        :param conditions:
        """

        self._mat_id = None
        self.mat_id = mat_id

        self._key = None
        self.key = key

        self._value = None
        self.value = value

        self._uncer = None
        self.uncer = uncer

        self._unit = None
        self.unit = unit

        self._component = None
        self.component = component

        self._method = None
        self.method = method

        self._data_uid = None
        self.data_uid = data_uid

        self._conditions = None
        self.conditions = conditions

    @property
    def mat_id(self):
        return self._mat_id

    @mat_id.setter
    @type_check_property
    def mat_id(self, mat_id):
        self._mat_id = mat_id

    @property
    def key(self):
        return self._key

    @key.setter
    @type_check_property
    def key(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    @type_check_property
    def value(self, value):
        self._value = value

    @property
    def uncer(self):
        return self._uncer

    @uncer.setter
    @type_check_property
    def uncer(self, uncer):
        self._uncer = uncer

    @property
    def unit(self):
        return self._unit

    @unit.setter
    @type_check_property
    def unit(self, unit):
        self._unit = unit

    @property
    def component(self):
        return self._component

    @component.setter
    @type_check_property
    def component(self, component):
        self._component = component

    @property
    def method(self):
        return self._method

    @method.setter
    @type_check_property
    def method(self, method):
        self._method = method

    @property
    def data_uid(self):
        return self._data_uid

    @data_uid.setter
    @type_check_property
    def data_uid(self, data_uid):
        self._data_uid = data_uid

    @property
    def conditions(self):
        return self._conditions

    @conditions.setter
    @type_check_property
    def conditions(self, conditions):
        self._conditions = conditions


class CRIPTError(Exception):

    def __init__(self, message):
        self.message = message
