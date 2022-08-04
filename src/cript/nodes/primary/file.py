import os
from typing import Union
from logging import getLogger

from beartype import beartype


from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes.primary.group import Group
from cript.nodes.primary.project import Project
from cript.nodes.primary.data import Data
from cript.validators import validate_required, validate_key
from cript.utils import sha256_hash
from cript.utils import auto_assign_group


logger = getLogger(__name__)


class File(BasePrimary):
    """Object representing a single raw data file."""

    node_name = "File"
    slug = "file"
    list_name = "files"
    required = ["group", "project", "data", "source", "type"]
    unique_together = ["checksum", "created_by"]

    @beartype
    def __init__(
        self,
        name: str = None,
        group: Union[Group, str] = None,
        project: Union[Project, str] = None,
        data: list[Union[Data, str]] = None,
        source: str = None,
        type: str = "data",
        checksum: Union[str, None] = None,
        extension: Union[str, None] = None,
        unique_name: str = None,
        external_source: Union[str, None] = None,
        public: bool = False,
    ):
        super().__init__(public=public)
        self.group = auto_assign_group(group, project)
        self.project = project
        self.data = data
        self.checksum = checksum
        self.name = name
        self.unique_name = unique_name
        self.source = source
        self.extension = extension
        self.external_source = external_source
        self.type = type
        validate_required(self)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = validate_key("file-type", value)

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        if value != "Invalid":
            if os.path.exists(value):
                value = value.replace("\\", "/")
                logger.info(f"Generating checksum for {value}.")
                self.checksum = sha256_hash(value)
                logger.info("Checksum generated successfully.")
                self.name = os.path.basename(value)
            elif value.startswith(("http", "https")):
                pass
            else:
                raise FileNotFoundError(
                    "The file could not be found on the local filesystem."
                )
        self._source = value

    @beartype
    def add_data(self, data: Union[Data, dict]):
        self._add_node(data, "data")

    @beartype
    def remove_data(self, data: Union[Data, int]):
        self._remove_node(data, "data")
