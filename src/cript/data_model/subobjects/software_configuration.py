from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.software import Software
from cript.data_model.subobjects.algorithm import Algorithm
from cript.data_model.subobjects.base_subobject import BaseSubobject
from cript.data_model.subobjects.citation import Citation

logger = getLogger(__name__)


class SoftwareConfiguration(BaseSubobject):
    """The <a href="../software_configuration" target="_blank">`SoftwareConfiguration`</a>
    object represents the
    <a href="/../nodes/software" target="_blank">`Software`</a> and set of
    <a href="../algorithm" target="_blank">`Algorithm`</a> objects
    used to execute a <a href="/../nodes/computation" target="_blank">`Computation`</a> or a
    <a href="/../nodes/computational_process" target="_blank">`ComputationalProcess`</a>.

    Args:
        software (Union[Software, str]): Software name
        algorithms (list[Union[Algorithm, dict]], optional): List of `Algorithm` objects associated with the software configuration
        notes (Union[str, None], optional): Software configuration notes
        citations (list[Union[Citation, dict]], optional): List of `Citation` objects associated with the software configuration

    ``` py title="Example"
    sc = SoftwareConfiguration(
        software="LabVIEW",
        notes="Version 2020 in lab 24B"
    )
    ```
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
        """Add an <a href="../algorithm" target="_blank">`Algorithm`</a> to the software configuration.

        Args:
            algorithm (Union[Algorithm, dict]): Algorithm to add

        ``` py title="Example"
        sc.add_algorithm(algorithm)
        ```
        """
        self._add_node(algorithm, "algorithms")

    @beartype
    def remove_algorithm(self, algorithm: Union[Algorithm, int]):
        """Remove an <a href="../algorithm" target="_blank">`Algorithm`</a> from the software configuration.

        Args:
            algorithm (Union[Algorithm, int]): Algorithm to remove

        ``` py title="Example"
        sc.remove_algorithm(algorithm)
        ```
        """
        self._remove_node(algorithm, "algorithms")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        """Add a <a href="../citation" target="_blank">`Citation`</a> to the software configiuration.

        Args:
            citation (Union[Citation, dict]): Citation to add

        ``` py title="Example"
        sc.add_citation(citation)
        ```
        """
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        """Remove a <a href="../citation" target="_blank">`Citation`</a> from this software configuration.

        Args:
            citation (Union[Citation, int]): Citation to remove

        ``` py title="Example"
        sc.remove_citation(citation)
        ```
        """
        self._remove_node(citation, "citations")
