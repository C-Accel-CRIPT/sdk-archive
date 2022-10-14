from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.secondary.base_secondary import BaseSecondary


logger = getLogger(__name__)


class Quantity(BaseSecondary):
    """
    Object representing a specified amount of an `Ingredient`
    object used as input to a `Process` object.
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
