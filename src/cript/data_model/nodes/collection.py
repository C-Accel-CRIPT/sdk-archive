from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.group import Group
from cript.data_model.nodes.project import Project
from cript.data_model.paginator import Paginator
from cript.data_model.subobjects.citation import Citation
from cript.data_model.utils import auto_assign_group
from cript.data_model.paginator import Paginator

logger = getLogger(__name__)


class Collection(BaseNode):
    """The <a href="../collection" target="_blank">`Collection`</a> object
    represents a logical grouping of
    <a href="../experiment" target="_blank">`Experiment`</a> and
    <a href="../inventory" target="_blank">`Inventory`</a>
    objects. Each collection is nested inside of a 
    <a href="../project" target="_blank">`Project`</a>.

    Args:
        project (Union[Project, str]): The collection's parent `Project`
        name (str): Collection name
        experiments (str, optional): URL for list of experiments inside the collection
        inventories (str, optional): URL for list of inventories inside the collection
        notes (Union[str, None], optional): Collection notes
        citations (list[Union[Citation, dict]], optional): List of citations associated with the collection
        public (bool, optional): Whether the collection is publicly viewable
        group (Union[Group, str], optional): `Group` object that manages the collection
    
    !!! warning "Collection name uniqueness"
        Each <a href="../collection" target="_blank">`Collection`</a> name must be unique within a
        <a href="../project" target="_blank">`Project`</a> node.     

    !!! success "Collection methods"
        Since the `Collection` object inherits from the <a href="../base_node" target="_blank">`BaseNode`</a> object,
        all the <a href="../base_node" target="_blank">`BaseNode`</a> object methods can be used to manipulate a `Collection`. These include
        `get()`, `create()`, `delete()`, `save()`, `search()`, `update()`, and `refresh()` methods.
        See the <a href="../base_node" target="_blank">`BaseNode`</a> documentation to learn more about these methods.

    ``` py title="Example"
    # get an existing project
    my_project = Project.get(name="My project")

    # create a new collection in the existing project
    my_collection = Collection.create(
        project=my_project,
        name="My collection name",
    )

    # get another collection
    my_other_collection = Collection.get(
        name="My other collection name",
        project=my_project,
    )
    ```

    !!! question "Why is `Project` needed when getting a collection?"
        <a href="../collection" target="_blank">`Collection`</a> names are only unique within a project, not across all projects,
        so when getting a `Collection` via name,
        the associated <a href="../project" target="_blank">`Project`</a> node must also be specified.


    ``` json title="Example of a collection in JSON format"
    {
        "url": "https://criptapp.org/api/collection/336d0584-04f9-49fe-9c0d-78772e2f1ead/",
        "uid": "336d0584-04f9-49fe-9c0d-78772e2f1ead",
        "group": "https://criptapp.org/api/group/68ed4c57-d1ca-4708-89b2-cb1c1609ace2/",
        "project": "https://criptapp.org/api/project/910445b2-88ca-43ac-88cf-f6424e85b1ba/",
        "name": "Navid's Collecton",
        "notes": null,
        "experiments": "https://criptapp.org/api/collection/336d0584-04f9-49fe-9c0d-78772e2f1ead/experiments/",
        "inventories": "https://criptapp.org/api/collection/336d0584-04f9-49fe-9c0d-78772e2f1ead/inventories/",
        "citations": [],
        "created_at": "2022-11-23T00:59:01.453731Z",
        "updated_at": "2022-11-23T00:59:01.453756Z",
        "public": false
    }

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
        """Add a <a href="/../subobjects/citation" target="_blank">`Citation`</a> to the collection.

        Args:
            citation (Union[Citation, dict]): Citation to add
        
        ``` py title="Example"
        my_collection.add_citation(citation)
        ```
        """
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        """Remove a <a href="/../subobjects/citation" target="_blank">`Citation`</a> from the collection.

        Args:
            citation (Union[Citation, dict]): Citation to remove
        
        ``` py title="Example"
        my_collection.remove_citation(citation)
        ```
        """
        self._remove_node(citation, "citations")
