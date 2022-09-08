from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.secondary.base_secondary import BaseSecondary
from cript.validators import validate_key, validate_value, validate_unit


logger = getLogger(__name__)


class Quantity(BaseSecondary):
    """
    Object representing a specified amount of an :class:`Ingredient`
    object used as input to a :class:`Process` object.
    """

    node_name = "Quantity"
    list_name = "quantities"

    @beartype
    def __init__(
        self,
        key: str,
        value: Union[int, float],
        unit: Union[str, None] = None,
        uncertainty: Union[float, None] = None,
        uncertainty_type: Union[str, None] = None,
    ):
        super().__init__()
        self.key = key
        self.unit = unit
        self.value = value
        self.uncertainty = uncertainty
        self.uncertainty_type = uncertainty_type

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

    @property
    def uncertainty_type(self):
        return self._uncertainty_type

    @uncertainty_type.setter
    def uncertainty_type(self, value):
        self._uncertainty_type = validate_key("uncertainty-type", value)
