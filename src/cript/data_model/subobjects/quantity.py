from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.subobjects.base_subobject import BaseSubobject

logger = getLogger(__name__)


class Quantity(BaseSubobject):
    """The <a href="../quantity" target="_blank">`Quantity`</a>
    object represents a specified amount of an
    <a href="../ingredient" target="_blank">`Ingredient`</a>
    object used in a <a href="/../nodes/process" target="_blank">`Process`</a>.
    For example, a catalyst in a polymerization process may be used in a
    <a href="../quantity" target="_blank">`Quantity`</a> of `100 mg`.

    Args:
        key (str): Quantity key
        value (Union[int, float]): Quantity value
        unit (Union[str, None], optional): Quantity unit
        uncertainty (Union[float, None], optional): Quantity uncertainty
        uncertainty_type (Union[str, None], optional): Quantity uncertainty type

    ``` py title="Example"
    quantity = Quantity(
        key="mass",
        value="8.3",
        unit="g",
        uncertainty=0.1,
        uncertainty_type="stdev",
    )
    ```
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
