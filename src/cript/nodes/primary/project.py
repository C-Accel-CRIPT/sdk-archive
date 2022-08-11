from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes.primary.group import Group


logger = getLogger(__name__)


class Project(BasePrimary):
    """
    Object representing a logical grouping of :class:`Material`, :class:`File`,
    and :class:`Collection` objects.
    """

    node_name = "Project"
    slug = "project"

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        name: str,
        materials=None,
        files=None,
        collections=None,
        public: bool = False,
    ):
        super().__init__(public=public)
        self.group = group
        self.name = name
        self.materials = materials if materials else []
        self.files = files if files else []
        self.collections = collections if collections else []
