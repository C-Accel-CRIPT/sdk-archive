from abc import ABC
from datetime import datetime
from bson import ObjectId
from json import dumps
from typing import Union

from .. import Quantity, Unit


class Serializable(ABC):
    """Base abstract class for a serializable object."""

    def __repr__(self):
        return dumps(self.dict_cleanup(self.as_dict(save=False)), indent=2, sort_keys=False)

    def __str__(self):
        return dumps(self.dict_remove_none(self.dict_cleanup(self.as_dict(save=False))), indent=2, sort_keys=False)

    def create_doc(self):
        """
        Converts a CRIPT node into document for upload to mongoDB
        """
        # add time stamps
        self._set_time_stamps()

        # convert to dictionary
        doc = self.as_dict(save=True)

        # remove empty id
        doc["_id"] = doc.pop("uid")

        # remove any unused attributes
        doc = self.dict_remove_none(doc)
        return doc

    def _set_time_stamps(self):
        """
        Adds time stamps to CRIPT node.
        """
        now = datetime.utcnow()
        if self.created_date is None:
            self.created_date = now

        self.last_modified_date = now

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
        """Remove 'key, value' pair form dictionary if value is None or []."""
        _dict = {}
        for k, v in ddict.items():
            if v is None or v == []:
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
    """ Used with Prop and Cond. """

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
                    new_uncer = uncer.split(" ", 1)
                    try:
                        uncer = float(new_uncer[0]) * Unit(new_uncer[1])
                    except Exception:
                        pass

        else:
            if key in self.keys.keys():
                unit_ = self.keys[key]["unit"]
                if unit_:
                    if value is not None:
                        value = value * Unit(unit_)
                        if uncer is not None:
                            uncer = uncer * Unit(unit_)

        return key, value, uncer
