"""
Inventory Node

"""

from . import CRIPTError
from .base import BaseModel, BaseSlot
from .utils.external_database_code import GetMaterial
from .utils.class_tools import freeze_class


class InventoryError(CRIPTError):
    pass


@freeze_class
class Inventory(BaseModel, _error=InventoryError):
    class_ = "Inventory"

    def __init__(
        self,
        name: str,
        c_material: list = None,
        notes: str = None,
        **kwargs
    ):
        """

        :param name: The name of the collection.

        :param notes: Any miscellaneous notes related to the user.

        :param _class: class of node.
        :param uid: The unique ID of the material.
        :param model_version: Version of CRIPT data model.
        :param version_control: Link to version control node.
        :param last_modified_date: Last date the node was modified.
        :param created_date: Date it was created.
        """
        super().__init__(name=name, class_=self.class_, notes=notes, **kwargs)

        self._c_material = BaseSlot("Material", c_material, self._error)

    @property
    def c_material(self):
        return self._c_material

    @c_material.setter
    def c_material(self, *args):
        self._base_slot_block()

    def get(self, target):
        return GetMaterial.get(target, self.c_material())
