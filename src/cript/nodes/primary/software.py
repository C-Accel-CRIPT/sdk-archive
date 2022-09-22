from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes.primary.group import Group


logger = getLogger(__name__)


class Software(BasePrimary):
    """
    Object representing a computation tool, code, programing language,
    or software package.
    """

    node_name = "Software"
    slug = "software"

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        name: str,
        version: str,
        source: Union[str, None] = None,
        notes: Union[str, None] = None,
        public: bool = False,
    ):
        super().__init__(public=public)
        self.name = name
        self.version = version
        self.source = source
        self.notes = notes
        self.group = group
