from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes import Group, Citation
from cript.validators import validate_key
from cript.utils import auto_assign_group


logger = getLogger(__name__)


class Data(BasePrimary):
    """
    Object representing a set of `File` objects and
    related meta-data.
    """

    node_name = "Data"
    slug = "data"
    list_name = "data"

    @beartype
    def __init__(
        self,
        experiment: Union[BasePrimary, str],
        name: str,
        type: str,
        files=None,
        sample_preparation: Union[BasePrimary, str, None] = None,
        computations: list[Union[BasePrimary, str]] = None,
        computational_process: Union[BasePrimary, str, None] = None,
        materials=None,
        processes=None,
        notes: Union[str, None] = None,
        citations: list[Union[Citation, dict]] = None,
        public: bool = False,
        group: Union[Group, str] = None,
    ):
        super().__init__(public=public)
        self.experiment = experiment
        self.name = name
        self.files = files
        self.type = type
        self.sample_preparation = sample_preparation
        self.computations = computations if computations else []
        self.computational_process = computational_process
        self.materials = materials if materials else []
        self.processes = processes if processes else []
        self.citations = citations if citations else []
        self.notes = notes
        self.group = auto_assign_group(group, experiment)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = validate_key("data-type", value)

    @beartype
    def add_computation(self, computation: Union[BasePrimary, dict]):
        self._add_node(computation, "computations")

    @beartype
    def remove_computation(self, computation: Union[BasePrimary, int]):
        self._remove_node(computation, "computations")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        self._remove_node(citation, "citations")
