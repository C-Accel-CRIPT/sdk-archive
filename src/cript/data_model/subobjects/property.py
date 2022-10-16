from typing import Union
from logging import getLogger

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.data import Data
from cript.data_model.nodes.computation import Computation
from cript.data_model.subobjects.base_subobject import BaseSubobject
from cript.data_model.subobjects.condition import Condition
from cript.data_model.subobjects.citation import Citation


logger = getLogger(__name__)


class Property(BaseSubobject):
    """
    Object representing an observed or measured attribute
    of a `Material` or `Process` object.
    """

    node_name = "Property"
    list_name = "properties"

    @beartype
    def __init__(
        self,
        key: str,
        value: Union[str, int, float, list, None] = None,
        unit: Union[str, None] = None,
        type: Union[str, None] = None,
        method: Union[str, None] = None,
        method_description: Union[str, None] = None,
        sample_preparation: Union[BaseNode, str, None] = None,
        uncertainty: Union[float, int, None] = None,
        uncertainty_type: Union[str, None] = None,
        components: list[Union[BaseNode, str]] = None,
        components_relative: list[Union[BaseNode, str]] = None,
        structure: Union[str, None] = None,
        set_id: Union[int, None] = None,
        conditions: list[Union[Condition, dict]] = None,
        data: Union[Data, str, None] = None,
        computations: list[Union[Computation, str]] = None,
        citations: list[Union[Citation, dict]] = None,
        notes: Union[str, None] = None,
    ):
        super().__init__()
        self.key = key
        self.unit = unit
        self.value = value
        self.type = type
        self.method = method
        self.method_description = method_description
        self.sample_preparation = sample_preparation
        self.uncertainty = uncertainty
        self.uncertainty_type = uncertainty_type
        self.components = components if components else []
        self.components_relative = components_relative if components_relative else []
        self.structure = structure
        self.set_id = set_id
        self.conditions = conditions if conditions else []
        self.data = data
        self.computations = computations if computations else []
        self.citations = citations if citations else []
        self.notes = notes

    @beartype
    def add_components(self, component: Union[BaseNode, dict]):
        self._add_node(component, "components")

    @beartype
    def remove_components(self, component: Union[BaseNode, int]):
        self._remove_node(component, "components")

    @beartype
    def add_components_relative(self, component: Union[BaseNode, dict]):
        self._add_node(component, "components_relative")

    @beartype
    def remove_components_relative(self, component: Union[BaseNode, int]):
        self._remove_node(component, "components_relative")

    @beartype
    def add_computation(self, computation: Union[Condition, dict]):
        self._add_node(computation, "computations")

    @beartype
    def remove_computation(self, computation: Union[Condition, int]):
        self._remove_node(computation, "computations")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        self._add_node(citation, "citations")

    @beartype
    def remove_condition(self, condition: Union[Condition, int]):
        self._remove_node(condition, "conditions")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        self._remove_node(citation, "citations")
