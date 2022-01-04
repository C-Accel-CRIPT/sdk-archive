"""
Collection Node

"""

from .. import CRIPTError
from ..utils import freeze_class
from .base import BaseModel, ReferenceList


class CollectionError(CRIPTError):
    """ Errors from the Collection Node

    """
    pass


@freeze_class
class Collection(BaseModel, _error=CollectionError):
    """ Collection Node


        Attributes
        ----------
        base_attributes:
            see CRIPT BaseModel
        c_collection: Collection node
            Parent CRIPT collections
        c_experiment: Experiment node
            CRIPT experiments that relates to the collection
        c_inventory: Inventory node
            CRIPT inventory associate with the collection
    """

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
        super().__init__(name=name, class_=self.class_, notes=notes, **kwargs)

        self._c_experiment = ReferenceList("Experiment", c_experiment, self._error)
        self._c_collection = ReferenceList("Collection", c_collection, self._error)
        self._c_inventory = ReferenceList("Inventory", c_inventory, self._error)

    @property
    def c_experiment(self):
        return self._c_experiment

    @c_experiment.setter
    def c_experiment(self, *args):
        self._base_reference_block()

    @property
    def c_collection(self):
        return self._c_collection

    @c_collection.setter
    def c_collection(self, *args):
        self._base_reference_block()

    @property
    def c_inventory(self):
        return self._c_inventory

    @c_inventory.setter
    def c_inventory(self, *args):
        self._base_reference_block()
