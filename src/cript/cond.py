"""
Condition Keywords

"""

from typing import Union

from . import Quantity, CRIPTError
from .base import CriptTypes, BaseSlot
from .doc_tools import load
from .utils.validator.type_check import type_check_property, type_check
from .utils.validator.cond import cond_keys_check
from .utils.serializable import SerializableSub
from .utils.printing import TablePrinting
from .utils.class_tools import freeze_class


class CondError(CRIPTError):
    pass


@freeze_class
class Cond(SerializableSub, TablePrinting, CriptTypes):
    keys = None
    _error = CondError

    def __init__(
            self,
            key: str,
            value,
            uncer: Union[float, int, Quantity] = None,
            c_data=None,
            _loading: bool = False
    ):
        """

        :param key: Unique key to define what the condition is. See Cond.key_table() for official list.
        :param value: numerical, text or material
        :param uncer: uncertainty
        :param data_uid: Referance to data node.
        """
        if _loading:
            key, value, uncer = self._loading(key, value, uncer)

        self._key = None
        self.key = key

        self._value = None
        self.value = value

        self._uncer = None
        self.uncer = uncer

        self._c_data = BaseSlot("Data", c_data, self._error)

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
    def c_data(self):
        return self._c_data

    @c_data.setter
    def c_data(self, *args):
        self._base_reference_block()

    @classmethod
    def _init_(cls):
        CriptTypes._init_()
        from .keys.cond import cond_keys
        cls.keys = cond_keys
