from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.secondary.base_secondary import BaseSecondary


logger = getLogger(__name__)


class Parameter(BaseSecondary):
    """Object representing a an input value to an :class:`Algorithm`."""

    node_name = "Parameter"
    list_name = "parameters"

    @beartype
    def __init__(
        self,
        key: str,
        value: Union[int, float],
        unit: Union[str, None] = None,
    ):
        super().__init__()
        self.key = key
        self.unit = unit
        self.value = value
