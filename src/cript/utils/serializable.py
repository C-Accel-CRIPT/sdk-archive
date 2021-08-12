from abc import ABC
from datetime import datetime

from .. import cript_types, Unit


def load(ddict: dict):
    ddict["uid"] = str(ddict.pop("_id"))
    class_ = ddict.pop("class_")
    obj = cript_types[class_](**ddict)
    return obj


class Serializable(ABC):
    """Base abstract class for a serializable object."""

    def as_dict(self):
        """Convert and return object as dictionary."""
        keys = {k.lstrip("_") for k in vars(self) if "__" not in k}

        attr = dict()
        for k in keys:
            value = Serializable._to_dict(self.__getattribute__(k))
            if isinstance(value, Unit):
                value = str(value)
            attr[k] = value

        return attr

    @staticmethod
    def _to_dict(obj):
        """Convert obj to a dictionary, and return it."""
        if isinstance(obj, list):
            return [Serializable._to_dict(i) for i in obj]
        elif hasattr(obj, "as_dict"):
            return obj.as_dict()
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
    def dict_datetime_to_str(ddict: dict) -> dict:
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
            return Serializable.dict_datetime_to_str(obj)
        elif type(obj) is datetime:
            return str(obj)
        else:
            return obj
