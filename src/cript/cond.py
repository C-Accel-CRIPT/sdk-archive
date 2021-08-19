"""
Condition Keywords

"""

from typing import Union

from . import Quantity, Unit
from .utils.validator.type_check import type_check_property, type_check
from .utils.validator.cond import cond_keys_check
from .utils.serializable import Serializable


class Cond(Serializable):
    keys = None
    cript_types = None

    def __init__(
            self,
            key: str,
            value=None,
            uncer: Union[float, int, Quantity] = None,
            data_uid=None,
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
    @type_check_property
    def value(self, value):
        if isinstance(value, self.cript_types["Material"]):
            value = value._reference()
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
        from .keys.cond import cond_keys
        from . import cript_types
        cls.keys = cond_keys
        cls.cript_types = cript_types

    @classmethod
    def key_table(cls):
        text = cls.to_table(cls.keys)
        print(text)

    def as_dict(self, **kwargs) -> dict:
        """Convert and return object as dictionary."""
        keys = {k.lstrip("_") for k in vars(self) if "__" not in k}

        attr = dict()
        for k in keys:
            value = self.__getattribute__(k)
            if isinstance(value, Quantity):
                value = self._to_dict_units(value, **kwargs)
            attr[k] = value

        return attr

    def _to_dict_units(self, value, save: bool = True) -> Union[str, int, float]:
        if save:
            if "+" in self.key[0]:
                return str(value)
            else:
                unit_ = self.keys[self.key]["unit"]
                return value.to(unit_).magnitude
        else:
            return str(value)

    def _loading(self, key, value, uncer):
        """ Loading from database; will add units back to numbers"""
        if "+" in key:
            if value is not None:
                new_value = value.split(" ", 1)
                try:
                    value = float(new_value[0]) * Unit(new_value[1])
                except Exception:
                    pass
                if uncer is not None:
                    new_value = value.split(" ", 1)
                    try:
                        value = float(new_value[0]) * Unit(new_value[1])
                    except Exception:
                        pass

        else:
            if key in self.keys.keys():
                unit_ = self.keys[key]["unit"]
                if unit_:
                    if value is not None:
                        value = value * Unit(unit_)
                        if uncer is not None:
                            value = value * Unit(unit_)

        return key, value, uncer
