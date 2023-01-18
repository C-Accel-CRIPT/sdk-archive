from logging import getLogger

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode

logger = getLogger(__name__)


class User(BaseNode):
    """The <a href="../user" target="_blank">`User`</a> object represents a single CRIPT user.

    !!! warning "Modifying CRIPT users"
        CRIPT `User` objects cannot be created or modified using the Python SDK.
        The `User` object documented here is for informational purposes only.

    Args:
        username (str, optional): Username displayed on the CRIPT interface
        email (str, optional): Email of the user
        orcid_id (str, optional): ORCID ID of the user
        groups (_type_, optional): `Group` objects that the user is a member of
        public (bool, optional): Whether the user is publicly viewable
     
    ``` json title="Example of a user in JSON format"
    {
        "url": "https://criptapp.org/api/user/8de042c7-ba6e-4e4e-9f6e-0fdeb73e4595/",
        "uid": "8de042c7-ba6e-4e4e-9f6e-0fdeb73e4595",
        "username": "esm",
        "email": "esm@email.com",
        "orcid_id": "0000-0001-7114-5424",
        "public": true,
        "created_at": "2022-04-18T17:35:30.019800Z",
        "updated_at": "2023-01-17T18:34:42.186527Z"
    },
    ```
    """

    node_name = "User"
    slug = "user"
    alt_names = ["users"]

    @beartype
    def __init__(
        self,
        username: str = None,
        email: str = None,
        orcid_id: str = None,
        groups=None,
        public: bool = False,
        **kwargs
    ):
        super().__init__(public=public, **kwargs)
        self.username = username
        self.email = email
        self.orcid_id = orcid_id
        self.groups = groups if groups else []
