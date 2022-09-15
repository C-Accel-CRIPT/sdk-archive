from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.secondary.base_secondary import BaseSecondary
from cript.validators import validate_key, validate_value


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

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = validate_key("material-identifier-key", value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = validate_value("material-identifier-key", self.key, value)
