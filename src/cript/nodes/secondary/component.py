from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes import Base
from cript.validators import validate_required


logger = getLogger(__name__)


class Component(Base):
    """Object representing a mixture component of a :class:`Material` object."""

    node_type = "secondary"
    node_name = "Component"
    list_name = "components"
    required = ["material"]

    @beartype
    def __init__(self, component_id: int = 1, material: Union[Base, str] = None):
        super().__init__()
        self.component_id = component_id
        self.material = material
        validate_required(self)
