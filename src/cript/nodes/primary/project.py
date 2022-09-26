from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes.primary.group import Group
from cript.paginators import Paginator

logger = getLogger(__name__)


class Project(BasePrimary):
    """
    Object representing a logical grouping of `Material`, `File`,
    and `Collection` objects.
    """

    node_name = "Project"
    slug = "project"

    @beartype
    def __init__(
        self,
        name: str,
        collections: str = None,
        materials: str = None,
        files: str = None,
        notes: Union[str, None] = None,
        public: bool = False,
        group: Union[Group, str] = None,
    ):
        super().__init__(public=public)
        self.name = name
        self.collections = collections
        self.materials = materials
        self.files = files
        self.notes = notes
        self.group = group

    @property
    def collections(self):
        return self._collections

    @collections.setter
    def collections(self, value):
        self._collections = Paginator(url=value)

    @property
    def materials(self):
        return self._materials

    @materials.setter
    def materials(self, value):
        self._materials = Paginator(url=value)

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, value):
        self._files = Paginator(url=value)
