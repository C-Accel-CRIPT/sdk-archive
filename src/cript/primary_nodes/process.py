"""
Process Node

"""
from typing import Union

from .. import CRIPTError
from .base import BaseModel
from ..secondary_nodes.cond import Cond
from ..secondary_nodes.prop import Prop
from ..secondary_nodes.ingr import Ingr
from ..utils import TablePrinting, freeze_class, loading_with_units, convert_to_list
from ..validator import type_check, keys_check
from ..keys.process import process_keywords


class ProcessError(CRIPTError):
    """Process Error"""
    pass


@freeze_class
class Process(TablePrinting, BaseModel, _error=ProcessError):
    """ Process

    The Process node contains a list of ingredients, quantities, and procedure information for a material
    transformation. Examples of a process are chemical reactions, separations, extrusions, etc.

    Attributes
    ----------
    base_attributes:
        See CRIPT BaseModel
    ingr: list[Ingr]
        ingredients
        See help(Ingr)
    procedure: list[str]
        a series of actions conducted
        array can allow for discretization of steps.
    equipment: list[str]
        equipment used in the process
    cond: list[Cond]
        process conditions
        see help(Cond)
    prop: list[Prop]
        process properties
        see help(Prop)
    keywords: list[str]  (has keys)
        words that classify the process
        see `Process.key_table()`

    """
    class_ = "Process"
    keys = process_keywords

    def __init__(
            self,
            name: str,
            ingr,
            procedure: Union[list[str], str],
            equipment: Union[list[str], str],
            cond: Union[list[Cond], Cond] = None,
            prop: Union[list[Prop], Prop] = None,
            keywords: Union[list[str], str] = None,
            notes: str = None,
            **kwargs
    ):

        super().__init__(name=name, class_=self.class_, notes=notes, **kwargs)

        self._procedure = None
        self.procedure = procedure

        self._equipment = None
        self.equipment = equipment

        self._prop = None
        self.prop = prop

        self._keywords = None
        self.keywords = keywords

        self._cond = None
        self.cond = cond

        if isinstance(ingr, Ingr):
            self.ingr = ingr
        else:
            self.ingr = Ingr(ingr)

    @property
    def procedure(self):
        return self._procedure

    @procedure.setter
    @type_check(list[str])
    @convert_to_list
    def procedure(self, procedure):
        self._procedure = procedure

    @property
    def equipment(self):
        return self._equipment

    @equipment.setter
    @type_check(list[str])
    @convert_to_list
    def equipment(self, equipment):
        self._equipment = equipment

    @property
    def prop(self):
        return self._prop

    @prop.setter
    @type_check(list[Prop])
    @convert_to_list
    @loading_with_units(Prop)
    def prop(self, prop):
        self._prop = prop

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    @keys_check
    @type_check(list[str])
    @convert_to_list
    def keywords(self, keywords):
        self._keywords = keywords

    @property
    def cond(self):
        return self._cond

    @cond.setter
    @type_check(list[Cond])
    @convert_to_list
    @loading_with_units(Cond)
    def cond(self, cond):
        self._cond = cond
