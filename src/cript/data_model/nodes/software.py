from typing import Union
from logging import getLogger

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.group import Group


logger = getLogger(__name__)


class Software(BaseNode):
    """
    Object representing a computation tool, code, programing language,
    or software package.
    """

    node_name = "Software"
    slug = "software"
    alt_names = ["software"]

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        name: str,
        version: str,
        source: Union[str, None] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        **kwargs
    ):
        super().__init__(public=public, **kwargs)
        self.name = name
        self.version = version
        self.source = source
        self.notes = notes
        self.group = group
