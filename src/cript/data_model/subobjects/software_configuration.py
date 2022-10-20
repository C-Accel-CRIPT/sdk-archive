from typing import Union
from logging import getLogger

from beartype import beartype

from cript.data_model.nodes.software import Software
from cript.data_model.subobjects.base_subobject import BaseSubobject
from cript.data_model.subobjects.algorithm import Algorithm
from cript.data_model.subobjects.citation import Citation


logger = getLogger(__name__)


class SoftwareConfiguration(BaseSubobject):
    """
    Object representing the `Software` and set of `Algorithm` objects
    used to execute a `Computation` or `ComputationalProcess`.
    """

    node_name = "SoftwareConfiguration"
    alt_names = ["software_configurations"]

    @beartype
    def __init__(
        self,
        software: Union[Software, str],
        algorithms: list[Union[Algorithm, dict]] = None,
        notes: Union[str, None] = None,
        citations: list[Union[Citation, dict]] = None,
    ):
        super().__init__()
        self.software = software
        self.algorithms = algorithms if algorithms else []
        self.notes = notes
        self.citations = citations if citations else []

    @beartype
    def add_algorithm(self, algorithm: Union[Algorithm, dict]):
        self._add_node(algorithm, "algorithms")

    @beartype
    def remove_algorithm(self, algorithm: Union[Algorithm, int]):
        self._remove_node(algorithm, "algorithms")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        self._remove_node(citation, "citations")
