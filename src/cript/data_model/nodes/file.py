import os
from typing import Union
from logging import getLogger

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.group import Group
from cript.data_model.nodes.project import Project
from cript.storage_clients import GlobusClient
from cript.storage_clients import AmazonS3Client
from cript.utils import sha256_hash
from cript.data_model.utils import auto_assign_group
from cript.utils import convert_file_size
from cript.data_model.utils import set_node_attributes
from cript.cache import get_cached_api_session
from cript.data_model.exceptions import FileSizeLimitError
from cript.data_model.exceptions import UniqueNodeError


logger = getLogger(__name__)


class File(BaseNode):
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

    @beartype
    def save(self, max_level: int = 0, update_existing: bool = False):
        api = get_cached_api_session(self.url)

        if api.host == "localhost":
            response = api.save_file(self)
        elif self.url:
            # Update an existing object via PUT
            response = api.put(self.url, data=self._to_json())
        else:
            # Create a new object via POST
            response = api.post(
                url=f"{api.url}/{self.slug}/",
                data=self._to_json(),
                valid_codes=[201, 400],
            )

            # Check if a unique error was returned
            if "unique" in response:
                unique_url = response.pop("unique")
                if unique_url and update_existing == True:
                    # Update existing unique node
                    self.url = unique_url
                    self.save(max_level=max_level)
                    return
                else:
                    raise UniqueNodeError(response["errors"][0])

        if api.host == "localhost":
            api.move_copy_file(self.source, api.data_folder)
        else:
            url = response["url"]
            uid = response["uid"]
            self._upload_file(api, url, uid)

        set_node_attributes(self, response)
        self._generate_nested_nodes(max_level=max_level)
        logger.info(f"{self.node_name} node has been saved to the database.")

        self.refresh(max_level=max_level)

    def _upload_file(self, api, url, uid):
        """
        Upload a file to the defined storage provider.
        """
        # Check if file is too big
        max_file_size = api.storage_info["max_file_size"]
        file_size = os.path.getsize(self.source)
        if file_size > max_file_size:
            raise FileSizeLimitError(convert_file_size(max_file_size))

        if isinstance(api.storage_client, GlobusClient):
            api.storage_client.https_upload(url, uid, self)
        elif isinstance(api.storage_client, AmazonS3Client):
            if file_size < 6291456:
                api.storage_client.single_file_upload(uid, self)
            else:
                # Multipart uploads for files bigger than 6 MB
                # Ref: https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html
                api.storage_client.multipart_file_upload(uid, self)

    @beartype
    def download_file(self, path: str = None, api=None):
        """
        Download a file from the defined storage provider.

        :param path: Path where the file should go.
        """
        api = get_cached_api_session(self.url)

        if path is None:
            path = f"./{self.name}"

        if isinstance(api.storage_client, GlobusClient):
            api.storage_client.https_download(self, path)
        elif isinstance(api.storage_client, AmazonS3Client):
            pass  # Coming soon
