from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.subobjects.base_subobject import BaseSubobject

logger = getLogger(__name__)


class Identifier(BaseSubobject):
    """
    Object representing an identifier of a `Material` object
    (e.g., CAS, BigSMILES).
    """

    node_name = "Identifier"
    alt_names = ["identifiers"]

    @beartype
    def __init__(self, key: str, value: Union[str, int, float, list]):
        super().__init__()
        self.key = key
        self.value = value
