from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.secondary.base_secondary import BaseSecondary
from cript.validators import validate_key
from cript.validators import validate_value
from cript.validators import validate_unit


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

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = validate_key("parameter-key", value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = validate_value("parameter-key", self.key, value, self.unit)

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        self._unit = validate_unit("parameter-key", self.key, value)
