from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.collection import Collection
from cript.data_model.nodes.group import Group
from cript.data_model.nodes.material import Material
from cript.data_model.utils import auto_assign_group

logger = getLogger(__name__)


class Inventory(BaseNode):
    """The <a href="../inventory" target="_blank">`Inventory`</a> object
    represents a logical grouping of
    <a href="../material" target="_blank">`Material`</a> objects.

    For example, the set of chemicals
    available in a specific laboratory, or set of polymers studied in a published article,
    may make up an inventory. Each <a href="../inventory" target="_blank">`Inventory`</a> is nested inside of a
    <a href="../collection" target="_blank">`Collection`</a> object.

    Args:
        collection (Union[Collection, str]): The parent `Collection` of the inventory
        name (str): Inventory name
        materials (list[Union[Material, str]], optional): List of `Material` objects inside the inventory
        notes (Union[str, None], optional): Inventory notes
        public (bool, optional): Whether the inventory is publicly viewable
        group (Union[Group, str], optional): `Group` object that manages the inventory

    !!! warning "Inventory names must be unique"
        Each <a href="../inventory" target="_blank">`Inventory`</a> name must be unique within a
        <a href="../collection" target="_blank">`Collection`</a> node.

    !!! success "Use <a href='../base_node' target='_blank'>`BaseNode`</a> methods to manipulate this object"
        Since this object inherits from the <a href="../base_node" target="_blank">`BaseNode`</a> object,
        all the <a href="../base_node" target="_blank">`BaseNode`</a> object methods can be used to manipulate it.
        These include `get()`, `create()`, `delete()`, `save()`, `search()`, `update()`, and `refresh()` methods.
        See the <a href="../base_node" target="_blank">`BaseNode`</a> documentation to learn more about these methods
        and see examples of their use.

    ``` py title="Example"
    # get an existing collection
    my_collection = Collection.get(name="My collection")

    # create a new inventory in the existing collection
    my_inv = Inventory.create(
        collection=my_collection,
        name="My inventory name",
    )

    # get another inventory
    my_other_inv = Inventory.get(
        name="My other inv name",
        collection=my_collection,
    )
    ```

    !!! question "Why is `Collection` needed when getting an inventory?"
        <a href="../inventory" target="_blank">`Inventory`</a> names are only unique within a collection, not across all collections,
        so when getting a `Inventory` via name,
        the associated <a href="../collection" target="_blank">`Collection`</a> node must also be specified.


    ``` json title="Example of an inventory in JSON format"
    {
        "url": "https://criptapp.org/api/inventory/c826d9aa-2950-448a-8ab7-ae0ca2657763/",
        "uid": "c826d9aa-2950-448a-8ab7-ae0ca2657763",
        "group": "https://criptapp.org/api/group/2a3d39f1-e740-4b99-8854-2aa216cd3858/",
        "name": "TestChiMD_inv",
        "materials": [
            "https://criptapp.org/api/material/7ee5a540-c9ef-467a-bae6-3c1d705e010f/",
            "https://criptapp.org/api/material/a48a00dc-c64f-4c2a-ad2b-6f3f6f9b4d46/",
            "https://criptapp.org/api/material/0b224d37-8505-41ef-8bca-3d59a13235fb/",
            "https://criptapp.org/api/material/8b5d2756-9e73-4540-8ca7-18509c4cf7b5/",
            "https://criptapp.org/api/material/6e2756ab-d042-4fe8-a0ce-a3eb603f540b/",
            "https://criptapp.org/api/material/2e468b97-eac5-4645-adfb-2020d45847aa/",
            "https://criptapp.org/api/material/7829719a-eb4b-4525-b427-a1432d2dfed3/"
        ],
        "collection": "https://criptapp.org/api/collection/44bbba40-0ebc-41db-bcc9-b78eabbf974e/",
        "notes": "Created for Lab 210B",
        "public": true,
        "created_at": "2022-08-19T14:06:07.129361Z",
        "updated_at": "2022-08-19T15:00:21.337246Z"
    }
    ```
    """

    node_name = "Inventory"
    slug = "inventory"

    @beartype
    def __init__(
        self,
        collection: Union[Collection, str],
        name: str,
        materials: list[Union[Material, str]] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        group: Union[Group, str] = None,
        **kwargs,
    ):
        super().__init__(public=public, **kwargs)
        self.collection = collection
        self.name = name
        self.notes = notes
        self.materials = materials if materials else []
        self.group = auto_assign_group(group, collection)

        self.__index_table = dict()
        self.__degenerate_index_table = set()

    def __getitem__(self, obj: Union[int, slice, str]) -> Material:
        # obj can be an index or slice of self.materials or a unique identifier of a material
        if isinstance(obj, (int, slice)):
            return self.materials[obj]
        elif isinstance(obj, str):
            if not self.__index_table:
                self._generate_index_table()
            if obj in self.__index_table:
                return self.materials[self.__index_table[obj]]
            if obj in self.__degenerate_index_table:
                raise ValueError("Multiple materials share this index. Try another.")
            raise ValueError(
                f"'{obj}' not found in Inventory: {self.name}."
                " (exact match required, case sensitive)"
            )

        raise TypeError("Invalid object for indexing.")

    def __len__(self) -> int:
        return len(self.materials)

    def __iter__(self) -> list[Material]:
        return self.materials

    @beartype
    def add_material(self, material: Union[Material, dict]):
        """Add a <a href="../material" target="_blank">`Material`</a> object to the inventory.

        Args:
            material (Union[Material, dict]): `Material` object to add

        ``` py title="Example"
        inventory.add_material(material)
        ```
        """
        self._add_node(material, "materials")

    @beartype
    def remove_material(self, material: Union[Material, int]):
        """Remove a <a href="../material" target="_blank">`Material`</a> object from the inventory.

        Args:
            material (Union[Material, int]): `Material` object to remove

        ``` py title="Example"
        inventory.remove_material(material)
        ```
        """
        self._remove_node(material, "materials")

    def _generate_index_table(self):
        for i, material in enumerate(self.materials):
            self._add_value_index_table(material.name, i)
            self._add_value_index_table(material.uid, i)
            for identifier in material.identifiers:
                if isinstance(identifier.value, list):
                    for value in identifier.value:
                        self._add_value_index_table(value, i)
                else:
                    self._add_value_index_table(identifier.value, i)

    def _add_value_index_table(self, value: str, index: int):
        if value in self.__index_table:
            if self.__index_table[value] != index:
                # if value is already in index table and not from same material node,
                # remove it and add to degenerate table
                del self.__index_table[value]
                self.__degenerate_index_table.add(value)
            return

        self.__index_table[value] = index
