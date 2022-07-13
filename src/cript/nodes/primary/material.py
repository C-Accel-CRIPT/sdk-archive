from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes import Group, Identifier, Component, Property
from cript.validators import validate_required, validate_key


logger = getLogger(__name__)


class Material(BasePrimary):
    """Object representing a material, mixture or compound."""

    node_name = "Material"
    slug = "material"
    list_name = "materials"
    required = ["group", "name"]
    unique_together = ["name", "created_by"]

    @beartype
    def __init__(
        self,
        group: Union[Group, str] = None,
        name: str = None,
        identifiers: list[Union[Identifier, dict]] = None,
        components: list[Union[Component, dict]] = None,
        keywords: Union[list[str], None] = None,
        process: Union[BasePrimary, str, None] = None,  # Needs more specific type check
        properties: list[Union[Property, dict]] = None,
        notes: Union[str, None] = None,
        public: bool = False,
    ):
        super().__init__(public=public)
        self.group = group
        self.name = name
        self.identifiers = identifiers if identifiers else []
        self.components = components if components else []
        self.keywords = keywords if keywords else []
        self.process = process
        self.properties = properties if properties else []
        self.notes = notes
        validate_required(self)

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, value):
        if value:
            for i in range(len(value)):
                value[i] = validate_key("material-keyword", value[i])
        self._keywords = value

    @beartype
    def add_identifier(self, identifier: Union[Identifier, dict]):
        self._add_node(identifier, "identifiers")

    @beartype
    def remove_identifier(self, identifier: Union[Identifier, int]):
        self._remove_node(identifier, "identifiers")

    @beartype
    def add_component(self, component: Union[Component, dict]):
        self._add_node(component, "components")

    @beartype
    def remove_component(self, component: Union[Component, int]):
        self._remove_node(component, "components")

    @beartype
    def add_property(self, property: Union[Property, dict]):
        self._add_node(property, "properties")

    @beartype
    def remove_property(self, property: Union[Property, int]):
        self._remove_node(property, "properties")
