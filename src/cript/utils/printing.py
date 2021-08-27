from abc import ABC, abstractmethod

QUANTITY_LENGTH = 10

# limits of printout length
label_length = {
    "keys": 16,
    "method": 25,
    "cond": 22,
    "required": 20,
    "type": 22,
    "range": 25,
    "unit": 12,
    "descr": 50,
    "names": 30,
    "mass": QUANTITY_LENGTH,
    "vol": QUANTITY_LENGTH,
    "pres": QUANTITY_LENGTH,
    "mole": QUANTITY_LENGTH,
    "equiv": QUANTITY_LENGTH,
    "molarity": QUANTITY_LENGTH,
    "mass_frac": QUANTITY_LENGTH
}

window = 150


class KeyPrinting(ABC):
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
                row_format = row_format + KeyPrinting._label_length(i)
            text_out = row_format.format(*headers)
            text_out = text_out + "\n" + "-" * window
            for k, v in ddict.items():
                entries = [str(i) for i in list(v.values())]
                for i, (entry, header) in enumerate(zip(entries, headers[1:])):
                    entries[i] = KeyPrinting._length_limit(header, entry)
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
