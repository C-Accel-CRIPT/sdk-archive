from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.material import Material
from cript.data_model.subobjects.base_subobject import BaseSubobject
from cript.data_model.subobjects.quantity import Quantity

logger = getLogger(__name__)


class Ingredient(BaseSubobject):
    """An <a href="../ingredient" target="_blank">`Ingredient`</a> object
    represents a quantity of material which is used as an input to a
    <a href="/../nodes/process" target="_blank">`Process`</a>. For example,
    the catalyst material in a polymerization process is an
    <a href="../ingredient" target="_blank">`Ingredient`</a>.

    Args:
        material (Union[Material, str]): `Material` which is used as an ingredient in the `Process` object
        keyword (str): Ingredient keyword
        quantities (list[Union[Quantity, dict]], optional): Quantities of the ingredient used in the process

    ``` py title="Example"
    material = Material(
        project="My project",
        name="Polystyrene",
    )

    quantity = Quantity(
        key="mass",
        value="8.3",
        unit="g",
    )

    ingredient = Ingredient(
        material=material,
        keyword="catalyst",
        quantities=[quantity],
    )
    ```
    """

    node_name = "Ingredient"
    alt_names = ["ingredients"]

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
        """Add a <a href="../quantity" target="_blank">`Quantity`</a> to the ingredient.

        Args:
            quantity (Union[Quantity, dict]): Quantity to add

        ``` py title="Example"
        quantity = Quantity(
            key="mass",
            value="8.3",
            unit="g",
        )

        ingredient.add(quantity)
        ```
        """
        self._add_node(quantity, "quantities")

    @beartype
    def remove_quantity(self, quantity: Union[Quantity, int]):
        """Remove a <a href="../quantity" target="_blank">`Quantity`</a> from the ingredient.

        Args:
            quantity (Union[Quantity, int]): Quantity to remove

        ``` py title="Example"
        quantity = Quantity(
            key="mass",
            value="8.3",
            unit="g",
        )

        ingredient.remove(quantity)
        ```
        """
        self._remove_node(quantity, "quantities")
