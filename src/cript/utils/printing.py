from abc import ABC, abstractmethod

QUANTITY_LENGTH = 10

# limits of printout length
label_length = {
    "keys": {
        "length": 16,
        "short": "k"
    },
    "method": {
        "length": 25,
        "short": "method"
    },
    "cond": {
        "length": 22,
        "short": "condition"
    },
    "required": {
        "length": 20,
        "short": "requ."
    },
    "type": {
        "length": 22,
        "short": "type"
    },
    "range": {
        "length": 25,
        "short": "range"
    },
    "unit": {
        "length": 12,
        "short": "unit"
    },
    "description":{
        "length": 50,
        "short": "descr"
    },
    "names": {
        "length": 30,
        "short": "names"
    },
    "mass": {
        "length": QUANTITY_LENGTH,
        "short": "mass"
    },
    "volume": {
        "length": QUANTITY_LENGTH,
        "short": "vol"
    },
    "pressure": {
        "length": QUANTITY_LENGTH,
        "short": "pres"
    },
    "mole": {
        "length": QUANTITY_LENGTH,
        "short": "mol"
    },
    "equiv": {
        "length": QUANTITY_LENGTH,
        "short": "pres"
    },
    "molarity": {
        "length": QUANTITY_LENGTH,
        "short": "M"
    },
    "mass_fraction": {
        "length": QUANTITY_LENGTH,
        "short": "mass_frac"
    }
}

window = 150


class TablePrinting(ABC):
    """
    Prints key tables out.
    """
    keys = None

    @classmethod
    def key_table(cls):
        text = cls.to_table(cls.keys)
        print(text)

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
                row_format = row_format + TablePrinting._label_length(i)
            text_out = row_format.format(*headers)
            text_out = text_out + "\n" + "-" * window
            for k, v in ddict.items():
                entries = [str(i) for i in list(v.values())]
                for i, (entry, header) in enumerate(zip(entries, headers[1:])):
                    entries[i] = TablePrinting._length_limit(header, entry)
                text_out = text_out + "\n" + row_format.format(k, *entries)
            text_out = text_out + "\n"

            return text_out

    @staticmethod
    def _label_length(label: str) -> str:
        if label in label_length.keys():
            return "{:<" + str(label_length[label]["length"]) + "}"
        else:
            return "{:<30}"

    @staticmethod
    def _length_limit(label: str, entry) -> str:
        if label in label_length.keys():
            length_limit = label_length[label]["length"]
            if len(entry) > length_limit:
                return entry[0:length_limit-5] + "..."

        return entry
