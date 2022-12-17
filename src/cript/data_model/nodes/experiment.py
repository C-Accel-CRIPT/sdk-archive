from typing import Union
from logging import getLogger

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.group import Group
from cript.data_model.nodes.collection import Collection
from cript.data_model.utils import auto_assign_group
from cript.data_model.paginator import Paginator
from cript.cache import get_cached_api_session


logger = getLogger(__name__)


class Experiment(BaseNode):
    """
    Object representing an experiment.
    """

    node_name = "Experiment"
    slug = "experiment"
    alt_names = ["experiments"]

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
        **kwargs,
    ):
        super().__init__(public=public, **kwargs)
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
        if value:
            self._processes = Paginator(url=value, node_name="Process")

    @property
    def computational_processes(self):
        return self._computational_processes

    @computational_processes.setter
    def computational_processes(self, value):
        if value:
            self._computational_processes = Paginator(
                url=value, node_name="ComputationalProcess"
            )

    @property
    def computations(self):
        return self._computations

    @computations.setter
    def computations(self, value):
        if value:
            self._computations = Paginator(url=value, node_name="Computation")

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if value:
            self._data = Paginator(url=value, node_name="Data")
