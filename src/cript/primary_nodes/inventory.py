"""
Inventory Node

"""

from .. import CRIPTError
from ..utils import freeze_class
from ..mongodb import GetMaterial
from .base import BaseModel, ReferenceList


class InventoryError(CRIPTError):
    pass


@freeze_class
class Inventory(BaseModel, _error=InventoryError):
    """ Inventory Node

    Groouping of Material nodes

    Attributes
    ----------
    base_attributes:

    c_material: list[Material]
        Materials used in this experiment
    """
    class_ = "Inventory"

    def __init__(
        self,
        name: str,
        c_material=None,
        notes: str = None,
        **kwargs
    ):
        super().__init__(name=name, class_=self.class_, notes=notes, **kwargs)

        self._c_material = ReferenceList("Material", c_material, self._error)

    @property
    def c_material(self):
        return self._c_material

    @c_material.setter
    def c_material(self, *args):
        self._base_reference_block()

    def get(self, target):
        """ Given a target (chemical name, cas number or some other identity) find material node."""
        return GetMaterial.get(target, self.c_material())
