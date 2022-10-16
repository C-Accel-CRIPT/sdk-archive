from typing import Union
from logging import getLogger

from beartype import beartype

from cript.data_model.nodes.material import Material
from cript.data_model.subobjects.quantity import Quantity
from cript.data_model.subobjects.base_subobject import BaseSubobject


logger = getLogger(__name__)


class Ingredient(BaseSubobject):
    """
    Object representing a `Material` object being used
    as an input to a `Process` object.
    """

    node_name = "Ingredient"
    list_name = "ingredients"

    @beartype
    def __init__(
        self,
        material: Union[Material, str],
        keyword: str,
        quantities: list[Union[Quantity, dict]] = None,
    ):
        super().__init__()
        self.material = material
        self.keyword = keyword
        self.quantities = quantities if quantities else []

    @beartype
    def add_quantity(self, quantity: Union[Quantity, dict]):
        self._add_node(quantity, "quantities")

    @beartype
    def remove_quantity(self, quantity: Union[Quantity, int]):
        self._remove_node(quantity, "quantities")
