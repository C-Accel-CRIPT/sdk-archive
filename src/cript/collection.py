"""
Collection Node

"""

from . import BaseModel


class Collection(BaseModel):

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

        self._c_collection = None
        self.c_collection = c_collection

        self._c_experiment = None
        self.c_experiment = c_experiment

        self._c_inventory = None
        self.c_inventory = c_inventory

    @property
    def c_collection(self):
        return self._c_collection

    @c_collection.setter
    def c_collection(self, c_collection):
        self._setter_CRIPT_prop(c_collection, "c_collection")

    @property
    def c_experiment(self):
        return self._c_experiment

    @c_experiment.setter
    def c_experiment(self, c_experiment):
        self._setter_CRIPT_prop(c_experiment, "c_experiment")

    @property
    def c_inventory(self):
        return self._c_inventory

    @c_inventory.setter
    def c_inventory(self, c_inventory):
        self._setter_CRIPT_prop(c_inventory, "c_inventory")
