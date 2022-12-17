from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.group import Group
from cript.data_model.nodes.project import Project
from cript.data_model.subobjects.base_subobject import BaseSubobject
from cript.data_model.subobjects.identifier import Identifier
from cript.data_model.subobjects.property import Property
from cript.data_model.utils import auto_assign_group

logger = getLogger(__name__)


class Material(BaseNode):
    """Object representing a material, mixture or compound."""

    node_name = "Material"
    slug = "material"
    alt_names = ["materials", "components", "products", "waste"]

    @beartype
    def __init__(
        self,
        project: Union[Project, str],
        name: str,
        identifiers: list[Union[Identifier, dict]] = None,
        components: list[Union[BaseNode, str]] = None,
        keywords: Union[list[str], None] = None,
        properties: list[Union[Property, dict]] = None,
        process: Union[BaseNode, str, None] = None,
        computational_forcefield: Union[BaseSubobject, dict, None] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        group: Union[Group, str] = None,
        **kwargs,
    ):
        super().__init__(public=public, **kwargs)
        self.project = project
        self.name = name
        self.identifiers = identifiers if identifiers else []
        self.components = components if components else []
        self.keywords = keywords if keywords else []
        self.properties = properties if properties else []
        self.process = process
        self.computational_forcefield = computational_forcefield
        self.notes = notes
        self.group = auto_assign_group(group, project)

    @beartype
    def add_identifier(self, identifier: Union[Identifier, dict]):
        self._add_node(identifier, "identifiers")

    @beartype
    def remove_identifier(self, identifier: Union[Identifier, int]):
        self._remove_node(identifier, "identifiers")

    @beartype
    def add_component(self, component: Union[BaseNode, dict]):
        self._add_node(component, "components")

    @beartype
    def remove_component(self, component: Union[BaseNode, int]):
        self._remove_node(component, "components")

    @beartype
    def add_property(self, property: Union[Property, dict]):
        self._add_node(property, "properties")

    @beartype
    def remove_property(self, property: Union[Property, int]):
        self._remove_node(property, "properties")
