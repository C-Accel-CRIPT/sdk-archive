"""
Property Object

"""

from typing import Union

from .. import CRIPTError
from ..primary_nodes.base import ReferenceList
from .cond import Cond
from ..utils import SerializableSub, TablePrinting, freeze_class, loading_with_units
from ..validator import type_check, keys_check, value_check
from ..keys.methods import method_keys


class CondError(CRIPTError):
    pass


@freeze_class
class Prop(SerializableSub, TablePrinting):
    """ Properties

    Properties are qualities or traits that belonging to a node.

    Attributes
    ----------
    key: str (has keys)
        type of property
        See Prop.key_table() for official list.
    value: Any
        piece of information or quantity
    uncer: Any
        uncertainty in quantity
    method: str
        approach or source of property data
    mat_id: int
        identifier that is associate with the property
        0 = whole mixture
        1+ = individual component
    structure: str
        specific chemical structure associate with the property
    c_data: list[Data]
        CRIPT Data associate with the property
    cond: list[Cond]
        conditions that the property was taken under

    """
    keys_material = None
    keys_rxn = None
    keys = None
    _error = CondError

    def __init__(
            self,
            key: str,
            value,
            method: str,
            uncer=None,
            mat_id: int = 0,
            structure: str = None,
            c_data=None,
            cond: Union[list[Cond], Cond] = None,
            _loading: bool = False  # need for loading a file from the data base
    ):
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

        self._structure = None
        self.structure = structure

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
    @keys_check
    @type_check(str)
    def key(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    @value_check
    def value(self, value):
        self._value = value

    @property
    def uncer(self):
        return self._uncer

    @uncer.setter
    @value_check
    def uncer(self, uncer):
        self._uncer = uncer

    @property
    def structure(self):
        return self._structure

    @structure.setter
    @type_check(str)
    def structure(self, structure):
        self._structure = structure

    @property
    def method(self):
        return self._method

    @method.setter
    @keys_check(method_keys)
    @type_check(str)
    def method(self, method):
        self._method = method

    @property
    def cond(self):
        return self._cond

    @cond.setter
    @type_check([list[Cond], Cond])
    @loading_with_units(Cond)
    def cond(self, cond):
        self._cond = cond

    @property
    def c_data(self):
        return self._c_data

    @c_data.setter
    def c_data(self, *args):
        self._base_reference_block()

    @classmethod
    def _init_(cls):
        """ Load key table after objects have been initiated. Called at the end of __init__.py """
        from ..keys.prop import property_material_keys, property_process_keys
        cls.keys_material = property_material_keys
        cls.keys_process = property_process_keys
        cls.keys = {**cls.keys_material, **cls.keys_process}

    @classmethod
    def key_table(cls, _type: str = "html"):
        """ Prints or opens html of official property keys. """
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
