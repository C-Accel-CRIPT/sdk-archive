from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.secondary.base_secondary import BaseSecondary
from cript.nodes.primary.data import Data
from cript.validators import (
    validate_required,
    validate_key,
    validate_value,
    validate_unit,
)


logger = getLogger(__name__)


class Condition(BaseSecondary):
    """
    Object representing a condition (e.g., temperature).
    These are used as modifiers for :class:`Property` and :class:`Process` objects.
    """

    node_name = "Condition"
    list_name = "conditions"
    required = ["key"]

    @beartype
    def __init__(
        self,
        key: str = None,
        value: Union[str, int, float, list, None] = None,
        unit: Union[str, None] = None,
        type: Union[str, None] = None,
        uncertainty: Union[float, int, None] = None,
        uncertainty_type: Union[str, None] = None,
        set_id: Union[int, None] = None,
        measurement_id: Union[int, None] = None,
        data: list[Union[Data, str]] = None,
    ):
        super().__init__()
        self.key = key
        self.unit = unit
        self.value = value
        self.type = type
        self.uncertainty = uncertainty
        self.uncertainty_type = uncertainty_type
        self.set_id = set_id
        self.measurement_id = measurement_id
        self.data = data if data else []
        validate_required(self)

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = validate_key("condition-key", value)

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        self._unit = validate_unit("condition-key", self.key, value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = validate_value("condition-key", self.key, value, self.unit)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = validate_key("set-type", value)

    @property
    def uncertainty_type(self):
        return self._uncertainty_type

    @uncertainty_type.setter
    def uncertainty_type(self, value):
        self._uncertainty_type = validate_key("uncertainty-type", value)

    @beartype
    def add_data(self, data: Union[Data, dict]):
        self._add_node(data, "data")

    @beartype
    def remove_data(self, data: Union[Data, int]):
        self._remove_node(data, "data")
