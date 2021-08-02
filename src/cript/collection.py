"""
Collection Node

"""

from .base import BaseModel
from .utils.type_check import *


class Collection(BaseModel):

    _class = "Collection"

    def __init__(
        self,
        name: str,
        c_collection=None,
        c_experiment=None,
        notes: str = None,
        **kwargs
    ):
        """
        :param name: The name of the collection.

        :param c_collection:
        :param c_experiment:

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

    @property
    def c_collection(self):
        return self._c_collection

    @c_collection.setter
    def c_collection(self, c_collection):
        self._set_CRIPT_prop(c_collection, "c_collection")

    @property
    def c_experiment(self):
        return self._c_experiment

    @c_experiment.setter
    def c_experiment(self, c_experiment):
        self._set_CRIPT_prop(c_experiment, "c_experiment")
