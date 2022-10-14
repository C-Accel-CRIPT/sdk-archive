from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.file import File
from cript.nodes.secondary.base_secondary import BaseSecondary
from cript.nodes.secondary.condition import Condition
from cript.nodes.secondary.citation import Citation


logger = getLogger(__name__)


class Equipment(BaseSecondary):
    """
    Object representing equipment used in a `Process`.
    """

    node_name = "Equipment"
    list_name = "equipment"

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
