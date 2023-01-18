from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.subobjects.base_subobject import BaseSubobject

logger = getLogger(__name__)


class Identifier(BaseSubobject):
    """The <a href="../identifier" target="_blank">`Identifier`</a> object
    is used for identifying a <a href="/../nodes/material" target="_blank">`Material`</a> object.
    For example, an <a href="../identifier" target="_blank">`Identifier`</a> can be
    a SMILES string, BigSMILES string, or material name.

    Args:
        key (str): Identifier key
        value (Union[str, int, float, list]): Identifier value

    ``` py title="Example"
    identifier = Identifier(
        key="smiles",
        value="CCC",
    )
    ```
    """

    node_name = "Identifier"
    alt_names = ["identifiers"]

    @beartype
    def __init__(self, key: str, value: Union[str, int, float, list]):
        super().__init__()
        self.key = key
        self.value = value
