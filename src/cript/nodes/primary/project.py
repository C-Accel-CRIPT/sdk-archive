from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes.primary.group import Group
from cript.nodes.secondary.citation import Citation
from cript.validators import validate_required


logger = getLogger(__name__)


class Project(BasePrimary):
    """
    Object representing a logical grouping of :class:`Material`, :class:`File`,
    and :class:`Collection` objects.
    """

    node_name = "Project"
    slug = "project"
    required = ["group", "name"]
    unique_together = ["name"]

    @beartype
    def __init__(
        self,
        group: Union[Group, str] = None,
        name: str = None,
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
        validate_required(self)
