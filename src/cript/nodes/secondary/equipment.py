from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.secondary.base_secondary import BaseSecondary
from cript.nodes.secondary.condition import Condition
from cript.nodes.secondary.citation import Citation
from cript.validators import validate_required, validate_key


logger = getLogger(__name__)


class Equipment(BaseSecondary):
    """
    Object representing equipment used in a :class:`Process`.
    """

    node_name = "Equipment"
    list_name = "equipment"
    required = ["key"]

    @beartype
    def __init__(
        self,
        key: str,
        description: Union[str, None] = None,
        conditions: list[Union[Condition, dict]] = None,
        citations: list[Union[Citation, dict]] = None,
    ):
        super().__init__()
        self.key = key
        self.description = description
        self.conditions = conditions if conditions else []
        self.citations = citations if citations else []
        validate_required(self)

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = validate_key("equipment-key", value)
