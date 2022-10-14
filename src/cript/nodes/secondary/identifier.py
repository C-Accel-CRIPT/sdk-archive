from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.secondary.base_secondary import BaseSecondary


logger = getLogger(__name__)


class Identifier(BaseSecondary):
    """
    Object representing an identifier of a `Material` object
    (e.g., CAS, BigSMILES).
    """

    node_name = "Identifier"
    list_name = "identifiers"

    @beartype
    def __init__(self, key: str, value: Union[str, int, float, list]):
        super().__init__()
        self.key = key
        self.value = value
