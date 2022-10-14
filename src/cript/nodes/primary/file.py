import os
from typing import Union
from logging import getLogger

from beartype import beartype


from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes.primary.group import Group
from cript.nodes.primary.project import Project
from cript.utils import sha256_hash
from cript.utils import auto_assign_group


logger = getLogger(__name__)


class File(BasePrimary):
    """Object representing a single raw data file."""

    node_name = "File"
    slug = "file"
    list_name = "files"

    @beartype
    def __init__(
        self,
        project: Union[Project, str],
        source: str,
        type: str = "data",
        name: str = None,
        checksum: Union[str, None] = None,
        unique_name: Union[str, None] = None,
        extension: Union[str, None] = None,
        public: bool = False,
        group: Union[Group, str] = None,
    ):
        super().__init__(public=public)
        self.project = project
        self.type = type
        self.name = name
        self.checksum = checksum
        self.unique_name = unique_name
        self.extension = extension
        self.source = source
        self.group = auto_assign_group(group, project)

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        if value != "Invalid":
            if os.path.exists(value):
                # Clean path
                value = value.replace("\\", "/")

                # Generate checksum
                logger.info(f"Generating checksum for {value}.")
                self.checksum = sha256_hash(value)
                logger.info("Checksum generated successfully.")

                self.name = os.path.basename(value)
                self.extension = os.path.splitext(value)[-1]
            elif value.startswith(("http://", "https://")):
                pass
            else:
                raise FileNotFoundError(
                    f"The file could not be found on the local filesystem. {value}"
                )
        self._source = value
