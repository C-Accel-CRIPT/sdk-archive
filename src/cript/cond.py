"""
Condition Keywords

"""

from typing import Union

from . import Quantity
from .utils.validator.type_check import type_check_property, type_check
from .utils.validator.cond import cond_keys_check
from .utils.serializable import Serializable


class Cond(Serializable):
    keys = None

    def __init__(
            self,
            key: str = None,
            value: Union[float, str, int, Quantity] = None,
            uncer: Union[float, int, Quantity] = None,
            data_uid=None,
    ):
        """

        :param key:
        :param value:
        :param uncer:
        :param data_uid:
        """

        self._key = None
        self.key = key

        self._value = None
        self.value = value

        self._uncer = None
        self.uncer = uncer

        self._data_uid = None
        self.data_uid = data_uid

    @property
    def key(self):
        return self._key

    @key.setter
    @type_check_property
    @cond_keys_check
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
    def data_uid(self):
        return self._data_uid

    @data_uid.setter
    @type_check_property
    def data_uid(self, data_uid):
        self._data_uid = data_uid

    @classmethod
    def _init_(cls):
        from .keys.cond import cond_keys
        cls.keys = cond_keys

    @classmethod
    def key_table(cls):
        text = cls.to_table(cls.keys)
        print(text)
