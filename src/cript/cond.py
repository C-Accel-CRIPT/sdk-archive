"""
Condition Keywords

"""

from typing import Union

from . import Quantity, CRIPTError
from .base import CriptTypes
from .doc_tools import load
from .utils.validator.type_check import type_check_property, type_check
from .utils.validator.cond import cond_keys_check
from .utils.serializable import SerializableSub
from .utils.printing import TablePrinting


class CondError(CRIPTError):
    def __init__(self, *msg):
        super().__init__(*msg)


class Cond(SerializableSub, TablePrinting, CriptTypes):
    keys = None
    _error = CondError

    def __init__(
            self,
            key: str,
            value=None,
            uncer: Union[float, int, Quantity] = None,
            data_uid: str = None,
            _loading: bool = False
    ):
        """

        :param key:
        :param value:
        :param uncer:
        :param data_uid:
        """
        if _loading:
            key, value, uncer = self._loading(key, value, uncer)

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
    @cond_keys_check
    @type_check_property
    def key(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    @cond_keys_check
    def value(self, value):
        if isinstance(value, self.cript_types["Material"]):
            value = value.reference()
        elif isinstance(value, dict) and "_id" in value.keys():
            value = load(value)
            value = value.reference()

        self._value = value

    @property
    def uncer(self):
        return self._uncer

    @uncer.setter
    @cond_keys_check
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
        CriptTypes._init_()
        from .keys.cond import cond_keys
        cls.keys = cond_keys
