from typing import Union
from logging import getLogger

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.group import Group
from cript.data_model.nodes.collection import Collection
from cript.utils import auto_assign_group
from cript.paginator import Paginator


logger = getLogger(__name__)


class Experiment(BaseNode):
    """
    Object representing an experiment.
    """

    node_name = "Experiment"
    slug = "experiment"
    list_name = "experiments"

    @beartype
    def __init__(
        self,
        collection: Union[Collection, str],
        name: str,
        processes: str = None,
        computations: str = None,
        computational_processes: str = None,
        data: str = None,
        funding: list[Union[str, None]] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        group: Union[Group, str] = None,
    ):
        super().__init__(public=public)
        self.collection = collection
        self.name = name
        self.funding = funding if funding else []
        self.processes = processes
        self.computations = computations
        self.computational_processes = computational_processes
        self.data = data
        self.notes = notes
        self.group = auto_assign_group(group, collection)

    @property
    def processes(self):
        return self._processes

    @processes.setter
    def processes(self, value):
        self._processes = Paginator(url=value)

    @property
    def computational_processes(self):
        return self._computational_processes

    @computational_processes.setter
    def computational_processes(self, value):
        self._computational_processes = Paginator(url=value)

    @property
    def computations(self):
        return self._computations

    @computations.setter
    def computations(self, value):
        self._computations = Paginator(url=value)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = Paginator(url=value)
