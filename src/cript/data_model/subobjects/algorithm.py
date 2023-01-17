from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.subobjects.base_subobject import BaseSubobject
from cript.data_model.subobjects.citation import Citation
from cript.data_model.subobjects.parameter import Parameter

logger = getLogger(__name__)


class Algorithm(BaseSubobject):
    """Object that represents an algorithm used in
    `Computation` and `ComputationalProcess` objects.

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
        """Add a parameter to this object.

        Args:
            parameter (Union[Parameter, dict]): The parameter to be added

        ``` py title="Example"
        algorithm.add_parameter(parameter)
        ```
        """
        self._add_node(parameter, "parameters")

    @beartype
    def remove_parameter(self, parameter: Union[Parameter, int]):
        """Remove a parameter from this object.

        Args:
            parameter (Union[Parameter, int]): The parameter to be removed

        ``` py title="Example"
        algorithm.remove_parameter(parameter)
        ```
        """
        self._remove_node(parameter, "parameters")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        """Add a citation to this object.

        Args:
            citation (Union[Citation, dict]): The citation to be added

        ``` py title="Example"
        algorithm.add_citation(citation)
        ```
        """
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        """Remove a citation from this object.

        Args:
            citation (Union[Citation, dict]): The citation to be removed

        ``` py title="Example"
        algorithm.remove_citation(citation)
        ```
        """
        self._remove_node(citation, "citations")
