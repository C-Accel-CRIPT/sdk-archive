from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes import Base
from cript.validators import (
    validate_required,
    validate_key,
    validate_value,
    validate_unit,
)


logger = getLogger(__name__)


class Quantity(Base):
    """
    Object representing a specified amount of an :class:`Ingredient`
    object used as input to a :class:`Process` object.
    """

    node_type = "secondary"
    node_name = "Quantity"
    list_name = "quantities"
    required = ["key", "value"]

    @beartype
    def __init__(
        self,
        key: str = None,
        value: Union[int, float] = None,
        unit: Union[str, None] = None,
    ):
        super().__init__()
        self.key = key
        self.unit = unit
        self.value = value
        validate_required(self)

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = validate_key("quantity-key", value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = validate_value("quantity-key", self.key, value, self.unit)

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        self._unit = validate_unit("quantity-key", self.key, value)
