from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes.primary.group import Group
from cript.nodes.primary.collection import Collection
from cript.utils import auto_assign_group


logger = getLogger(__name__)


class Experiment(BasePrimary):
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
        processes=None,
        computations: list[Union[BasePrimary, str]] = None,
        computational_processes: list[Union[BasePrimary, str]] = None,
        data=None,
        funding: list[Union[str, None]] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        group: Union[Group, str] = None,
    ):
        super().__init__(public=public)
        self.collection = collection
        self.name = name
        self.funding = funding if funding else []
        self.processes = processes if processes else []
        self.computational_processes = (
            computational_processes if computational_processes else []
        )
        self.computations = computations if computations else []
        self.data = data if data else []
        self.notes = notes
        self.group = auto_assign_group(group, collection)

    @beartype
    def add_computation(self, computation: Union[BasePrimary, dict]):
        self._add_node(computation, "computations")

    @beartype
    def remove_computation(self, computation: Union[BasePrimary, int]):
        self._remove_node(computation, "computations")

    @beartype
    def add_computational_process(
        self, computational_process: Union[BasePrimary, dict]
    ):
        self._add_node(computational_process, "computational_processes")

    @beartype
    def remove_computational_process(
        self, computational_process: Union[BasePrimary, int]
    ):
        self._remove_node(computational_process, "computational_processes")
