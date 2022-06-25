from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes import Base, Group, Collection, Material
from cript.validators import validate_required
from cript.utils import auto_assign_group


logger = getLogger(__name__)


class Inventory(Base):
    """Object representing a logical grouping of :class:`Material` objects."""

    node_type = "primary"
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

    @beartype
    def add_material(self, material: Union[Material, dict]):
        self._add_node(material, "materials")

    @beartype
    def remove_material(self, material: Union[Material, int]):
        self._remove_node(material, "materials")
