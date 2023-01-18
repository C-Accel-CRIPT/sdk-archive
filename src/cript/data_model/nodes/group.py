from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.user import User

logger = getLogger(__name__)


class Group(BaseNode):
    """The <a href="../group" target="_blank">`Group`</a> object
    represents a group of users who have permission to edit a set of
    CRIPT objects. For example, all members of an academic group who participate in a
    specific research project may constitute a
    <a href="../group" target="_blank">`Group`</a> object that manages the
    <a href="../project" target="_blank">`Project`</a> object.

    Args:
        name (str): Group name
        users (list[Union[User, str]], optional): List of users who are members of the group
        public (bool, optional): Whether the group is publicly viewable
    
    !!! warning "Group names must be unique"
        Each <a href="../group" target="_blank">`Group`</a> name must be unique across all of CRIPT.

    !!! success "Use <a href='../base_node' target='_blank'>`BaseNode`</a> methods to manipulate this object"
        Since this object inherits from the <a href="../base_node" target="_blank">`BaseNode`</a> object,
        all the <a href="../base_node" target="_blank">`BaseNode`</a> object methods can be used to manipulate it.
        These include `get()`, `create()`, `delete()`, `save()`, `search()`, `update()`, and `refresh()` methods.
        See the <a href="../base_node" target="_blank">`BaseNode`</a> documentation to learn more about these methods
        and see examples of their use.

    ``` py title="Example"
    # create a new group
    my_group = Group.create(
        name="My group",
    )
    ```

    ``` json title="Example of a group in JSON format"
    {
        "url": "https://criptapp.org/api/group/b782ab55-22de-4409-b81b-1bf6367b4123/",
        "uid": "b782ab55-22de-4409-b81b-1bf6367b4123",
        "name": "Polymer physics lab group",
        "users": [
            "https://criptapp.org/api/user/d0a212b0-5aa7-47d3-a6fc-d161acf90726/",
            "https://criptapp.org/api/user/77fb119a-0768-4ad2-9055-d817480c0180/",
            "https://criptapp.org/api/user/8de042c7-ba6e-4e4e-9f6e-0fdeb73e4595/"
        ],
        "public": false,
        "created_at": "2022-07-21T20:41:18.889002Z",
        "updated_at": "2022-07-21T20:49:38.525372Z"
    }
    ```
    """

    node_name = "Group"
    slug = "group"

    @beartype
    def __init__(
        self,
        name: str,
        users: list[Union[User, str]] = None,
        public: bool = False,
        **kwargs,
    ):
        super().__init__(public=public, **kwargs)
        self.name = name
        self.users = users if users else []

    @beartype
    def add_user(self, user: Union[User, dict]):
        """Add a <a href="../user" target="_blank">`User`</a> to the group.

        Args:
            user (Union[User, dict]): `User` object to add
        
        ``` py title="Example"
        eric = User.get(name="Eric M")

        my_group.add_user(eric)
        ```
        """
        self._add_node(user, "users")

    @beartype
    def remove_user(self, user: Union[User, int]):
        """Remove a <a href="../user" target="_blank">`User`</a> from the group.

        Args:
            user (Union[User, dict]): `User` object to remove
        
        ``` py title="Example"
        eric = User.get(name="Eric M")

        my_group.remove_user(eric)
        ```
        """
        self._remove_node(user, "users")
