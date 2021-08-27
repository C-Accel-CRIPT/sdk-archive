from typing import Union

from . import Quantity, Unit, Cond
from .utils.validator.type_check import type_check_property, type_check
from .utils.validator.prop import prop_keys_check
from .utils.serializable import SerializableSub
from .utils.printing import KeyPrinting


class Prop(SerializableSub, KeyPrinting):
    keys_molecule = None
    keys_polymer = None
    keys_rxn = None
    keys = None

    def __init__(
            self,
            key: str,
            value: Union[float, int, str, Quantity],
            uncer: Union[float, int, Quantity] = None,
            method: str = None,
            mat_id: int = 0,
            component: str = None,
            data_uid: str = None,
            cond: Union[list[Cond], Cond] = None,
            _loading: bool = False
    ):
        """

        :param mat_id: mat_id=0 is for bulk (default)
        :param key:
        :param value:
        :param uncer:
        :param component:
        :param method:
        :param data_uid:
        :param cond:
        """
        if _loading:
            key, value, uncer = self._loading(key, value, uncer)

        self._mat_id = None
        self.mat_id = mat_id

        self._key = None
        self.key = key

        self._value = None
        self.value = value

        self._uncer = None
        self.uncer = uncer

        self._component = None
        self.component = component

        self._method = None
        self.method = method

        self._data_uid = None
        self.data_uid = data_uid

        self._cond = None
        self.cond = cond

    @property
    def mat_id(self):
        return self._mat_id

    @mat_id.setter
    @type_check_property
    def mat_id(self, mat_id):
        self._mat_id = mat_id

    @property
    def key(self):
        return self._key

    @key.setter
    @type_check_property
    def key(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    @type_check_property
    def value(self, value):
        self._value = value

    @property
    def uncer(self):
        return self._uncer

    @uncer.setter
    @type_check_property
    def uncer(self, uncer):
        self._uncer = uncer

    @property
    def component(self):
        return self._component

    @component.setter
    @type_check_property
    def component(self, component):
        self._component = component

    @property
    def method(self):
        return self._method

    @method.setter
    @type_check_property
    def method(self, method):
        self._method = method

    @property
    def data_uid(self):
        return self._data_uid

    @data_uid.setter
    @type_check_property
    def data_uid(self, data_uid):
        self._data_uid = data_uid

    @property
    def cond(self):
        return self._cond

    @cond.setter
    @type_check((list[Cond], Cond, None))
    def cond(self, cond):
        if isinstance(cond, list):
            for i, s in enumerate(cond):
                if isinstance(s, dict):
                    cond[i] = Cond(**s, _loading=True)
        elif isinstance(cond, Cond):
            cond = [cond]
        self._cond = cond

    @classmethod
    def _init_(cls):
        from .keys.prop import prop_keys_mat, prop_keys_poly, prop_keys_rxn
        cls.keys_molecule = prop_keys_mat
        cls.keys_polymer = prop_keys_poly
        cls.keys_rxn = prop_keys_rxn
        cls.keys = cls.keys_molecule | cls.keys_polymer | cls.keys_rxn

    @classmethod
    def key_table(cls):
        print("\nMolecular Properties")
        print("-" * 20)
        text = cls.to_table(cls.keys_molecule)
        print(text)

        print("\nPolymer Properties")
        print("-" * 18)
        text = cls.to_table(cls.keys_polymer)
        print(text)

        print("\nReaction Properties")
        print("-" * 19)
        text = cls.to_table(cls.keys_rxn)
        print(text)

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