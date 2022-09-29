from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes.primary.group import Group
from cript.nodes.primary.data import Data
from cript.nodes.secondary.software_configuration import SoftwareConfiguration
from cript.nodes.secondary.condition import Condition
from cript.nodes.secondary.citation import Citation
from cript.validators import validate_key
from cript.utils import auto_assign_group


logger = getLogger(__name__)


class Computation(BasePrimary):
    """
    Object representing the transformation of data or the creation
    of a computational data set
    """

    node_name = "Computation"
    slug = "computation"
    list_name = "computations"

    @beartype
    def __init__(
        self,
        experiment: Union[BasePrimary, str],
        name: str,
        type: str,
        input_data: list[Union[Data, str]] = None,
        software_configurations: list[Union[SoftwareConfiguration, dict]] = None,
        conditions: list[Union[Condition, dict]] = None,
        output_data: list[Union[Data, str]] = None,
        prerequisite_computation: Union[BasePrimary, str] = None,
        citations: list[Union[Citation, dict]] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        group: Union[Group, str] = None,
    ):
        super().__init__(public=public)
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

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = validate_key("computation-type", value)

    @beartype
    def add_input_data(self, data: Union[Data, dict]):
        self._add_node(data, "input_data")

    @beartype
    def remove_input_data(self, data: Union[Data, int]):
        self._remove_node(data, "input_data")

    @beartype
    def add_condition(self, condition: Union[Condition, dict]):
        self._add_node(condition, "conditions")

    @beartype
    def remove_condition(self, condition: Union[Condition, int]):
        self._remove_node(condition, "conditions")

    @beartype
    def add_software_configuration(
        self, configuration: Union[SoftwareConfiguration, dict]
    ):
        self._add_node(configuration, "software_configurations")

    @beartype
    def remove_software_configurations(
        self, configuration: Union[SoftwareConfiguration, int]
    ):
        self._remove_node(configuration, "software_configurations")

    @beartype
    def add_output_data(self, data: Union[Data, dict]):
        self._add_node(data, "output_data")

    @beartype
    def remove_output_data(self, data: Union[Data, int]):
        self._remove_node(data, "output_data")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        self._remove_node(citation, "citations")
