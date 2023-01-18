from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.subobjects.base_subobject import BaseSubobject

logger = getLogger(__name__)


class Parameter(BaseSubobject):
    """The <a href="../parameter" target="_blank">`Parameter`</a> object 
    represents an input parameter to an <a href="../algorithm" target="_blank">`Algorithm`</a>.
    For example, the `k` variable in a `k-means` clustering algorithm is a parameter.

    Args:
        key (str): Parameter key
        value (Union[int, float]): Parameter value
        unit (Union[str, None], optional): Parameter unit

    ``` py title="Example"
    parameter = Parameter(
        key="duration",
        value=10,
        unit="ns",
    )
    ```
    """

    node_name = "Parameter"
    alt_names = ["parameters"]

    @beartype
    def __init__(
        self,
        key: str,
        value: Union[int, float],
        unit: Union[str, None] = None,
    ):
        super().__init__()
        self.key = key
        self.unit = unit
        self.value = value
