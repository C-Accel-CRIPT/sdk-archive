from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.data import Data
from cript.data_model.nodes.group import Group
from cript.data_model.subobjects.citation import Citation
from cript.data_model.subobjects.condition import Condition
from cript.data_model.subobjects.software_configuration import SoftwareConfiguration
from cript.data_model.utils import auto_assign_group

logger = getLogger(__name__)


class Computation(BaseNode):
    """The <a href="../computation" target="_blank">`Computation`</a> object represents a
    single computation that is used for calculating a value, transforming some data,
    or creating a data set. Each <a href="../Computation" target="_blank">`Computation`</a> is
    nested inside a single <a href="../experiment" target="_blank">`Experiment`</a>.

    Args:
        experiment (Union[BaseNode, str]): The computation's parent `Experiment`
        name (str): Computation name
        type (str): Computation type
        input_data (list[Union[Data, str]], optional): List of `Data` objects used as inputs to the computation
        software_configurations (list[Union[SoftwareConfiguration, dict]], optional): List of `SoftwareConfiguration` objects used in the computation
        conditions (list[Union[Condition, dict]], optional): List of `Condition` objects associated with the computation
        output_data (list[Union[Data, str]], optional): List of `Data` objects which are produced by the computation
        prerequisite_computation (Union[BaseNode, str, None], optional): A `Computation` object which always preceeds the current computation
        citations (list[Union[Citation, dict]], optional): List of `Citation` objects which link references to the computation
        notes (Union[str, None], optional): Computation notes
        public (bool, optional): Whether the computation is publicly viewable
        group (Union[Group, str], optional): `Group` which manages the computation

    !!! warning "Computation names must be unique"
        Each <a href="../computation" target="_blank">`Copmutation`</a> name must be unique within an
        <a href="../experiment" target="_blank">`Experiment`</a> node.     

    !!! success "Use <a href='../base_node' target='_blank'>`BaseNode`</a> methods to manipulate this object"
        Since this object inherits from the <a href="../base_node" target="_blank">`BaseNode`</a> object,
        all the <a href="../base_node" target="_blank">`BaseNode`</a> object methods can be used to manipulate it.
        These include `get()`, `create()`, `delete()`, `save()`, `search()`, `update()`, and `refresh()` methods.
        See the <a href="../base_node" target="_blank">`BaseNode`</a> documentation to learn more about these methods
        and see examples of their use.

    !!! note "Allowed `Computation` types"
        The allowed `Computation` types are listed in the [CRIPT controlled vocabulary](https://criptapp.org/keys/computation-type/).
        
    ``` py title="Example"
    # get an existing experiment
    my_exp = Experiment.get(name="My experiment")

    # create a new computation in the existing experiment
    computation = Computation.create(
        experiment=my_exp,
        name="k-means clustering",
        type="analysis",
    )
    ```
    """

    node_name = "Computation"
    slug = "computation"
    alt_names = ["computations"]

    @beartype
    def __init__(
        self,
        experiment: Union[BaseNode, str],
        name: str,
        type: str,
        input_data: list[Union[Data, str]] = None,
        software_configurations: list[Union[SoftwareConfiguration, dict]] = None,
        conditions: list[Union[Condition, dict]] = None,
        output_data: list[Union[Data, str]] = None,
        prerequisite_computation: Union[BaseNode, str, None] = None,
        citations: list[Union[Citation, dict]] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        group: Union[Group, str] = None,
        **kwargs,
    ):
        super().__init__(public=public, **kwargs)
        self.experiment = experiment
        self.name = name
        self.type = type
        self.input_data = input_data if input_data else []
        self.software_configurations = (
            software_configurations if software_configurations else []
        )
        self.conditions = conditions if conditions else []
        self.output_data = output_data if output_data else []
        self.prerequisite_computation = prerequisite_computation
        self.citations = citations if citations else []
        self.notes = notes
        self.group = auto_assign_group(group, experiment)

    @beartype
    def add_input_data(self, data: Union[Data, dict]):
        """Add an input <a href="../data" target="_blank">`Data`</a> object to this `Computation`.

        Args:
            data (Union[Data, dict]): `Data` object to add
        
        ``` py title="Example"
        computation.add_input_data(data)
        ```
        """
        self._add_node(data, "input_data")

    @beartype
    def remove_input_data(self, data: Union[Data, int]):
        """Remove an input <a href="../data" target="_blank">`Data`</a> object from this `Computation`.

        Args:
            data (Union[Data, int]): `Data` object to remove
        
        ``` py title="Example"
        computation.remove_input_data(data)
        ```
        """
        self._remove_node(data, "input_data")

    @beartype
    def add_condition(self, condition: Union[Condition, dict]):
        """Add a <a href="/../subobjects/condition" target="_blank">`Condition`</a> object to this `Computation`.

        Args:
            condition (Union[Condition, dict]): `Condition` to add
        
        ``` py title="Example"
        computation.add_condition(condition)
        ```
        """
        self._add_node(condition, "conditions")

    @beartype
    def remove_condition(self, condition: Union[Condition, int]):
        """Remove a <a href="/../subobjects/condition" target="_blank">`Condition`</a> object from this `Computation`.

        Args:
            condition (Union[Condition, int]): `Condition` to remove
        
        ``` py title="Example"
        computation.remove_condition(condition)
        ```
        """
        self._remove_node(condition, "conditions")

    @beartype
    def add_software_configuration(
        self, configuration: Union[SoftwareConfiguration, dict]
    ):
        """Add a <a href="/../subobjects/software_configuration" target="_blank">`SoftwareConfiguration`</a> object to this `Computation`.

        Args:
            configuration (Union[SoftwareConfiguration, dict]): `SoftwareConfiguration` to add
        
        ``` py title="Example"
        computation.add_software_configuration(configuration)
        ```
        """
        self._add_node(configuration, "software_configurations")

    @beartype
    def remove_software_configurations(
        self, configuration: Union[SoftwareConfiguration, int]
    ):
        """Remove a <a href="/../subobjects/software_configuration" target="_blank">`SoftwareConfiguration`</a> object from this `Computation`.

        Args:
            configuration (Union[SoftwareConfiguration, int]): `SoftwareConfiguration` to remove
        
        ``` py title="Example"
        computation.remove_software_configuration(configuration)
        ```
        """
        self._remove_node(configuration, "software_configurations")

    @beartype
    def add_output_data(self, data: Union[Data, dict]):
        """Add an outnput <a href="../data" target="_blank">`Data`</a> object to this `Computation`.

        Args:
            data (Union[Data, dict]): `Data` object to add
        
        ``` py title="Example"
        computation.add_output_data(data)
        ```
        """
        self._add_node(data, "output_data")

    @beartype
    def remove_output_data(self, data: Union[Data, int]):
        """Remove an output <a href="../data" target="_blank">`Data`</a> object from this `Computation`.

        Args:
            data (Union[Data, int]): `Data` object to remove.
        
        ``` py title="Example"
        computation.remove_output_data(data)
        ```
        """
        self._remove_node(data, "output_data")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        """Add a <a href="/../subobjects/citation" target="_blank">`Citation`</a> object to this `Computation`.

        Args:
            citation (Union[Citation, dict]): `Citation` to add
        
        ``` py title="Example"
        computation.add_citation(citation)
        ```
        """
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        """Remove a <a href="/../subobjects/citation" target="_blank">`Citation`</a> object from this `Computation`.

        Args:
            citation (Union[Citation, int]): `Citation` to remove
        
        ``` py title="Example"
        computation.remove_citation(citation)
        ```
        """
        self._remove_node(citation, "citations")
