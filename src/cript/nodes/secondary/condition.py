from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes.secondary.base_secondary import BaseSecondary
from cript.nodes.primary.data import Data


logger = getLogger(__name__)


class Condition(BaseSecondary):
    """
    Object representing a condition (e.g., temperature).
    These are used as modifiers for `Property` and `Process` objects.
    """

    node_name = "Condition"
    list_name = "conditions"

    @beartype
    def __init__(
        self,
        key: str,
        value: Union[str, int, float, list, None] = None,
        unit: Union[str, None] = None,
        type: Union[str, None] = None,
        uncertainty: Union[float, int, None] = None,
        uncertainty_type: Union[str, None] = None,
        material: Union[BasePrimary, str, None] = None,
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
