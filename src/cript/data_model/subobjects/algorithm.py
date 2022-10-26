from typing import Union
from logging import getLogger

from beartype import beartype

from cript.data_model.subobjects.base_subobject import BaseSubobject
from cript.data_model.subobjects.parameter import Parameter
from cript.data_model.subobjects.citation import Citation


logger = getLogger(__name__)


class Algorithm(BaseSubobject):
    """
    Object that represents an algorithm used in :class:`Computation` and
    `ComputationalProcess` objects.
    """

    node_name = "Algorithm"
    alt_names = ["algorithms"]

    @beartype
    def __init__(
        self,
        key: str,
        type: str,
        parameters: list[Union[Parameter, dict]] = None,
        citations: list[Union[Citation, dict]] = None,
    ):
        super().__init__()
        self.key = key
        self.type = type
        self.parameters = parameters if parameters else []
        self.citations = citations if citations else []

    @beartype
    def add_parameter(self, parameter: Union[Parameter, dict]):
        self._add_node(parameter, "parameters")

    @beartype
    def remove_parameter(self, parameter: Union[Parameter, int]):
        self._remove_node(parameter, "parameters")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        self._remove_node(citation, "citations")
