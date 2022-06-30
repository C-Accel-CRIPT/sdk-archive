from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes.primary.group import Group
from cript.nodes.secondary.citation import Citation
from cript.validators import validate_required


logger = getLogger(__name__)


class Collection(BasePrimary):
    """
    Object representing a logical grouping of :class:`Experiment` and
    :class:`Inventory` objects.
    """

    node_name = "Collection"
    slug = "collection"
    required = ["group", "name"]
    unique_together = ["name", "created_by"]

    @beartype
    def __init__(
        self,
        group: Union[Group, str] = None,
        name: str = None,
        experiments=None,
        inventories=None,
        notes: Union[str, None] = None,
        citations: list[Union[Citation, dict]] = None,
        public: bool = False,
    ):
        super().__init__(public=public)
        self.group = group
        self.name = name
        self.experiments = experiments if experiments else []
        self.inventories = inventories if inventories else []
        self.citations = citations if citations else []
        self.notes = notes
        validate_required(self)

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        self._remove_node(citation, "citations")
