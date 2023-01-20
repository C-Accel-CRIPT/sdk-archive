from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.data import Data
from cript.data_model.subobjects.base_subobject import BaseSubobject

logger = getLogger(__name__)


class Condition(BaseSubobject):
    """
    The <a href="../condition" target="_blank">`Condition`</a>
    object represents a physical or virtual condition (e.g. temperature, pressure,
    or humidity). A <a href="../condition" target="_blank">`Condition`</a> object
    may be used as a modifier for
    <a href="../property" target="_blank">`Property`</a> or
    <a href="/../nodes/process" target="_blank">`Process`</a> objects.

    Args:
        key (str): Condition key
        value (Union[str, int, float, list, None], optional): Condition value
        unit (Union[str, None], optional): Condition unit
        type (Union[str, None], optional): Condition type
        uncertainty (Union[float, int, None], optional): Condition uncertainty
        uncertainty_type (Union[str, None], optional): Condition uncertainty type
        material (Union[BaseNode, str, None], optional): Material associated with this condition
        descriptor (Union[str, None], optional): Condition descriptor
        set_id (Union[int, None], optional): Condition set ID
        measurement_id (Union[int, None], optional): Condition measurement ID
        data (Union[Data, str, None], optional): `Data` object associated with this condition

    ``` py title="Example"
    condition = Condition(
        key="flow_rate",
        value=8.13,
        unit="mL/min",
        uncertainty=0.3,
        uncertainty_type="stdev",
        descriptor="measured on flow controller 2B"
    )
    ```
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
