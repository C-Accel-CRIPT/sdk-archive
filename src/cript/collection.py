"""
Collection Node

"""

from . import CRIPTError
from .base import BaseModel, BaseSlot
from .utils.class_tools import freeze_class


class CollectionError(CRIPTError):
    pass


@freeze_class
class Collection(BaseModel, _error=CollectionError):
    class_ = "Collection"

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
        super().__init__(name=name, class_=self.class_, notes=notes, **kwargs)

        self._c_experiment = BaseSlot("Experiment", c_experiment, self._error)
        self._c_collection = BaseSlot("Collection", c_collection, self._error)
        self._c_inventory = BaseSlot("Inventory", c_inventory, self._error)

    @property
    def c_experiment(self):
        return self._c_experiment

    @c_experiment.setter
    def c_experiment(self, *args):
        self._base_slot_block()

    @property
    def c_collection(self):
        return self._c_collection

    @c_collection.setter
    def c_collection(self, *args):
        self._base_slot_block()

    @property
    def c_inventory(self):
        return self._c_inventory

    @c_inventory.setter
    def c_inventory(self, *args):
        self._base_slot_block()
