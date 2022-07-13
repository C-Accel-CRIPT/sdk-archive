from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes import Group, Citation
from cript.validators import validate_required, validate_key
from cript.utils import auto_assign_group


logger = getLogger(__name__)


class Data(BasePrimary):
    """
    Object representing a set of :class:`File` objects and
    related meta-data.
    """

    node_name = "Data"
    slug = "data"
    list_name = "data"
    required = ["group", "experiment", "name", "type"]
    unique_together = ["experiment", "name"]

    @beartype
    def __init__(
        self,
        group: Union[Group, str] = None,
        experiment: Union[BasePrimary, str] = None,
        name: str = None,
        type: str = None,
        files=None,
        sample_prep: Union[str, None] = None,
        calibration: Union[str, None] = None,
        configuration: Union[str, None] = None,
        materials=None,
        processes=None,
        notes: Union[str, None] = None,
        citations: list[Union[Citation, dict]] = None,
        public: bool = False,
    ):
        super().__init__(public=public)
        self.group = auto_assign_group(group, experiment)
        self.experiment = experiment
        self.name = name
        self.files = files
        self.type = type
        self.sample_prep = sample_prep
        self.calibration = calibration
        self.configuration = configuration
        self.materials = materials if materials else []
        self.processes = processes if processes else []
        self.citations = citations if citations else []
        self.notes = notes
        validate_required(self)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = validate_key("data-type", value)

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        self._remove_node(citation, "citations")
