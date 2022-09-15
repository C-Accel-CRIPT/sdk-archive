from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.material import Material
from cript.nodes.secondary.quantity import Quantity
from cript.nodes.secondary.base_secondary import BaseSecondary
from cript.validators import validate_key


logger = getLogger(__name__)


class Ingredient(BaseSecondary):
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
        keyword: str = None,
        quantities: list[Union[Quantity, dict]] = None,
    ):
        super().__init__()
        self.material = material
        self.keyword = keyword
        self.quantities = quantities if quantities else []

    @property
    def keyword(self):
        return self._keyword

    @keyword.setter
    def keyword(self, value):
        self._keyword = validate_key("ingredient-keyword", value)

    @beartype
    def add_quantity(self, quantity: Union[Quantity, dict]):
        self._add_node(quantity, "quantities")

    @beartype
    def remove_quantity(self, quantity: Union[Quantity, int]):
        self._remove_node(quantity, "quantities")
