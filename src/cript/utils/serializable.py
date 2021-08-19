from abc import ABC
from datetime import datetime
from json import dumps

from .. import Quantity

label_length = {
    "keys": 16,
    "method": 25,
    "cond": 22,
    "required": 20,
    "type": 22,
    "range": 25,
    "unit": 12,
    "descr": 50,
    "names": 30
}

window = 150


class Serializable(ABC):
    """Base abstract class for a serializable object."""

    def __repr__(self):
        return dumps(self.dict_cleanup(self.as_dict(save=False)), indent=2, sort_keys=True)

    def __str__(self):
        return dumps(self.dict_remove_none(self.dict_cleanup(self.as_dict(save=False))), indent=2, sort_keys=True)

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
        elif type(obj) is datetime:
            return str(obj)
        elif type(obj) is Quantity:
            return str(obj)
        else:
            return obj

    @staticmethod
    def to_table(ddict: dict) -> str:
        levels = 0
        if isinstance(ddict, dict):
            levels = 1
            if isinstance(list(ddict.values())[0], dict):
                levels = 2

        if levels == 0:
            raise TypeError(f"Needs to be a dictionary.")

        elif levels == 1:
            row_format = "{:<30}" + "{:<" + str(window - 30) + "}"
            text_out = row_format.format("key", "description")
            text_out = text_out + "\n" + "-" * window
            for k, v in ddict.items():
                text_out = text_out + "\n" + row_format.format(k, v, )
            text_out = text_out + "\n"

            return text_out

        elif levels == 2:
            headers = list(list(ddict.values())[0].keys())
            headers.insert(0, "keys")
            row_format = ""
            for i in headers:
                row_format = row_format + Serializable._label_length(i)
            text_out = row_format.format(*headers)
            text_out = text_out + "\n" + "-" * window
            for k, v in ddict.items():
                entries = [str(i) for i in list(v.values())]
                for i, (entry, header) in enumerate(zip(entries, headers[1:])):
                    entries[i] = Serializable._length_limit(header, entry)
                text_out = text_out + "\n" + row_format.format(k, *entries)
            text_out = text_out + "\n"

            return text_out

    @staticmethod
    def _label_length(label: str) -> str:
        if label in label_length.keys():
            return "{:<" + str(label_length[label]) + "}"
        else:
            return "{:<30}"

    @staticmethod
    def _length_limit(label: str, entry) -> str:
        if label in label_length.keys():
            length_limit = label_length[label]
            if len(entry) > length_limit:
                return entry[0:length_limit-5] + "..."

        return entry
