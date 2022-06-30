from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes.primary.group import Group
from cript.nodes.primary.collection import Collection
from cript.nodes.primary.material import Material
from cript.validators import validate_required
from cript.utils import auto_assign_group


logger = getLogger(__name__)


class Inventory(BasePrimary):
    """Object representing a logical grouping of :class:`Material` objects."""

    node_name = "Inventory"
    slug = "inventory"
    required = ["group", "collection", "name"]
    unique_together = ["collection", "name"]

    @beartype
    def __init__(
        self,
        group: Union[Group, str] = None,
        collection: Union[Collection, str] = None,
        name: str = None,
        materials: list[Union[Material, str]] = None,
        description: Union[str, None] = None,
        public: bool = False,
    ):
        super().__init__()
        self.url = None
        self.uid = None
        self.group = auto_assign_group(group, collection)
        self.collection = collection
        self.name = name
        self.description = description
        self.materials = materials if materials else []
        self.public = public
        self.created_at = None
        self.updated_at = None
        validate_required(self)
        self._index_table = dict()
        self._degenerate_index_table = set()

    def __index__(self, obj: Union[int, slice, str]) -> Material:
        """
        obj can be an index or slice of self.materials or a unique identifier of a material
        """
        if isinstance(obj, (int, slice)):
            return self.materials[obj]
        elif isinstance(obj, str):
            if not self._index_table:
                self._generate_index_table()
            if obj in self._index_table:
                return self.materials[self._index_table[obj]]
            if obj in self._degenerate_index_table:
                raise ValueError("Multiple materials share this index. Try another.")

        raise TypeError("Invalid object for indexing.")

    def __len__(self) -> int:
        return len(self.materials)

    def __iter__(self) -> list[Material]:
        return self.materials

    @beartype
    def add_material(self, material: Union[Material, dict]):
        self._add_node(material, "materials")

    @beartype
    def remove_material(self, material: Union[Material, int]):
        self._remove_node(material, "materials")

    def _generate_index_table(self):
        for i, material in enumerate(self.materials):
            for identifier in material.identifiers:
                if isinstance(identifier.value, list):
                    for value in identifier.value:
                        self._add_value_index_table(value, i)
                else:
                    self._add_value_index_table(identifier.value, i)

    def _add_value_index_table(self, value: str, index: int):
        if value in self._index_table:
            if self._index_table[value] != index:
                # if value is already in index table and not from same material node,
                # remove it and add to degenerate table
                del self._index_table[value]
                self._degenerate_index_table.add(value)
            return

        self._index_table[value] = index
