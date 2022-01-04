"""
Process Node

"""
from typing import Union

from .. import CRIPTError
from .base import BaseModel
from ..secondary_nodes.cond import Cond
from ..secondary_nodes.prop import Prop
from ..secondary_nodes.ingr import Ingr
from ..utils import TablePrinting, freeze_class, loading_with_units
from ..keys.process import process_keywords


class ProcessError(CRIPTError):
    pass


@freeze_class
class Process(TablePrinting, BaseModel, _error=ProcessError):
    """ Process



    Attributes
    ----------
    base_attributes:
        See CRIPT BaseModel
    ingr:
        See help(Ingr.__init__)
    procedure:
        Text write up of procedure
    cond:

    prop:

    keywords:

    """
    class_ = "Process"
    keys = process_keywords

    def __init__(
            self,
            name: str,
            ingr,
            procedure: str,
            cond: Union[Cond, list[Cond]] = None,
            prop: Union[Prop, list[Prop]] = None,
            keywords: list[str] = None,
            notes: str = None,
            **kwargs
    ):

        super().__init__(name=name, class_=self.class_, notes=notes, **kwargs)

        self._procedure = None
        self.procedure = procedure

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
    def procedure(self, procedure):
        self._procedure = procedure

    @property
    def prop(self):
        return self._prop

    @prop.setter
    @loading_with_units(Prop)
    def prop(self, prop):
        self._prop = prop

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        self._keywords = keywords

    @property
    def cond(self):
        return self._cond

    @cond.setter
    @loading_with_units(Cond)
    def cond(self, cond):
        self._cond = cond
