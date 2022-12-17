from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.file import File
from cript.data_model.subobjects.base_subobject import BaseSubobject
from cript.data_model.subobjects.citation import Citation
from cript.data_model.subobjects.condition import Condition

logger = getLogger(__name__)


class Equipment(BaseSubobject):
    """
    Object representing equipment used in a `Process`.
    """

    node_name = "Equipment"
    alt_names = ["equipment"]

    @beartype
    def __init__(
        self,
        key: str,
        description: Union[str, None] = None,
        conditions: list[Union[Condition, dict]] = None,
        files: list[Union[File, dict]] = None,
        citations: list[Union[Citation, dict]] = None,
    ):
        super().__init__()
        self.key = key
        self.description = description
        self.conditions = conditions if conditions else []
        self.files = files if files else []
        self.citations = citations if citations else []
