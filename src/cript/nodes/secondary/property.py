from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes import Base, Data, Condition, Citation
from cript.validators import (
    validate_required,
    validate_key,
    validate_value,
    validate_unit,
)


logger = getLogger(__name__)


class Property(Base):
    """
    Object representing an observed or measured attribute
    of a :class:`Material` or :class:`Process` object.
    """

    node_type = "secondary"
    node_name = "Property"
    list_name = "properties"
    required = ["key", "value"]

    @beartype
    def __init__(
        self,
        key: str = None,
        value: Union[str, int, float, list, None] = None,
        unit: Union[str, None] = None,
        type: Union[str, None] = None,
        method: Union[str, None] = None,
        method_description: Union[str, None] = None,
        uncertainty: Union[float, None] = None,
        uncertainty_type: Union[str, None] = None,
        component_id: Union[int, None] = None,
        structure: Union[str, None] = None,
        set_id: Union[int, None] = None,
        conditions: list[Union[Condition, dict]] = None,
        data: list[Union[Data, str]] = None,
        citations: list[Union[Citation, dict]] = None,
    ):
        super().__init__()
        self.key = key
        self.unit = unit
        self.value = value
        self.type = type
        self.method = method
        self.method_description = method_description
        self.uncertainty = uncertainty
        self.uncertainty_type = uncertainty_type
        self.component_id = component_id
        self.structure = structure
        self.set_id = set_id
        self.conditions = conditions if conditions else []
        self.data = data if data else []
        self.citations = citations if citations else []
        validate_required(self)

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = validate_key("property-key", value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = validate_value("property-key", self.key, value, self.unit)

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        self._unit = validate_unit("property-key", self.key, value)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = validate_key("set-type", value)

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        self._method = validate_key("property-method", value)

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

    @beartype
    def add_condition(self, condition: Union[Condition, dict]):
        self._add_node(condition, "conditions")

    @beartype
    def remove_condition(self, condition: Union[Condition, int]):
        self._remove_node(condition, "conditions")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        self._remove_node(citation, "citations")
