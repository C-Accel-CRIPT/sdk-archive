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

    ``` py title="Example"
    algorithm = Algorithm(
        key="clustering",
        type="k-means",
        parameters=[],
        citations=[],
    )
    ```

    :param key: Algorithm key
    :param type: Algorithm type
    :param parameters: List of parameters linked to this algorithm, defaults to None
    :param citations: List of citations linked to this algorithm, defaults to None
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

        :param parameter: The parameter to be added
        """
        self._add_node(parameter, "parameters")

    @beartype
    def remove_parameter(self, parameter: Union[Parameter, int]):
        """Remove a parameter from this object.

        :param parameter: The parameter to be removed
        """
        self._remove_node(parameter, "parameters")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        """Adds a citation to this object.

        :param citation: The citation to be added
        """
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        """Removes a citation from this object.

        :param citation: The citation to be removed
        """
        self._remove_node(citation, "citations")
