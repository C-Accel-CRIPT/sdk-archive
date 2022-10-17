from typing import Union
from logging import getLogger

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.group import Group
from cript.data_model.nodes.file import File
from cript.data_model.subobjects.citation import Citation
from cript.data_model.utils import auto_assign_group


logger = getLogger(__name__)


class Data(BaseNode):
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
        experiment: Union[BaseNode, str],
        name: str,
        type: str,
        files: list[Union[File, str]] = None,
        sample_preparation: Union[BaseNode, str, None] = None,
        computations: list[Union[BaseNode, str]] = None,
        computational_process: Union[BaseNode, str, None] = None,
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
        self.files = files if files else []
        self.type = type
        self.sample_preparation = sample_preparation
        self.computations = computations if computations else []
        self.computational_process = computational_process
        self.materials = materials if materials else []
        self.processes = processes if processes else []
        self.citations = citations if citations else []
        self.notes = notes
        self.group = auto_assign_group(group, experiment)

    @beartype
    def add_file(self, file: Union[File, dict]):
        self._add_node(file, "files")

    @beartype
    def remove_file(self, file: Union[File, int]):
        self._remove_node(file, "files")

    @beartype
    def add_computation(self, computation: Union[BaseNode, dict]):
        self._add_node(computation, "computations")

    @beartype
    def remove_computation(self, computation: Union[BaseNode, int]):
        self._remove_node(computation, "computations")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        self._remove_node(citation, "citations")
