from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.group import Group
from cript.data_model.nodes.project import Project
from cript.data_model.paginator import Paginator
from cript.data_model.subobjects.citation import Citation
from cript.data_model.utils import auto_assign_group

logger = getLogger(__name__)


class Collection(BaseNode):
    """Object representing a logical grouping of
    <a href="../experiment" target="_blank">`Experiment`</a> and
    <a href="../inventory" target="_blank">`Inventory`</a>
    objects. Each collection is nested inside of a 
    <a href="../project" target="_blank">`Project`</a>
    node.

    Args:
        project (Union[Project, str]): The collection's parent `Project`
        name (str): Collection name
        experiments (str, optional): URL for list of experiments inside this collection
        inventories (str, optional): URL for list of inventories inside this collection
        notes (Union[str, None], optional): Collection notes
        citations (list[Union[Citation, dict]], optional): List of citations associated with this collection
        public (bool, optional): Whether this collection is publicly viewable
        group (Union[Group, str], optional): `Group` object which manages this collection
    
    !!! warning "Collection names"
        Each `Collection` name must be unique within a `Project` node

    ```py title="Example"
    # get an existing project
    my_project = cript.Project.get(name="My project")
    # create the collection
    collection = Collection(
        project=my_project,
        name="My new collection",
        notes="
    )
    ```
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
        """Object representing a logical grouping of
        <a href="../experiment" target="_blank">`Experiment`</a> and
        <a href="../inventory" target="_blank">`Inventory`</a>
        objects. Each collection is nested inside of a 
        <a href="../project" target="_blank">`Project`</a>
        node.

        <a href="../base_node" target="_blank">basenode</a>

        Args:
            project (Union[Project, str]): The collection's parent `Project`
            name (str): Collection name
            experiments (str, optional): URL for list of experiments inside this collection
            inventories (str, optional): URL for list of inventories inside this collection
            notes (Union[str, None], optional): Collection notes
            citations (list[Union[Citation, dict]], optional): List of citations associated with this collection
            public (bool, optional): Whether this collection is publicly viewable
            group (Union[Group, str], optional): `Group` object which manages this collection
        
        !!! warning "Collection names"
            Each `Collection` name must be unique within a `Project` node

        ```py title="Example"
        # get an existing project
        my_project = cript.Project.get(name="My project")
        # create the collection
        collection = Collection(
            project=my_project,
            name="My new collection",
            notes="
        )
        ```
        """
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
