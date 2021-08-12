"""
Condition and Property sub-nodes

"""

from typing import Union

from .utils.type_check import type_check_property, type_check
from .utils.serializable import Serializable
from . import Unit


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
            mat_uid: int = 0,
            component: str = None,
            data_uid: str = None,
            cond: Union[list[Cond], Cond] = None
    ):
        """

        :param mat_id: mat_id=0 is for bulk (default)
        :param key:
        :param value:
        :param uncer:
        :param unit:
        :param component:
        :param method:
        :param data_uid:
        :param cond:
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

        self._cond = None
        self.cond = cond

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
    def cond(self):
        return self._cond

    @cond.setter
    @type_check((list[Cond], Cond, None))
    def cond(self, cond):
        self._cond = cond
