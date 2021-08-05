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
        super().__init__(name=name, _class=self._class, notes=notes, **kwargs)

        self._c_material = None
        self.c_material = c_material

    @property
    def c_material(self):
        return self._c_material

    @c_material.setter
    def c_material(self, c_material):
        self._setter_CRIPT_prop(c_material, "c_material")
