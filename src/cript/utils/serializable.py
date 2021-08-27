from abc import ABC
from datetime import datetime
from bson import ObjectId
from json import dumps
from typing import Union

from .. import Quantity


class Serializable(ABC):
    """Base abstract class for a serializable object."""

    def __repr__(self):
        return dumps(self.dict_cleanup(self.as_dict(save=False)), indent=2, sort_keys=False)

    def __str__(self):
        return dumps(self.dict_remove_none(self.dict_cleanup(self.as_dict(save=False))), indent=2, sort_keys=False)

    def as_dict(self, **kwargs) -> dict:
        """Convert and return object as dictionary."""
        keys = {k.lstrip("_") for k in vars(self) if "__" not in k}

        attr = dict()
        for k in keys:
            value = self._to_dict(self.__getattribute__(k), **kwargs)
            attr[k] = value

        return attr

    @staticmethod
    def _to_dict(obj, **kwargs):
        """Convert obj to a dictionary, and return it."""
        if isinstance(obj, list):
            return [Serializable._to_dict(i, **kwargs) for i in obj]
        elif hasattr(obj, "as_dict"):
            return obj.as_dict(**kwargs)
        else:
            return obj

    @staticmethod
    def dict_remove_none(ddict: dict) -> dict:
        """Remove 'key, value' pair form dictionary if value is None."""
        _dict = {}
        for k, v in ddict.items():
            if v is None:
                continue
            elif isinstance(v, dict):
                _dict[k] = Serializable.dict_remove_none(v)
            elif isinstance(v, list):
                _list = []
                for obj in v:
                    if isinstance(obj, dict):
                        obj = Serializable.dict_remove_none(obj)
                    _list.append(obj)
                _dict[k] = _list
            else:
                _dict[k] = v

        return _dict

    @staticmethod
    def dict_cleanup(ddict: dict) -> dict:
        """Converts any datetime objects to strings"""
        attr = dict()
        for k, v in ddict.items():
            value = Serializable._loop_through(v)
            attr[k] = value

        return attr

    @staticmethod
    def _loop_through(obj):
        if isinstance(obj, list):
            return [Serializable._loop_through(i) for i in obj]
        elif isinstance(obj, dict):
            return Serializable.dict_cleanup(obj)
        elif isinstance(obj, datetime):
            return str(obj)
        elif isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, Quantity):
            return str(obj)
        else:
            return obj


class SerializableSub(Serializable, ABC):

    def as_dict(self, **kwargs) -> dict:
        """Convert and return object as dictionary."""
        keys = {k.lstrip("_") for k in vars(self) if "__" not in k}

        attr = dict()
        for k in keys:
            value = self.__getattribute__(k)
            if isinstance(value, Quantity):
                value = self._to_dict_units(value, **kwargs)
            else:
                value = self._to_dict(value, **kwargs)
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
