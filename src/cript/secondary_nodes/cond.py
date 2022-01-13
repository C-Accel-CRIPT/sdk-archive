"""
Condition Object

"""

from typing import Union

from .. import Quantity, CRIPTError
from ..primary_nodes.base import CriptTypes, ReferenceList
from .load import load
from ..utils import SerializableSub, TablePrinting, freeze_class
from ..validator import type_check, cond_keys_check


class CondError(CRIPTError):
    pass


@freeze_class
class Cond(SerializableSub, TablePrinting, CriptTypes):
    """ Condition

    Conditions are environmental variables.

    Attributes
    ----------
    key: str
        Yields
        See Cond.key_table() for official list.
    value: Any
        piece of information or quantity
    uncer: Any
        uncertainty in quantity
    c_data: list[Data]
        CRIPT Data associate with the property

    """

    keys = None
    _error = CondError

    def __init__(
            self,
            key: str,
            value,
            uncer: Union[float, int, Quantity] = None,
            c_data=None,
            _loading: bool = False  # need for loading a file from the data base
    ):

        if _loading:
            key, value, uncer = self._loading(key, value, uncer)

        self._key = None
        self.key = key

        self._value = None
        self.value = value

        self._uncer = None
        self.uncer = uncer

        self._c_data = ReferenceList("Data", c_data, self._error)

    @property
    def key(self):
        return self._key

    @key.setter
    @cond_keys_check
    @type_check(str)
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
    @type_check([int, float, Quantity])
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
        from ..keys.cond import cond_keys
        cls.keys = cond_keys
