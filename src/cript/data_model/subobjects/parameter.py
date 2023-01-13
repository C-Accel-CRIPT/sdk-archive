from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.subobjects.base_subobject import BaseSubobject

logger = getLogger(__name__)


class Parameter(BaseSubobject):
    """Object representing a an input parameter of an `Algorithm`.

    ``` py title="Example"
    parameter = Parameter(
        key="duration",
        value=10,
        unit="ns",
    )
    ```

    :param key: Parameter key
    :param value: Parameter value
    :param unit: Parameter unit
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
