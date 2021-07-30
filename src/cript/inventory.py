"""
Inventory Node

"""
from typing import Union

from .base import BaseModel
import cript.material


class Inventory(BaseModel):

    _class = "Inventory"

    def __init__(
        self,
        name: str,
        materials: Union[list[cript.material.Material], list[list[str, str]]] = None,
        notes: str = None
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
        super().__init__(name=name, _class=self._class, notes=notes)

        self._materials = None
        self.materials = materials

    @property
    def materials(self):
        return self._materials

    @materials.setter
    def materials(self, materials):
        self._materials = materials

    def add(self, material):
        if self.materials is None:
            mat_list = self.materials
            self.materials = mat_list.append()
