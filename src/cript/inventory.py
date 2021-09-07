"""
Inventory Node

"""

from . import CRIPTError
from .base import BaseModel, BaseReference
from .utils.external_database_code import GetMaterial


class InventoryError(CRIPTError):
    def __init__(self, *msg):
        super().__init__(*msg)


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

        self.c_material = BaseReference("Material", c_material, self._error)

    def get(self, target):
        return GetMaterial.get(target, self.c_material())
