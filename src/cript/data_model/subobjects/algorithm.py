from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.subobjects.base_subobject import BaseSubobject
from cript.data_model.subobjects.citation import Citation
from cript.data_model.subobjects.parameter import Parameter
from cript.data_model.nodes.computation import Computation

logger = getLogger(__name__)


class Algorithm(BaseSubobject):
    """The <a href="../algorithm" target="_blank">`Algorithm`</a>
    object represents an algorithm that can be used as part of a
    <a href="/../nodes/computation" target="_blank">`Computation`</a> object. For example,
    the computation might consist of a clustering algorithm or sorting a algorithm.

    Args:
        key (str): Algorithm key
        type (str): Algorithm type
        parameters (list[Union[Parameter, dict]], optional): List of parameters linked to this algorithm
        citations (list[Union[Citation, dict]], optional): List of citations linked to this algorithm

    ``` py title="Example"
    algorithm = Algorithm(
        key="clustering",
        type="k-means",
        parameters=[],
        citations=[],
    )
    ```
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
        """Add a <a href="../parameter" target="_blank">`Parameter`</a> to the algorithm.

        Args:
            parameter (Union[Parameter, dict]): The parameter to be added

        ``` py title="Example"
        algorithm.add_parameter(parameter)
        ```
        """
        self._add_node(parameter, "parameters")

    @beartype
    def remove_parameter(self, parameter: Union[Parameter, int]):
        """Remove a <a href="../parameter" target="_blank">`Parameter`</a> from the algorithm.

        Args:
            parameter (Union[Parameter, int]): The parameter to be removed

        ``` py title="Example"
        algorithm.remove_parameter(parameter)
        ```
        """
        self._remove_node(parameter, "parameters")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        """Add a <a href="../citation" target="_blank">`Citation`</a> to the algorithm.

        Args:
            citation (Union[Citation, dict]): The citation to be added

        ``` py title="Example"
        algorithm.add_citation(citation)
        ```
        """
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        """Remove a <a href="../citation" target="_blank">`Citation`</a> from the algorithm.

        Args:
            citation (Union[Citation, int]): The citation to be removed

        ``` py title="Example"
        algorithm.remove_citation(citation)
        ```
        """
        self._remove_node(citation, "citations")
