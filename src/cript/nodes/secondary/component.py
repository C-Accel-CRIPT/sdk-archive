from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes.secondary.base_secondary import BaseSecondary
from cript.validators import validate_required


logger = getLogger(__name__)


class Component(BaseSecondary):
    """Object representing a mixture component of a :class:`Material` object."""

    node_name = "Component"
    list_name = "components"
    required = ["material"]

    @beartype
    def __init__(self, component_id: int = 1, material: Union[BasePrimary, str] = None):
        super().__init__()
        self.component_id = component_id
        self.material = material
        validate_required(self)
