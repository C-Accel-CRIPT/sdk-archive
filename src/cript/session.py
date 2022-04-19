import os
import json
import urllib
import warnings
from pprint import pprint
from typing import Union
from getpass import getpass

import requests
from beartype import beartype
from beartype.typing import Type
import globus_sdk
from globus_sdk.scopes import ScopeBuilder

from cript import VERSION, NODE_CLASSES
from cript.nodes import Base, User
from cript.utils import convert_file_size, display_errors
from cript.exceptions import (
    APIAuthError,
    APIRefreshError,
    APISaveError,
    APIDeleteError,
    APISearchError,
    APIGetError,
    APIFileUploadError,
    DuplicateNodeError,
    FileSizeLimitError,
)


class API:
    version = VERSION
    keys = None

    def __init__(self, url: str = None, token: str = None):
        """
        Establishes a session with the CRIPT API.

        :param url: The base URL for the relevant CRIPT instance.
        :param token: The user's API token.
        """
        self.latest_version = None
        self.user = None
        self.storage_info = None
        if url is None:
            url = input("Base URL: ")
        if token is None:
            token = getpass("API Token: ")
        self.url = url.rstrip("/") + "/api"

        self.session = requests.Session()
        self.session.headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "Accept": f"application/json; version={self.version}",
        }

        # Test API authentication by fetching session info and keys
        response = self.session.get(f"{self.url}/session-info/")
        if response.status_code == 200:
            self.latest_version = response.json()["latest_version"]
            self.user = User(**response.json()["user_info"])
            self.storage_info = response.json()["storage_info"]
            API.keys = response.json()["keys"]  # For use by validators
        elif response.status_code == 404:
            raise APIAuthError("Please provide a correct base URL.")
        else:
            raise APIAuthError(display_errors(response.content))

        print(f"Connection to the API was successful!")

        # Warn user if an update is required
        if self.version != self.latest_version:
            warnings.warn(response.json()["version_warning"], stacklevel=2)

    def __repr__(self):
        return f"Connected to {self.url}"

    def __str__(self):
        return f"Connected to {self.url}"

    @beartype
    def refresh(self, node: Base):
        """
        Overwrite a node's attributes with the latest values from the DB.

        :param node: The node to refresh.
        """
        if hasattr(node, "url"):
            if node.url:
                response = self.session.get(node.url)
                self._set_node_attributes(node, response.json())
                self._generate_nodes(node)
            else:
                raise APIRefreshError(
                    "Before you can refresh a node, you must either save it or define it's URL."
                )
        else:
            raise APIRefreshError(
                f"{node.node_name} is a secondary node, thus cannot be refreshed."
            )

    @beartype
    def save(self, node: Base, auto_update=False):
        """
        Create or update a node in the DB.

        :param node: The node to be saved.
        :param auto_update: Indicates whether to update a node that matches a unique constraint.
        """
        if node.node_type == "primary":
            if node.url:
                # Update an existing object via PUT
                response = self.session.put(url=node.url, data=node._to_json())
            else:
                # Create a new object via POST
                response = self.session.post(
                    url=f"{self.url}/{node.slug}/", data=node._to_json()
                )
        else:
            raise APISaveError(
                f"The save() method cannot be called on secondary nodes such as {node.node_name}"
            )

        if response.status_code in (200, 201):
            # Handle new file uploads
            if node.slug == "file" and os.path.exists(node.source):
                file_uid = response.json()["uid"]  # Grab uid from JSON response
                self._upload_file(file_uid, node)

            self._set_node_attributes(node, response.json())
            self._generate_nodes(node)

            # Update File node source field
            if node.slug == "file":
                self.refresh(node)

            print(f"{node.node_name} node has been saved to the database.")

        else:
            try:
                # Raise error if duplicate node is found
                response_dict = json.loads(response.content)
                if "duplicate" in response_dict:
                    response_dict.pop("duplicate")
                    raise DuplicateNodeError(display_errors(json.dumps(response_dict)))
            except json.decoder.JSONDecodeError:
                pass
            raise APISaveError(display_errors(response.content))

    def _set_node_attributes(self, node, obj_json):
        """
        Set node attributes using data from an API response.

        :param node: The node you want to set attributes for.
        :param response: The response from an API call.
        """
        for json_key, json_value in obj_json.items():
            setattr(node, json_key, json_value)

    def _upload_file(self, file_uid, node):
        """ "
        Upload the file to Globus or S3.

        :param node: ID of the File node.
        """
        storage_provider = self.storage_info["provider"]
        max_file_size = self.storage_info["max_file_size"]

        # Check if file is too big
        file_size = os.path.getsize(node.source)
        if file_size > max_file_size:
            raise FileSizeLimitError(convert_file_size(max_file_size))

        if storage_provider == "globus":
            self._globus_https_upload(file_uid, node)
        elif storage_provider == "s3":
            if file_size < 6291456:
                self._s3_single_file_upload(file_uid, node.source)
            else:
                # Multipart uploads for files bigger than 6 MB
                # Ref: https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html
                self._s3_multipart_file_upload(file_uid, node.source)

    def _globus_https_upload(self, file_uid, file_obj):
        """
        Upload a file to a Globus endpoint via HTTPS.

        :param file_uid: UID of the File node.
        :param file_path: Path to file on local filesystem.
        """
        endpoint_id = self.storage_info["endpoint_id"]
        native_client_id = self.storage_info["native_client_id"]

        if not hasattr(self, "globus_transfer_client"):
            client, tokens = self._globus_user_auth(endpoint_id, native_client_id)

            # Initialize transfer client
            transfer_authorizer = globus_sdk.RefreshTokenAuthorizer(
                tokens["transfer_refresh_token"],
                client,
                access_token=tokens["transfer_access_token"],
                expires_at=tokens["transfer_expiration"],
            )
            transfer_client = globus_sdk.TransferClient(authorizer=transfer_authorizer)

            # Save the client and tokens so the user doesnt have to auth each upload
            self.globus_transfer_client = transfer_client
            self.globus_tokens = tokens

        # Stage the transfer
        unique_file_name = self._globus_stage_upload(file_uid, file_obj.checksum)

        # Get endpoint URL
        endpoint = self.globus_transfer_client.get_endpoint(endpoint_id)
        https_server = endpoint["https_server"]

        print("\nUpload in progress ...\n")

        # Perform the transfer
        https_auth_token = self.globus_tokens["https_auth_token"]
        headers = {"Authorization": f"Bearer {https_auth_token}"}
        response = requests.put(
            url=f"{https_server}/files/{file_uid}/{unique_file_name}",
            data=open(file_obj.source, "rb"),
            headers=headers,
        )
        if response.status_code != 200:
            raise APIFileUploadError

    def _globus_user_auth(self, endpoint_id, client_id):
        """
        Prompts a user to authenticate using their Globus credentials.

        :param endpoint_id: ID of the Globus endpoint.
        :param client_id: ID of the Globus Native Client.
        :return: Tokens generated after successful auth.
        """
        client = globus_sdk.NativeAppAuthClient(client_id)

        # Define scopes
        auth_scopes = "openid profile email"
        transfer_scopes = "urn:globus:auth:scope:transfer.api.globus.org:all"
        https_scopes = ScopeBuilder(endpoint_id).url_scope_string("https")

        # Initiate auth flow
        client.oauth2_start_flow(
            requested_scopes=[auth_scopes, transfer_scopes, https_scopes],
            refresh_tokens=True,
        )
        authorize_url = client.oauth2_get_authorize_url()

        # Prompt user to login and enter code
        print(f"Please go to this URL and login:\n\n{authorize_url}\n")
        auth_code = input("Enter the code here: ").strip()
        token_response = client.oauth2_exchange_code_for_tokens(auth_code)

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
        return (client, tokens)

    def _globus_stage_upload(self, file_uid, file_checksum):
        """
        Sends a POST to the REST API to stage the Globus endpoint for upload.

        Staging consists of creating a directory on the endpoint, applying an
        access rule to he directory, then removing the access rule after a
        specified expiration timer.

        :param file_uid: UID of the File node.
        :return: The unique file name to be used for upload.
        """
        payload = {"file_uid": file_uid, "file_checksum": file_checksum}
        response = self.session.post(
            url=f"{self.url}/globus-stage-upload/",
            data=json.dumps(payload),
        )
        if response.status_code != 200:
            raise APIFileUploadError
        return json.loads(response.content)["unique_file_name"]

    def _s3_single_file_upload(self, file_uid, file_path):
        """
        Performs a single file upload to AWS S3.

        :param file_uid: The UID of the File node.
        :param file_path: The path to the file on the local filesystem.
        """
        # Generate signed URL for uploading
        data = {"action": "upload", "file_uid": file_uid}
        response = self.session.post(
            url=f"{self.url}/signed-url/", data=json.dumps(data)
        )

        # Upload file
        if response.status_code == 200:
            print("\nUpload in progress ...\n")
            url = json.loads(response.content)
            files = {"file": open(file_path, "rb")}
            response = requests.put(url=url, files=files)
            if response.status_code != 200:
                raise APIFileUploadError
        else:
            raise APIFileUploadError

    def _s3_multipart_file_upload(self, file_uid, file_path):
        """
        Performs a multipart file upload to AWS S3.

        :param file_uid: UID of the File node.
        :param file_path: Path to the file on the local filesystem.
        """
        chunk_size = 500 * 1024**2

        # Create multipart upload and get upload ID
        data = {"action": "create", "file_uid": file_uid}
        response = self.session.post(
            url=f"{self.url}/multipart-upload/",
            data=json.dumps(data),
        )
        upload_id = json.loads(response.content)["UploadId"]

        # Upload file in chunks
        print("\nUpload in progress ...\n")
        parts = []
        with open(file_path, "rb") as local_file:
            while True:
                file_data = local_file.read(chunk_size)
                if not file_data:
                    break

                # Generate signed URL for uploading
                data = {
                    "action": "upload",
                    "file_uid": file_uid,
                    "upload_id": upload_id,
                    "part_number": len(parts) + 1,
                }
                response = self.session.post(
                    url=f"{self.url}/signed-url/", data=json.dumps(data)
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
            url=f"{self.url}/multipart-upload/",
            data=json.dumps(data),
        )
        if response.status_code != 200:
            raise APIFileUploadError

    def delete(self, node: Base):
        """
        Delete a node in the DB and clear it locally.

        :param node: The node to be deleted.
        :return: Response message.
        """
        if node.node_type == "primary":
            if node.url:
                response = self.session.delete(url=node.url)
                if response.status_code == 204:
                    print(f"{node.node_name} node has been deleted from the database.")
                    # Set specific fields to None, indicating the object has been deleted from DB
                    node.url = None
                    node.uid = None
                    node.created_at = None
                    node.updated_at = None
                else:
                    raise APIDeleteError(display_errors(response.content))
            else:
                raise APIDeleteError(
                    f"This {node.node_name} node does not exist in the database."
                )
        else:
            raise APIDeleteError(
                f"The delete() method cannot be called on secondary nodes such as {node.node_name}"
            )

    @beartype
    def search(self, node_class: Type[Base], query: dict = None):
        """
        Send a query to the API and print the results.

        :param node: The node type you want to search.
        :param query: A dictionary defining the query parameters.
        :return: A JSONPaginator object.
        """
        if node_class.node_type == "secondary":
            raise APISearchError(
                f"{node_class.node_name} is a secondary node, thus cannot be searched."
            )

        if isinstance(query, dict):
            query_slug = self._generate_query_slug(query)
            response = self.session.get(f"{self.url}/{node_class.slug}/?{query_slug}")
        elif query is None:
            response = self.session.get(f"{self.url}/{node_class.slug}/")
        else:
            raise APISearchError(f"'{query}' is not a valid query.")

        if response.status_code != 200:
            raise APISearchError(display_errors(response.content))

        return JSONPaginator(self.session, response.content)

    def _generate_query_slug(self, query):
        """Generate the query URL slug."""
        slug = ""
        for key in query:
            value = query[key]
            if isinstance(value, str):
                value = urllib.parse.quote(value.encode("utf8"))
            slug += f"{key}={value}&"
        return slug

    @beartype
    def get(self, obj: Union[str, Type[Base]], query: dict = None, counter: int = 0):
        """
        Get the JSON for a node and use it to generated a local node object.

        :param url: The API URL of the node.
        :param counter: Cross-method recursion counter.
        :return: The generated node object.
        """
        # Fetch node from a URL, if defined
        if isinstance(obj, str):
            obj_json = self._get_from_url(obj)

            # Define node class from URL slug
            node_slug = obj.rstrip("/").rsplit("/")[-2]
            node_class = self._define_node_class(node_slug)

        # Fetch node from search query, if defined
        elif issubclass(obj, Base) and query:
            obj_json = self._get_from_query(obj, query)
            node_class = obj
        else:
            raise APIGetError(
                f"Please enter a node URL or a node class with a search query."
            )

        # Return the local node object if it already exists
        local_node = self._get_local_primary_node(obj_json["url"])
        if local_node:
            return local_node
        else:
            node = node_class(**obj_json)
            if counter > 0:
                counter += 1
            self._generate_nodes(node, counter=counter)
            return node

    def _get_from_url(self, url):
        """Get a node using a URL."""
        if self.url not in url:
            raise APIGetError("Please enter a valid node URL.")
        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise APIGetError(f"The specified node was not found.")

    def _get_from_query(self, node_class, query):
        """Get a node using a search query."""
        results = self.search(node_class=node_class, query=query)
        if results.count < 1:
            raise APIGetError("Your query did not match any existing nodes.")
        elif results.count > 1:
            raise APIGetError("Your query mathced more than one node.")
        else:
            return results.current["results"][0]

    def _generate_nodes(self, node: Base, counter: int = 0):
        """
        Generate nested node objects within a given node.

        :param node: The parent node.
        :param counter: Cross method recursion counter.
        """
        # Limit recursion to one level
        if counter > 1:
            return

        node_dict = node.__dict__
        for key, value in node_dict.items():
            # Skip the url field
            if key == "url":
                continue
            # Generate primary nodes
            if isinstance(value, str) and self.url in value:
                # Check if node already exists in memory
                local_node = self._get_local_primary_node(value)
                if local_node:
                    node_dict[key] = local_node
                else:
                    try:
                        node_dict[key] = self.get(value, counter=counter + 1)
                    except APIGetError:
                        # Leave the URL if node is not viewable
                        pass
            # Generate secondary nodes
            elif isinstance(value, dict):
                node_class = self._define_node_class(key)
                secondary_node = node_class(**value)
                node_dict[key] = secondary_node
                self._generate_nodes(secondary_node, counter=counter + 1)
            # Handle lists
            elif isinstance(value, list):
                for i in range(len(value)):
                    # Generate primary nodes
                    if isinstance(value[i], str) and self.url in value[i]:
                        # Check if node already exists in memory
                        local_node = self._get_local_primary_node(value[i])
                        if local_node:
                            value[i] = local_node
                        else:
                            try:
                                value[i] = self.get(value[i], counter=counter + 1)
                            except APIGetError:
                                # Leave the URL if node is not viewable
                                pass
                    # Generate secondary nodes
                    elif isinstance(value[i], dict):
                        node_class = self._define_node_class(key)
                        secondary_node = node_class(**value[i])
                        value[i] = secondary_node
                        self._generate_nodes(secondary_node, counter=counter + 1)

    def _define_node_class(self, key: str):
        """
        Find the correct class associated with a given key.

        :param key: The key used to find the correct class.
        :return: The correct node class.
        """
        for node_cls in NODE_CLASSES:
            # Use node slug
            if hasattr(node_cls, "slug") and node_cls.slug == key:
                return node_cls
            # Use node list name (e.g., properties)
            if hasattr(node_cls, "list_name") and node_cls.list_name == key:
                return node_cls
        return None

    def _get_local_primary_node(self, url: str):
        """
        Use a URL to get a primary node object stored in memory.

        :param url: The URL to match against existing node objects.
        :return: The matching object or None.
        """
        for instance in Base.__refs__:
            if hasattr(instance, "url") and url == instance.url:
                return instance
        return None


class JSONPaginator:
    """Paginate JSON response content sent from the API."""

    def __init__(self, session, content):
        self._session = session
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
            response = self._session.get(next_url)
            self.current = response.content
        else:
            raise AttributeError("You're currently on the final page.")

    @property
    def previous(self):
        """Flip to the previous page."""
        previous_url = self.current["previous"]
        if previous_url:
            response = self._session.get(previous_url)
            self.current = response.content
        else:
            raise AttributeError("You're currently on the first page.")

    def to_page(self, page_number: int):
        """
        Navigate to a specific page in the results.

        :param page_number: The page number as an int.
        """
        if self.current["next"]:
            url = self.current["next"]
        elif self.current["previous"]:
            url = self.current["previous"]

        url = url.split("?page=")[0]
        url += f"?page={str(page_number)}"

        response = self._session.get(url)
        if response.status_code == 200:
            self.current = response.content
        else:
            raise ValueError(f"{page_number} is not a valid page number.")
