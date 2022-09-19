import os
import json
import urllib
import warnings
from typing import Union
from getpass import getpass
from logging import getLogger
from distutils.version import StrictVersion

import requests
from beartype import beartype
from beartype.typing import Type
import globus_sdk
from globus_sdk.scopes import ScopeBuilder

from cript import NODE_CLASSES, __api_version__
from cript.nodes.base import Base
from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes.primary.user import User
from cript.nodes.primary.file import File
from cript.nodes.secondary.base_secondary import BaseSecondary
from cript.utils import (
    get_api_url,
    convert_to_api_url,
    convert_file_size,
    display_errors,
)
from cript.exceptions import (
    APIAuthError,
    APIRefreshError,
    APISaveError,
    APIDeleteError,
    APISearchError,
    APIGetError,
    APIFileUploadError,
    APIFileDownloadError,
    DuplicateNodeError,
    FileSizeLimitError,
)


logger = getLogger(__name__)


class API:
    """The entry point for interacting with the CRIPT API."""

    api_version = __api_version__
    keys = None

    def __init__(self, host: str = None, token: str = None, tls: bool = True):
        """
        Establishes a session with a CRIPT API endpoint.

        :param host: The hostname of the relevant CRIPT instance. (e.g., criptapp.org)
        :param token: The API token used for authentication.
        :param tls: Indicates whether to use TLS encryption for the API connection.
        """
        if host is None:
            host = input("Host: ")
        if token is None:
            token = getpass("API Token: ")
        self.api_url = get_api_url(host, tls)
        self.latest_api_version = None
        self.user = None
        self.storage_info = None

        self.session = requests.Session()
        self.session.headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "Accept": f"application/json; version={self.api_version}",
        }

        # Test API authentication by fetching session info and keys
        response = self.session.get(f"{self.api_url}/session-info/")
        if response.status_code == 200:
            self.latest_api_version = response.json()["latest_version"]
            self.user = self._create_node(User, response.json()["user_info"])
            self.storage_info = response.json()["storage_info"]
            API.keys = response.json()["keys"]  # For use by validators
        elif response.status_code == 404:
            raise APIAuthError("Please provide a correct base URL.")
        else:
            raise APIAuthError(display_errors(response.content))

        logger.info(f"Connection to {self.api_url} API was successful!")

        # Warn user if an update is required
        if StrictVersion(self.api_version) < StrictVersion(self.latest_api_version):
            warnings.warn(response.json()["version_warning"], stacklevel=2)

    def __repr__(self):
        return f"Connected to {self.api_url}"

    def __str__(self):
        return f"Connected to {self.api_url}"

    @beartype
    def refresh(self, node: BasePrimary, max_level: int = 1):
        """
        Overwrite a node's attributes with the latest values from the database.

        :param node: The node to refresh.
        :param max_level: Max depth to recursively generate nested primary nodes.
        """
        if not isinstance(node, BasePrimary):
            raise APIRefreshError(
                f"{node.node_name} is a secondary node, thus cannot be refreshed."
            )

        if node.url:
            response = self.session.get(node.url)
            self._set_node_attributes(node, response.json())
            self._generate_nodes(node, max_level=max_level)
        else:
            raise APIRefreshError(
                "Before you can refresh a node, you must either save it or define its URL."
            )

    @beartype
    def save(
        self, node: BasePrimary, max_level: int = 1, update_existing: bool = False
    ):
        """
        Create or update a node in the database.

        :param node: The node to be saved.
        :param max_level: Max depth to recursively generate nested primary nodes.
        :param update_existing: Indicates whether to update an existing node with the same unique fields.
        """
        if not isinstance(node, BasePrimary):
            raise APISaveError(
                f"The save() method cannot be called on secondary nodes such as {node.node_name}"
            )

        if node.url:
            # Update an existing object via PUT
            response = self.session.put(url=node.url, data=node._to_json())
        else:
            # Create a new object via POST
            response = self.session.post(
                url=f"{self.api_url}/{node.slug}/", data=node._to_json()
            )

        if response.status_code in (200, 201):
            # Handle new file uploads
            if node.slug == "file" and os.path.exists(node.source):
                file_url = response.json()["url"]
                file_uid = response.json()["uid"]
                self._upload_file(file_url, file_uid, node)

            self._set_node_attributes(node, response.json())
            self._generate_nodes(node, max_level=max_level)

            # Update File node source field
            if node.slug == "file":
                self.refresh(node, max_level=max_level)

            logger.info(f"{node.node_name} node has been saved to the database.")

        else:
            try:
                # Check if a duplicate error was returned
                response_dict = json.loads(response.content)
                if "duplicate" in response_dict:
                    duplicate_url = response_dict.pop("duplicate")
                    if update_existing == True and duplicate_url is not None:
                        # Update existing duplicate node
                        node.url = duplicate_url
                        self.save(node)
                        return
                    else:
                        response_content = json.dumps(response_dict)
                        raise DuplicateNodeError(display_errors(response_content))
            except json.decoder.JSONDecodeError:
                pass
            raise APISaveError(display_errors(response.content))

    @staticmethod
    def _set_node_attributes(node, obj_json):
        """
        Set node attributes using data from an API response.

        :param node: The node you want to set attributes for.
        :param obj_json: The JSON representation of the node object.
        """
        for json_key, json_value in obj_json.items():
            setattr(node, json_key, json_value)

    @beartype
    def download_file(self, node: File, path: str = None):
        """
        Download a file from the defined storage provider.

        :param node: The `File` node object.
        :param path: Path where the file should go.
        """
        storage_provider = self.storage_info["provider"]
        if not path:
            path = f"./{node.name}"

        if storage_provider == "globus":
            self._globus_https_download(node, path)
        elif storage_provider == "s3":
            pass  # Coming soon

    def _globus_https_download(self, node: File, path: str):
        """
        Download a file from a Globus endpoint.

        :param node: The `File` node object.
        :param path: Path where the file should go.
        """
        endpoint_id = self.storage_info["endpoint_id"]
        native_client_id = self.storage_info["native_client_id"]

        if not hasattr(self, "globus_transfer_client"):
            auth_client, tokens = self._globus_user_auth(endpoint_id, native_client_id)
            self._globus_set_transfer_client(auth_client, tokens)

        # Stage the transfer
        globus_url = self._globus_stage_download(node.uid)
        logger.info(f"Download of file {node.uid} from Globus endpoint in progress.")

        # Perform transfer
        https_auth_token = self.globus_tokens["https_auth_token"]
        headers = {"Authorization": f"Bearer {https_auth_token}"}
        response = requests.get(
            url=globus_url,
            headers=headers,
            allow_redirects=True,
        )

        if response.status_code == 200:
            # Save the file to local filesystem
            f = open(path, "wb")
            f.write(response.content)
            f.close()
        else:
            raise APIFileDownloadError

    def _globus_stage_download(self, file_uid):
        """
        Sends a POST to the API to stage the Globus endpoint for download.

        :param file_uid: UID of the `File` node object.
        :return: The Globus download URL.
        :rtype: str
        """
        payload = {"file_uid": file_uid}
        response = self.session.post(
            url=f"{self.api_url}/globus-stage-download/", data=json.dumps(payload)
        )
        if response.status_code != 200:
            raise APIFileDownloadError
        return json.loads(response.content)

    def _upload_file(self, file_url, file_uid, node):
        """
        Upload a file to the defined storage provider.

        :param file_uid: UID of the `File` node object.
        :param file_url: URL of the `File` node object.
        :param node: The `File` node object.
        """
        storage_provider = self.storage_info["provider"]
        max_file_size = self.storage_info["max_file_size"]

        # Check if file is too big
        file_size = os.path.getsize(node.source)
        if file_size > max_file_size:
            raise FileSizeLimitError(convert_file_size(max_file_size))

        if storage_provider == "globus":
            self._globus_https_upload(file_url, file_uid, node)
        elif storage_provider == "s3":
            if file_size < 6291456:
                self._s3_single_file_upload(file_uid, node)
            else:
                # Multipart uploads for files bigger than 6 MB
                # Ref: https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html
                self._s3_multipart_file_upload(file_uid, node)

    def _globus_https_upload(self, file_url, file_uid, node):
        """
        Upload a file to a Globus endpoint via HTTPS.

        :param file_url: URL of the `File` node object.
        :param file_uid: UID of the `File` node object.
        :param node: The `File` node object.
        """
        endpoint_id = self.storage_info["endpoint_id"]
        native_client_id = self.storage_info["native_client_id"]

        if not hasattr(self, "globus_transfer_client"):
            auth_client, tokens = self._globus_user_auth(endpoint_id, native_client_id)
            self._globus_set_transfer_client(auth_client, tokens)

        # Stage the transfer
        unique_file_name = self._globus_stage_upload(file_uid, node.checksum)
        logger.info(f"Upload of file {file_uid} to Globus endpoint in progress.")

        # Get endpoint URL
        endpoint = self.globus_transfer_client.get_endpoint(endpoint_id)
        https_server = endpoint["https_server"]

        # Perform the transfer
        https_auth_token = self.globus_tokens["https_auth_token"]
        headers = {"Authorization": f"Bearer {https_auth_token}"}
        storage_path = self.storage_info["path"]
        try:
            response = requests.put(
                url=f"{https_server}/{storage_path}{file_uid}/{unique_file_name}",
                data=open(node.source, "rb"),
                headers=headers,
            )
            error = None
        except requests.exceptions.RequestException as e:
            error = e

        # Delete File node if upload fails
        if error or response.status_code != 200:
            if error is None:
                error = response.status_code
            node.url = file_url
            self.delete(node)
            logger.info(f"Upload of file {file_uid} failed: {error}")
            raise APIFileUploadError

    @staticmethod
    def _globus_user_auth(endpoint_id, client_id):
        """
        Prompts a user authorize using their Globus credentials.

        :param endpoint_id: ID of the Globus endpoint.
        :param client_id: ID of the Globus Native Client.
        :return: A tuple of the auth client and generated tokens.
        :rtype: (globus_sdk.NativeAppAuthClient, dict)
        """
        auth_client = globus_sdk.NativeAppAuthClient(client_id)

        # Define scopes
        auth_scopes = "openid profile email"
        transfer_scopes = "urn:globus:auth:scope:transfer.api.globus.org:all"
        https_scopes = ScopeBuilder(endpoint_id).url_scope_string("https")

        # Initiate auth flow
        auth_client.oauth2_start_flow(
            requested_scopes=[auth_scopes, transfer_scopes, https_scopes],
            refresh_tokens=True,
        )
        authorize_url = auth_client.oauth2_get_authorize_url()

        # Prompt user to login and enter code
        print(f"Please go to this URL and login:\n\n{authorize_url}\n")
        auth_code = input("Enter the code here: ").strip()
        token_response = auth_client.oauth2_exchange_code_for_tokens(auth_code)

        # Get tokens
        auth_data = token_response.by_resource_server["auth.globus.org"]
        transfer_data = token_response.by_resource_server["transfer.api.globus.org"]
        https_transfer_data = token_response.by_resource_server[endpoint_id]
        tokens = {
            "auth_token": auth_data["access_token"],
            "transfer_access_token": transfer_data["access_token"],
            "transfer_refresh_token": transfer_data["refresh_token"],
            "transfer_expiration": transfer_data["expires_at_seconds"],
            "https_auth_token": https_transfer_data["access_token"],
        }

        return auth_client, tokens

    def _globus_set_transfer_client(self, auth_client, tokens):
        """
        Initialize and save the transfer client so the user doesn't have to
        auth for each upload.

        :param auth_client: Instance of `globus_sdk.NativeAppAuthClient`
        :param tokens: The relevant auth, transfer, and refresh tokens.
        """
        # Initialize transfer client
        transfer_authorizer = globus_sdk.RefreshTokenAuthorizer(
            tokens["transfer_refresh_token"],
            auth_client,
            access_token=tokens["transfer_access_token"],
            expires_at=tokens["transfer_expiration"],
        )
        transfer_client = globus_sdk.TransferClient(authorizer=transfer_authorizer)

        # Save the transfer client and tokens as object attributes
        self.globus_transfer_client = transfer_client
        self.globus_tokens = tokens

    def _globus_stage_upload(self, file_uid, file_checksum):
        """
        Sends a POST to the API to stage the Globus endpoint for upload.

        :param file_uid: UID of the `File` node object.
        :file_checksum: The checksum of the raw file.
        :return: The unique file name to be used for upload.
        :rtype: str
        """
        payload = {"file_uid": file_uid, "file_checksum": file_checksum}
        response = self.session.post(
            url=f"{self.api_url}/globus-stage-upload/",
            data=json.dumps(payload),
        )
        if response.status_code != 200:
            raise APIFileUploadError
        return json.loads(response.content)["unique_file_name"]

    def _s3_single_file_upload(self, file_uid, node):
        """
        Performs a single file upload to AWS S3.

        :param file_uid: UID of the `File` node object.
        :param node: The `File` node object.
        """
        # Generate signed URL for uploading
        payload = {
            "action": "upload",
            "file_uid": file_uid,
            "file_checksum": node.checksum,
        }
        response = self.session.post(
            url=f"{self.api_url}/s3-signed-url/", data=json.dumps(payload)
        )

        # Upload file
        if response.status_code == 200:
            logger.info(f"Upload of file {file_uid} to AWS S3 in progress.")
            url = json.loads(response.content)
            files = {"file": open(node.source, "rb")}
            response = requests.put(url=url, files=files)
            if response.status_code != 200:
                raise APIFileUploadError
        else:
            raise APIFileUploadError

    def _s3_multipart_file_upload(self, file_uid, node):
        """
        Performs a multipart file upload to AWS S3.

        :param file_uid: UID of the File node.
        :param node: The `File` node object.
        """
        chunk_size = 500 * 1024**2

        # Create multipart upload and get upload ID
        payload = {
            "action": "create",
            "file_uid": file_uid,
            "file_checksum": node.checksum,
        }
        response = self.session.post(
            url=f"{self.api_url}/s3-multipart-upload/",
            data=json.dumps(payload),
        )
        upload_id = json.loads(response.content)["UploadId"]

        # Upload file in chunks
        logger.info(f"Upload of file {file_uid} to AWS S3 in progress.")
        parts = []
        with open(node.source, "rb") as local_file:
            while True:
                file_data = local_file.read(chunk_size)
                if not file_data:
                    break

                # Generate signed URL for uploading
                data = {
                    "action": "upload",
                    "file_uid": file_uid,
                    "file_checksum": node.checksum,
                    "upload_id": upload_id,
                    "part_number": len(parts) + 1,
                }
                response = self.session.post(
                    url=f"{self.api_url}/s3-signed-url/", data=json.dumps(data)
                )

                # Upload file chunk
                if response.status_code == 200:
                    signed_url = json.loads(response.content)
                    response = requests.put(url=signed_url, data=file_data)
                    if response.status_code == 200:
                        etag = response.headers["ETag"]
                        parts.append({"ETag": etag, "PartNumber": len(parts) + 1})
                    else:
                        raise APIFileUploadError
                else:
                    raise APIFileUploadError

        # Complete multipart upload
        data = {
            "action": "complete",
            "file_uid": file_uid,
            "upload_id": upload_id,
            "parts": parts,
        }
        response = self.session.post(
            url=f"{self.api_url}/s3-multipart-upload/",
            data=json.dumps(data),
        )
        if response.status_code != 200:
            raise APIFileUploadError

    def delete(self, obj: Union[BasePrimary, str, type], query: dict = None):
        """
        Delete a node in the database and clear it locally.

        :param obj: The node to be deleted itself or its class.
        :param query: A dictionary defining the query parameters (e.g., {"name": "NewMaterial"})
        """
        if isinstance(obj, BaseSecondary):
            raise APIDeleteError(
                f"The delete() method cannot be called on secondary nodes such as {obj.node_name}"
            )

        # Delete with node
        if isinstance(obj, BasePrimary):
            if obj.url:
                url = obj.url
            else:
                raise APIDeleteError(
                    f"This {obj.node_name} node does not exist in the database."
                )

        # Delete with URL
        elif isinstance(obj, str):
            url = obj
            if self.api_url not in url:
                raise APIDeleteError("Invalid URL provided.")

        # Delete with search query
        elif issubclass(obj, BasePrimary) and isinstance(query, dict):
            results = self.search(node_class=obj, query=query)
            if results.count == 1:
                url = results.current["results"][0]["url"]
            elif results.count < 1:
                raise APIGetError("Your query did not match any existing nodes.")
            elif results.count > 1:
                raise APIGetError("Your query matched more than one node.")
        else:
            raise APIDeleteError(
                "Please enter a node, valid node URL, or a node class and search query."
            )

        response = self.session.delete(url)
        if response.status_code == 204:
            # Check if node exists locally
            # If it does, clear fields to indicate it has been deleted
            local_node = self._get_local_primary_node(url)
            if local_node:
                local_node.url = None
                local_node.uid = None
                local_node.created_at = None
                local_node.updated_at = None
            logger.info("The node has been deleted from the database.")
        else:
            raise APIGetError(display_errors(response.content))

    @beartype
    def search(
        self,
        node_class: Type[BasePrimary],
        query: dict,
        limit: Union[int, None] = None,
        offset: Union[int, None] = None,
    ):
        """
        Send a query to the API and print the results.

        :param node_class: The class of the node type to query for.
        :param query: A dictionary defining the query parameters (e.g., {"name": "NewMaterial"}).
        :param limit: The max number of items to return.
        :param offset: The starting position of the query.
        :return: A `SearchPaginator` object containing the results.
        :rtype: cript.session.SearchPaginator
        """
        if not issubclass(node_class, BasePrimary):
            raise APISearchError(
                f"{node_class.node_name} is a secondary node, thus cannot be searched."
            )

        # Generate URL
        url = f"{self.api_url}/search/{node_class.slug}/?"
        if limit:
            url += f"limit={str(limit)}&"
        if offset:
            url += f"offset={str(offset)}"

        if isinstance(query, dict):
            payload = json.dumps(query)
            response = self.session.post(url=url, data=payload)
        else:
            raise APISearchError(f"'{query}' is not a valid query.")

        if response.status_code != 200:
            raise APISearchError(display_errors(response.content))
        return SearchPaginator(self.session, response.content, payload)

    @beartype
    def get(
        self,
        obj: Union[str, Type[BasePrimary]],
        query: dict = None,
        level: int = 0,
        max_level: int = 1,
    ):
        """
        Get the JSON for a node and use it to generate a local node object.

        :param obj: The node's URL or class type.
        :param query: Search query if obj argument is a class type.
        :param level: Current nested node level.
        :param max_level: Max depth to recursively generate nested primary nodes.
        :return: The generated node object.
        :rtype: cript.nodes.Base
        """
        # Get node with a URL
        if isinstance(obj, str):
            obj = convert_to_api_url(obj)
            if self.api_url not in obj:
                raise APIGetError("Please enter a valid node URL.")
            response = self.session.get(obj)
            if response.status_code == 200:
                obj_json = response.json()
            else:
                raise APIGetError("The specified node was not found.")
            # Define node class from URL slug
            node_slug = obj.rstrip("/").rsplit("/")[-2]
            node_class = self._define_node_class(node_slug)

        # Get node with a search query
        elif issubclass(obj, BasePrimary) and query:
            results = self.search(node_class=obj, query=query)
            if results.count < 1:
                raise APIGetError("Your query did not match any existing nodes.")
            elif results.count > 1:
                raise APIGetError("Your query matched more than one node.")
            else:
                obj_json = results.current["results"][0]
                node_class = obj
        else:
            raise APIGetError(
                "Please enter a node URL or a node class with a search query."
            )

        # Return the local node object if it already exists
        # Otherwise, create a new node
        local_node = self._get_local_primary_node(obj_json["url"])
        if local_node:
            return local_node
        else:
            node = self._create_node(node_class, obj_json)
            self._generate_nodes(node, level=level, max_level=max_level)
            return node

    def _generate_nodes(self, node: Base, level: int = 0, max_level: int = 1):
        """
        Generate nested node objects within a given node.

        :param node: The parent node.
        :param level: Current nested node level.
        :param max_level: Max depth to recursively generate nested primary nodes.
        """
        if level <= max_level:
            level += 1

        # Limit recursive primary node generation
        skip_primary = False
        if level > max_level:
            skip_primary = True

        node_dict = node.__dict__
        for key, value in node_dict.items():
            # Skip empty values and the url field
            if not value or key == "url":
                continue
            # Generate primary nodes
            if (
                isinstance(value, str)
                and self.api_url in value
                and skip_primary == False
            ):
                # Check if node already exists in memory
                local_node = self._get_local_primary_node(value)
                if local_node:
                    node_dict[key] = local_node
                else:
                    try:
                        node_dict[key] = self.get(
                            value, level=level, max_level=max_level
                        )
                    except APIGetError:
                        # Leave the URL if node is not viewable
                        pass
            # Generate secondary nodes
            elif isinstance(value, dict):
                node_class = self._define_node_class(key)
                secondary_node = node_class(**value)
                node_dict[key] = secondary_node
                self._generate_nodes(secondary_node, level=level, max_level=max_level)
            # Handle lists
            elif isinstance(value, list):
                for i in range(len(value)):
                    # Generate primary nodes
                    if (
                        isinstance(value[i], str)
                        and self.api_url in value[i]
                        and skip_primary == False
                    ):
                        # Check if node already exists in memory
                        local_node = self._get_local_primary_node(value[i])
                        if local_node:
                            value[i] = local_node
                        else:
                            try:
                                value[i] = self.get(
                                    value[i], level=level, max_level=max_level
                                )
                            except APIGetError:
                                # Leave the URL if node is not viewable
                                pass
                    # Generate secondary nodes
                    elif isinstance(value[i], dict):
                        node_class = self._define_node_class(key)
                        secondary_node = node_class(**value[i])
                        value[i] = secondary_node
                        self._generate_nodes(
                            secondary_node, level=level, max_level=max_level
                        )

    @staticmethod
    def _define_node_class(key: str):
        """
        Find the correct class associated with a given key.

        :param key: The key string indicating the class.
        :return: The correct node class.
        :rtype: cript.nodes.Base
        """
        for node_cls in NODE_CLASSES:
            # Use node slug
            if hasattr(node_cls, "slug") and node_cls.slug == key:
                return node_cls
            # Use node list name (e.g., properties)
            if hasattr(node_cls, "list_name") and node_cls.list_name == key:
                return node_cls
        return None

    @staticmethod
    def _create_node(node_class, obj_json):
        """
        Create a node with JSON returned from the API.

        :param node_class: The class of the node to be created.
        :param obj_json: The JSON representation of the node object.
        :return: The created node.
        :rtype: cript.nodes.Base
        """
        # Pop common attributes
        url = obj_json.pop("url")
        uid = obj_json.pop("uid")
        created_at = obj_json.pop("created_at")
        updated_at = obj_json.pop("updated_at")

        # Create node
        node = node_class(**obj_json)

        # Replace common attributes
        node.url = url
        node.uid = uid
        node.created_at = created_at
        node.updated_at = updated_at

        return node

    @staticmethod
    def _get_local_primary_node(url: str):
        """
        Use a URL to get a primary node object stored in memory.

        :param url: The URL to match against existing node objects.
        :return: The matching object or None.
        :rtype: Union[cript.nodes.Base, None]
        """
        for instance in Base.__refs__:
            if hasattr(instance, "url") and url == instance.url:
                return instance
        return None


class SearchPaginator:
    """Paginate search JSON response content."""

    def __init__(self, session, content, payload):
        self._session = session
        self.payload = payload
        self.current = content
        self.count = self.current["count"]

    def __repr__(self):
        return json.dumps(self.current, indent=4)

    def __str__(self):
        return json.dumps(self.current, indent=4)

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, value):
        self._current = json.loads(value)

    @property
    def next(self):
        """Flip to the next page."""
        next_url = self.current["next"]
        if next_url:
            response = self._session.post(url=next_url, data=self.payload)
            self.current = response.content
        else:
            raise AttributeError("You've reached the end of the query.")

    @property
    def previous(self):
        """Flip to the previous page."""
        previous_url = self.current["previous"]
        if previous_url:
            response = self._session.post(url=previous_url, data=self.payload)
            self.current = response.content
        else:
            raise AttributeError("You've reached the beginning of the query.")
