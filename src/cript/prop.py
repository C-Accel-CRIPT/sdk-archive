"""
Property Object

"""

from typing import Union

from . import CRIPTError
from .base import ReferenceList
from .load_export import loading_with_units
from .cond import Cond
from .utils import SerializableSub, TablePrinting, freeze_class
from .validator import type_check, prop_keys_check


class CondError(CRIPTError):
    pass


@freeze_class
class Prop(SerializableSub, TablePrinting):
    keys_material = None
    keys_rxn = None
    keys = None
    _error = CondError

    def __init__(
            self,
            key: str,
            value,
            uncer=None,
            method: str = None,
            mat_id: int = 0,
            component: str = None,
            c_data=None,
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
        :param c_data:
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

        self._cond = None
        self.cond = cond

        self._c_data = ReferenceList("Data", c_data, self._error)

    @property
    def mat_id(self):
        return self._mat_id

    @mat_id.setter
    def mat_id(self, mat_id):
        self._mat_id = mat_id

    @property
    def key(self):
        return self._key

    @key.setter
    @type_check(str)
    def key(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def uncer(self):
        return self._uncer

    @uncer.setter
    def uncer(self, uncer):
        self._uncer = uncer

    @property
    def component(self):
        return self._component

    @component.setter
    @type_check(str)
    def component(self, component):
        self._component = component

    @property
    def method(self):
        return self._method

    @method.setter
    @type_check(str)
    def method(self, method):
        self._method = method

    @property
    def cond(self):
        return self._cond

    @cond.setter
    @type_check([list[Cond], Cond])
    def cond(self, cond):
        cond = loading_with_units(cond, Cond)
        self._cond = cond

    @property
    def c_data(self):
        return self._c_data

    @c_data.setter
    def c_data(self, *args):
        self._base_reference_block()

    @classmethod
    def _init_(cls):
        from .keys.prop import property_material_keys, property_process_keys
        cls.keys_material = property_material_keys
        cls.keys_process = property_process_keys
        cls.keys = {**cls.keys_material, **cls.keys_process}

    @classmethod
    def key_table(cls, _type: str = "html"):
        if _type == "html":
            cls.open_html("property_keys_materials.html")
            cls.open_html("property_keys_reaction.html")

        elif _type == "console":
            print("\nMolecular Properties")
            print("-" * 20)
            text = cls.to_table(cls.keys_material)
            print(text)

            print("\nReaction Properties")
            print("-" * 19)
            text = cls.to_table(cls.keys_rxn)
            print(text)
