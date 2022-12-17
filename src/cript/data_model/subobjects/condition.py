from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.data import Data
from cript.data_model.subobjects.base_subobject import BaseSubobject

logger = getLogger(__name__)


class Condition(BaseSubobject):
    """
    Object representing a condition (e.g., temperature).
    These are used as modifiers for `Property` and `Process` objects.
    """

    node_name = "Condition"
    alt_names = ["conditions"]

    @beartype
    def __init__(
        self,
        key: str,
        value: Union[str, int, float, list, None] = None,
        unit: Union[str, None] = None,
        type: Union[str, None] = None,
        uncertainty: Union[float, int, None] = None,
        uncertainty_type: Union[str, None] = None,
        material: Union[BaseNode, str, None] = None,
        descriptor: Union[str, None] = None,
        set_id: Union[int, None] = None,
        measurement_id: Union[int, None] = None,
        data: Union[Data, str, None] = None,
    ):
        super().__init__()
        self.key = key
        self.unit = unit
        self.value = value
        self.type = type
        self.uncertainty = uncertainty
        self.uncertainty_type = uncertainty_type
        self.material = material
        self.descriptor = descriptor
        self.set_id = set_id
        self.measurement_id = measurement_id
        self.data = data
