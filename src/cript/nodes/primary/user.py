from logging import getLogger

from beartype import beartype

from cript.nodes.primary.base_primary import BasePrimary


logger = getLogger(__name__)


class User(BasePrimary):
    """
    Object representing a CRIPT user.

    Note: A user cannot be created or modified using the SDK.
          This object is for read-only purposes only.
    """

    node_name = "User"
    slug = "user"
    list_name = "users"

    @beartype
    def __init__(
        self,
        username: str = None,
        email: str = None,
        orcid_id: str = None,
        groups=None,
        public: bool = False,
    ):
        super().__init__(public=public)
        self.username = username
        self.email = email
        self.orcid_id = orcid_id
        self.groups = groups if groups else []
