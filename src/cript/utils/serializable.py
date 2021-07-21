import abc
from pint import Unit
from bson import ObjectId


class Serializable(abc.ABC):
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
        elif isinstance(obj, ObjectId):
            return str(obj)
        else:
            return obj

    @staticmethod
    def dict_remove_none(ddict: dict) -> dict:
        """Remove key, value pair form dictionary if value is None."""
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

    @classmethod
    def from_dict(cls, ddict: dict):
        """Construct an object from the input dictionary."""
        return cls(**ddict)
