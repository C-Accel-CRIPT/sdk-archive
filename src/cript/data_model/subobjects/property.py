from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.computation import Computation
from cript.data_model.nodes.data import Data
from cript.data_model.subobjects.base_subobject import BaseSubobject
from cript.data_model.subobjects.citation import Citation
from cript.data_model.subobjects.condition import Condition

logger = getLogger(__name__)


class Property(BaseSubobject):
    """
    Object representing an observed or measured attribute
    of a `Material` or `Process` object.

    Args:
        key (str): Property key
        value (Union[str, int, float, list, None], optional): Property value
        unit (Union[str, None], optional): Property unit
        type (Union[str, None], optional):Property type
        method (Union[str, None], optional): Property method
        method_description (Union[str, None], optional): Property method description
        sample_preparation (Union[BaseNode, str, None], optional): Sample preparation
        uncertainty (Union[float, int, None], optional): Property uncertainty
        uncertainty_type (Union[str, None], optional): Property uncertainty type
        components (list[Union[BaseNode, str]], optional): List of `Component` objects
        components_relative (list[Union[BaseNode, str]], optional): List of relative `Component` objects
        structure (Union[str, None], optional): Property structure
        set_id (Union[int, None], optional): Property set ID
        conditions (list[Union[Condition, dict]], optional): List of `Condition` objects associated with this property
        data (Union[Data, str, None], optional): `Data` object associated with this property
        computations (list[Union[Computation, str]], optional): List of `Computation` objects associated with this property
        citations (list[Union[Citation, dict]], optional): List of `Citation` objects associated with this property
        notes (Union[str, None], optional): Property nodes

    ``` py title="Example"
    property = Property(
        key="contact_angle",
        value=18.3,
        unit="deg",
        method=["Contact angle measurement"],
        uncertainty=0.4,
        uncertainty_type="stdev",
        notes="Measured on SiO2 wafer",
    )
    ```
    """

    node_name = "Property"
    alt_names = ["properties"]

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
        """Add a component to this property.

        Args:
            component (Union[BaseNode, dict]): Component to add

        ``` py title="Example"
        property.add_components(component)
        ```
        """
        self._add_node(component, "components")

    @beartype
    def remove_components(self, component: Union[BaseNode, int]):
        """Remove a component from this proeprty.

        Args:
            component (Union[BaseNode, int]): Component to remove

        ``` py title="Example"
        property.remove_components(component)
        ```
        """
        self._remove_node(component, "components")

    @beartype
    def add_components_relative(self, component: Union[BaseNode, dict]):
        """Add a relative component to this property.

        Args:
            component (Union[BaseNode, dict]): Relative component to add

        ``` py title="Example"
        property.add_components_relative(component)
        ```
        """
        self._add_node(component, "components_relative")

    @beartype
    def remove_components_relative(self, component: Union[BaseNode, int]):
        """Remove a relative component from this property.

        Args:
            component (Union[BaseNode, int]): Relative component to remove

        ``` py title="Example"
        property.remove_components_relative(component)
        ```
        """
        self._remove_node(component, "components_relative")

    @beartype
    def add_computation(self, computation: Union[Computation, dict]):
        """Add a `Computation` object to this property.

        Args:
            computation (Union[Computation, dict]): Computation to add

        ``` py title="Example"
        property.add_computation(computation)
        ```
        """
        self._add_node(computation, "computations")

    @beartype
    def remove_computation(self, computation: Union[Condition, int]):
        """Remove a computation from this property.

        Args:
            computation (Union[Computation, int]): Computation to remove

        ``` py title="Example"
        property.remove_computation(computation)
        ```
        """
        self._remove_node(computation, "computations")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        """Add a `Citation` object to this property.

        Args:
            citation (Union[Citation, dict]): `Citation` to add

        ``` py title="Example"
        property.add_citation(citation)
        ```
        """
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        """Remove a `Citation` object from this property.

        Args:
            citation (Union[Citation, int]): `Citation` to remove

        ``` py title="Example"
        property.remove_citation(citation)
        ```
        """
        self._remove_node(citation, "citations")

    @beartype
    def add_condition(self, condition: Union[Condition, int]):
        """Add a `Condition` object to this property.

        Args:
            condition (Union[Condition, int]): `Condition` to add

        ``` py title="Example"
        property.add_cndition(condition)
        ```
        """
        self._remove_node(condition, "conditions")

    @beartype
    def remove_condition(self, condition: Union[Condition, int]):
        """Remove a `Condition` object from this property.

        Args:
            condition (Union[Condition, int]): `Condition` to remove.

        ``` py title="Example"
        property.remove_condition(condition)
        ```
        """
        self._remove_node(condition, "conditions")
