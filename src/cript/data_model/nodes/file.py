import os
from logging import getLogger
from typing import Union

from beartype import beartype

from cript.cache import get_cached_api_session
from cript.api.rest import API
from cript.data_model.exceptions import FileSizeLimitError, UniqueNodeError
from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.group import Group
from cript.data_model.nodes.project import Project
from cript.data_model.utils import auto_assign_group, set_node_attributes
from cript.storage_clients import AmazonS3Client, GlobusClient
from cript.utils import convert_file_size, sha256_hash

logger = getLogger(__name__)


class File(BaseNode):
    """The <a href="../file" target="_blank">`File`</a> object represents a
    single computer file. The <a href="../file" target="_blank">`File`</a> object
    is always nested inside a <a href="../project" target="_blank">`Project`</a> object, and
    may exist inside a <a href="../data" target="_blank">`Data`</a> object as well.

    Args:
        project (Union[Project, str]): Parent `Project` object
        source (str): Source of the file
        type (str, optional): File type
        name (str, optional): File name
        checksum (Union[str, None], optional): File checksum for verifying integrity
        unique_name (Union[str, None], optional): Unique file name generated from `File` object UID
        extension (Union[str, None], optional): File extension
        public (bool, optional): Whether the file is publicly viewable
        group (Union[Group, str], optional): `Group` object which manages the file

    !!! success "Use <a href='../base_node' target='_blank'>`BaseNode`</a> methods to manipulate this object"
        Since this object inherits from the <a href="../base_node" target="_blank">`BaseNode`</a> object,
        all the <a href="../base_node" target="_blank">`BaseNode`</a> object methods can be used to manipulate it.
        These include `get()`, `create()`, `delete()`, `save()`, `search()`, `update()`, and `refresh()` methods.
        See the <a href="../base_node" target="_blank">`BaseNode`</a> documentation to learn more about these methods
        and see examples of their use.

    !!! note "Allowed `File` types"
        The allowed `File` types are listed in the
        <a href="https://criptapp.org/keys/file-type/" target="_blank">CRIPT controlled vocabulary</a>
        
    ``` py title="Example"
    # get an existing project
    my_project = Project.get(name="My project")

    # create a new file in the existing project
    f = File.create(
        project=my_project
        name="my_calibration_data.txt",
        type="calibration",
    )
    ```
    """

    node_name = "File"
    slug = "file"
    alt_names = ["files"]

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
        **kwargs,
    ):
        super().__init__(public=public, **kwargs)
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
    def save(self, get_level: int = 1, update_existing: bool = False):
        """Save the file node and upload it to the file storage provider.

        Args:
            get_level (int, optional): Level to recursively get nested nodes
            update_existing (bool, optional): Whether to update an existing node with the same unique fields

        Raises:
            UniqueNodeError: The file has already been created
        """
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
                if unique_url and update_existing:
                    # Update existing unique node
                    self.url = unique_url
                    self.save(get_level=get_level)
                    return
                else:
                    raise UniqueNodeError(response["errors"][0])

        if api.host == "localhost":
            api.move_copy_file(self.source, api.data_folder)
        elif os.path.exists(self.source):
            url = response["url"]
            uid = response["uid"]
            self._upload_file(api, url, uid)

        set_node_attributes(self, response)
        self._generate_nested_nodes(get_level=get_level)
        logger.info(f"{self.node_name} node has been saved to the database.")

        self.refresh(get_level=get_level)

    def _upload_file(self, api, url, uid):
        # Upload a file to the defined storage provider.
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
    def download_file(self, api, path: str = None):
        """Download the file from the file storage provider.

        Args:
            api (API): Instantiated CRIPT API object
            path (str, optional): Path where file should be downloaded to
        
        ``` py title="Example"
        f.download(api=api)
        ```
        """
        api = get_cached_api_session(self.url)

        if path is None:
            path = f"./{self.name}"

        if isinstance(api.storage_client, GlobusClient):
            api.storage_client.https_download(self, path)
        elif isinstance(api.storage_client, AmazonS3Client):
            print("AWS file storage is not implemented yet")
