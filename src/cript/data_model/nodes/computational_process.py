from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.data import Data
from cript.data_model.nodes.experiment import Experiment
from cript.data_model.nodes.group import Group
from cript.data_model.subobjects.citation import Citation
from cript.data_model.subobjects.condition import Condition
from cript.data_model.subobjects.ingredient import Ingredient
from cript.data_model.subobjects.property import Property
from cript.data_model.subobjects.software_configuration import SoftwareConfiguration
from cript.data_model.utils import auto_assign_group

logger = getLogger(__name__)


class ComputationalProcess(BaseNode):
    """The <a href="../computational_process" target="_blank">`ComputationalProcess`</a> object represents a
    computer simulation which processes or changes a virtual
    <a href="../material" target="_blank">`Material`</a> object.

    Args:
        experiment (Union[Experiment, str]): Parent `Experiment` of the `CopmutationalProcess`
        name (str): Computational process name
        type (str): Copmutational process type
        input_data (list[Union[Data, str]], optional): List of `Data` objects used as inputs to the computational process
        ingredients (list[Union[Ingredient, dict]], optional): List of `Ingredient` objects used as inputs to the computational process
        software_configurations (list[Union[SoftwareConfiguration, dict]], optional): List of `SoftwareConfiguration` objects associated with the computational process
        properties (list[Union[Property, dict]], optional): List of `Property` objects associated with the computational process
        conditions (list[Union[Condition, dict]], optional): List of `Condition` objects associated with the comnputational process
        output_data (list[Union[Data, str]], optional): List of `Data` objects used as outputs of the computational process
        citations (list[Union[Citation, dict]], optional): List of `Citation` objects linked to the computational process
        notes (Union[str, None], optional): Copmutational process notes
        public (bool, optional): Whether the computational process is publicly viewable
        group (Union[Group, str], optional): `Group` object which manages the computational process

    !!! warning "ComputationalProcess names must be unique"
        Each <a href="../computational_process" target="_blank">`CopmutationalProcess`</a> name must be unique within an
        <a href="../experiment" target="_blank">`Experiment`</a> node.     

    !!! success "Use <a href='../base_node' target='_blank'>`BaseNode`</a> methods to manipulate this object"
        Since this object inherits from the <a href="../base_node" target="_blank">`BaseNode`</a> object,
        all the <a href="../base_node" target="_blank">`BaseNode`</a> object methods can be used to manipulate it.
        These include `get()`, `create()`, `delete()`, `save()`, `search()`, `update()`, and `refresh()` methods.
        See the <a href="../base_node" target="_blank">`BaseNode`</a> documentation to learn more about these methods
        and see examples of their use.

    !!! note "Allowed `ComputationalProcess` types"
        The allowed `ComputationalProcess` types are listed in the
        <a href="https://criptapp.org/keys/computational-process-type/" target="_blank">CRIPT controlled vocabulary</a>.
        
    ``` py title="Example"
    # get an existing experiment
    my_exp = Experiment.get(name="My experiment")

    # create a new computational process in the existing experiment
    cp = ComputationalProcess.create(
        experiment=my_exp,
        name="reaction simulation",
        type="reaction",
    )
    ```
    """

    node_name = "ComputationalProcess"
    slug = "computational-process"
    alt_names = ["computational_processes"]

    @beartype
    def __init__(
        self,
        experiment: Union[Experiment, str],
        name: str,
        type: str,
        input_data: list[Union[Data, str]] = None,
        ingredients: list[Union[Ingredient, dict]] = None,
        software_configurations: list[Union[SoftwareConfiguration, dict]] = None,
        properties: list[Union[Property, dict]] = None,
        conditions: list[Union[Condition, dict]] = None,
        output_data: list[Union[Data, str]] = None,
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
        self.ingredients = ingredients if ingredients else []
        self.software_configurations = (
            software_configurations if software_configurations else []
        )
        self.properties = properties if properties else []
        self.conditions = conditions if conditions else []
        self.output_data = output_data if output_data else []
        self.citations = citations if citations else []
        self.notes = notes
        self.group = auto_assign_group(group, experiment)

    @beartype
    def add_input_data(self, data: Union[Data, dict]):
        """Add an input <a href="../data" target="_blank">`Data`</a> object to this `ComputationalProcess`.

        Args:
            data (Union[Data, dict]): `Data` object to add
        
        ``` py title="Example"
        cp.add_input_data(data)
        ```
        """
        self._add_node(data, "input_data")

    @beartype
    def remove_input_data(self, data: Union[Data, int]):
        """Remove an input <a href="../data" target="_blank">`Data`</a> object from this `ComputationalProcess`.

        Args:
            data (Union[Data, int]): `Data` object to remove
        
        ``` py title="Example"
        cp.remove_input_data(data)
        ```
        """
        self._remove_node(data, "input_data")

    @beartype
    def add_ingredient(self, ingredient: Union[Ingredient, dict]):
        """Add an <a href="/../subobjects/ingredient" target="_blank">`Ingredient`</a> object.

        Args:
            ingredient (Union[Ingredient, dict]): `Ingredient` to add
        
        ``` py title="Example"
        cp.add_ingredient(ingredient)
        ```
        """
        self._add_node(ingredient, "ingredients")

    @beartype
    def remove_ingredient(self, ingredient: Union[Ingredient, int]):
        """Remove an <a href="/../subobjects/ingredient" target="_blank">`Ingredient`</a> object.

        Args:
            ingredient (Union[Ingredient, int]): `Ingredient` to remove
        
        ``` py title="Example"
        cp.remove_ingredient(ingredient)
        ```
        """
        self._remove_node(ingredient, "ingredients")

    @beartype
    def add_software_configuration(
        self, configuration: Union[SoftwareConfiguration, dict]
    ):
        """Add a <a href="/../subobjects/software_configuration" target="_blank">`SoftwareConfiguration`</a> object.

        Args:
            configuration (Union[SoftwareConfiguration, dict]): `SoftwareConfiguration` to add
        
        ``` py title="Example"
        cp.add_software_configuration(configuration)
        ```
        """
        self._add_node(configuration, "software_configurations")

    @beartype
    def remove_software_configurations(
        self, configuration: Union[SoftwareConfiguration, int]
    ):
        """Remove a <a href="/../subobjects/software_configuration" target="_blank">`SoftwareConfiguration`</a> object.

        Args:
            configuration (Union[SoftwareConfiguration, int]): `SoftwareConfiguration` to remove
        
        ``` py title="Example"
        cp.remove_software_configuration(configuration)
        ```
        """
        self._remove_node(configuration, "software_configurations")

    @beartype
    def add_property(self, property: Union[Property, dict]):
        """Add a <a href="/../subobjects/property" target="_blank">`Property`</a> object.

        Args:
            property (Union[Property, dict]): `Property` to add
        
        ``` py title="Example"
        cp.add_property(property)
        ```
        """
        self._add_node(property, "properties")

    @beartype
    def remove_property(self, property: Union[Property, int]):
        """Remove a <a href="/../subobjects/property" target="_blank">`Property`</a> object.

        Args:
            property (Union[Property, int]): `Property` to remove
        
        ``` py title="Example"
        cp.remove_property(property)
        ```
        """
        self._remove_node(property, "properties")

    @beartype
    def add_condition(self, condition: Union[Condition, dict]):
        """Add a <a href="/../subobjects/condition" target="_blank">`Condition`</a> object.

        Args:
            condition (Union[Condition, dict]): `Condition` to add
        
        ``` py title="Example"
        cp.add_condition(condition)
        ```
        """
        self._add_node(condition, "conditions")

    @beartype
    def remove_condition(self, condition: Union[Condition, int]):
        """Remove a <a href="/../subobjects/condition" target="_blank">`Condition`</a> object.

        Args:
            condition (Union[Condition, int]): `Condition` to remove
        
        ``` py title="Example"
        cp.remove_condition(condition)
        ```
        """
        self._remove_node(condition, "conditions")

    @beartype
    def add_output_data(self, data: Union[Data, dict]):
        """Add an outnput <a href="../data" target="_blank">`Data`</a> object.

        Args:
            data (Union[Data, dict]): `Data` object to add
        
        ``` py title="Example"
        cp.add_output_data(data)
        ```
        """
        self._add_node(data, "output_data")

    @beartype
    def remove_output_data(self, data: Union[Data, int]):
        """Remove an output <a href="../data" target="_blank">`Data`</a> object.

        Args:
            data (Union[Data, int]): `Data` object to remove
        
        ``` py title="Example"
        cp.remove_output_data(data)
        ```
        """
        self._remove_node(data, "output_data")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        """Add a <a href="/../subobjects/citation" target="_blank">`Citation`</a> object.

        Args:
            citation (Union[Citation, dict]): `Citation` to add
        
        ``` py title="Example"
        cp.add_citation(citation)
        ```
        """
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        """Remove a <a href="/../subobjects/citation" target="_blank">`Citation`</a> object.

        Args:
            citation (Union[Citation, int]): `Citation` to remove
        
        ``` py title="Example"
        cp.remove_citation(citation)
        ```
        """
        self._remove_node(citation, "citations")
