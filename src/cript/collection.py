"""
Collection Node

"""

from . import CRIPTError
from .base import BaseModel, BaseReference


class CollectionError(CRIPTError):
    def __init__(self, *msg):
        super().__init__(*msg)


class Collection(BaseModel, _error=CollectionError):
    _class = "Collection"

    def __init__(
        self,
        name: str,
        c_collection=None,
        c_experiment=None,
        c_inventory=None,
        notes: str = None,
        **kwargs
    ):
        """
        :param name: The name of the collection.

        :param c_collection:
        :param c_experiment:
        :param c_inventory:

        :param notes: Any miscellaneous notes related to the user.
        :param _class: class of node.
        :param uid: The unique ID of the material.
        :param model_version: Version of CRIPT data model.
        :param version_control: Link to version control node.
        :param last_modified_date: Last date the node was modified.
        :param created_date: Date it was created.
        """
        super().__init__(name=name, _class=self._class, notes=notes, **kwargs)

        self.c_experiment = BaseReference("Experiment", c_experiment, self._error)
        self.c_collection = BaseReference("Collection", c_collection, self._error)
        self.c_inventory = BaseReference("Inventory", c_inventory, self._error)
