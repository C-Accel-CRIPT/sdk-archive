from typing import Union
from logging import getLogger

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.group import Group
from cript.data_model.nodes.project import Project
from cript.data_model.subobjects.citation import Citation
from cript.data_model.utils import auto_assign_group
from cript.data_model.paginator import Paginator
from cript.cache import get_cached_api_session


logger = getLogger(__name__)


class Collection(BaseNode):
    """
    Object representing a logical grouping of `Experiment` and
    `Inventory` objects.
    """

    node_name = "Collection"
    slug = "collection"
    alt_names = ["collections"]

    @beartype
    def __init__(
        self,
        project: Union[Project, str],
        name: str,
        experiments: str = None,
        inventories: str = None,
        notes: Union[str, None] = None,
        citations: list[Union[Citation, dict]] = None,
        public: bool = False,
        group: Union[Group, str] = None,
        **kwargs,
    ):
        super().__init__(public=public, **kwargs)
        self.project = project
        self.name = name
        self.experiments = experiments
        self.inventories = inventories
        self.citations = citations if citations else []
        self.notes = notes
        self.group = auto_assign_group(group, project)

    @property
    def experiments(self):
        return self._experiments

    @experiments.setter
    def experiments(self, value):
        if value:
            self._experiments = Paginator(url=value, node_name="Experiment")

    @property
    def inventories(self):
        return self._inventories

    @inventories.setter
    def inventories(self, value):
        if value:
            self._inventories = Paginator(url=value, node_name="Inventory")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        self._remove_node(citation, "citations")
