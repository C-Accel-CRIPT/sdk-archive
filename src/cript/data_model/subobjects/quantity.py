from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.subobjects.base_subobject import BaseSubobject

logger = getLogger(__name__)


class Quantity(BaseSubobject):
    """
    Object representing a specified amount of an `Ingredient`
    object used as input to a `Process` object.
    """

    node_name = "Quantity"
    alt_names = ["quantities"]

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
