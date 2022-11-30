import json

import requests
from logging import getLogger
import globus_sdk
from globus_sdk.scopes import ScopeBuilder

from cript.data_model.nodes.base_node import BaseNode
from cript.storage_clients.exceptions import InvalidAuthCode, FileUploadError, FileDownloadError


logger = getLogger(__name__)


class GlobusClient:
    def __init__(self, api):
        self.api = api
        self.session = self.api.session
        self.url = self.api.url
        self.endpoint_id = self.api.storage_info["endpoint_id"]
        self.native_client_id = self.api.storage_info["native_client_id"]
        self.storage_path = self.api.storage_info["path"]
        self.auth_client = None
        self.tokens = None
        self.transfer_client = None

    def https_download(self, node: BaseNode, path: str):
        """
        Download a file from a Globus endpoint.

        :param node: The `File` node object.
        :param path: Path where the file should go.
        """
        if self.transfer_client is None:
            if self.tokens is None:
                authorize_url = self.get_authorize_url()
                self.set_tokens(authorize_url)
            self._initialize_transfer_client()

        # Stage the transfer
        globus_url = self._stage_download(node.uid)
        logger.info(f"Download of file {node.uid} from Globus endpoint in progress.")

        # Perform transfer
        https_auth_token = self.tokens["https_auth_token"]
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
            raise FileDownloadError

    def _stage_download(self, file_uid):
        """
        Sends a POST to the API to stage the Globus endpoint for download.

        :param file_uid: UID of the `File` node object.
        :return: The Globus download URL.
        :rtype: str
        """
        payload = {"file_uid": file_uid}
        response = self.session.post(
            url=f"{self.url}/globus-stage-download/", data=json.dumps(payload)
        )
        if response.status_code != 200:
            raise FileDownloadError
        return json.loads(response.content)

    def https_upload(self, file_url, file_uid, node):
        """
        Upload a file to a Globus endpoint via HTTPS.

        :param file_url: URL of the `File` node object.
        :param file_uid: UID of the `File` node object.
        :param node: The `File` node object.
        """
        if self.transfer_client is None:
            if self.tokens is None:
                authorize_url = self.get_authorize_url()
                self.set_tokens(authorize_url)
            self._initialize_transfer_client()

        # Stage the transfer
        unique_file_name = self._stage_upload(file_uid, node.checksum)
        logger.info(f"Upload of file {file_uid} to Globus endpoint in progress.")

        # Get endpoint URL
        endpoint = self.transfer_client.get_endpoint(self.endpoint_id)
        https_server = endpoint["https_server"]

        # Perform the transfer
        https_auth_token = self.tokens["https_auth_token"]
        headers = {"Authorization": f"Bearer {https_auth_token}"}
        try:
            response = requests.put(
                url=f"{https_server}/{self.storage_path}{file_uid}/{unique_file_name}",
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
            node.delete()
            logger.info(f"Upload of file {file_uid} failed: {error}")
            raise FileUploadError

    def get_authorize_url(self):
        """
        Get the authorization URL.

        :return: Authorization URL
        :rtype: str
        """
        if self.auth_client is None:
            self.auth_client = globus_sdk.NativeAppAuthClient(self.native_client_id)

        # Define scopes
        auth_scopes = "openid profile email"
        transfer_scopes = "urn:globus:auth:scope:transfer.api.globus.org:all"
        https_scopes = ScopeBuilder(self.endpoint_id).url_scope_string("https")

        # Initiate auth flow
        self.auth_client.oauth2_start_flow(
            requested_scopes=[auth_scopes, transfer_scopes, https_scopes],
            refresh_tokens=True,
        )
        return self.auth_client.oauth2_get_authorize_url()

    def set_tokens(self, authorize_url, auth_code=None):
        """
        Uses the authorization code to retrieve and save the tokens.

        :param authorize_url: The authorization URL to which users should be sent.
        :param auth_code: The authorization code copied from the web UI.
        """
        if auth_code is None:
            # Prompt user to login and enter code
            print(f"\nPlease go to this URL and login:\n\n{authorize_url}\n")
            auth_code = input("Enter the code here: ").strip()

        # Get tokens
        try:
            token_response = self.auth_client.oauth2_exchange_code_for_tokens(auth_code)
        except globus_sdk.services.auth.errors.AuthAPIError as error:
            raise InvalidAuthCode

        auth_data = token_response.by_resource_server["auth.globus.org"]
        transfer_data = token_response.by_resource_server["transfer.api.globus.org"]
        https_transfer_data = token_response.by_resource_server[self.endpoint_id]
        self.tokens = {
            "auth_token": auth_data["access_token"],
            "transfer_access_token": transfer_data["access_token"],
            "transfer_refresh_token": transfer_data["refresh_token"],
            "transfer_expiration": transfer_data["expires_at_seconds"],
            "https_auth_token": https_transfer_data["access_token"],
        }

    def _initialize_transfer_client(self):
        """
        Initialize and save the transfer client so the user doesn't have to
        auth for each upload.

        :param auth_client: Instance of `globus_sdk.NativeAppAuthClient`
        :param tokens: The relevant auth, transfer, and refresh tokens.
        """
        # Initialize transfer client
        transfer_authorizer = globus_sdk.RefreshTokenAuthorizer(
            self.tokens["transfer_refresh_token"],
            self.auth_client,
            access_token=self.tokens["transfer_access_token"],
            expires_at=self.tokens["transfer_expiration"],
        )
        transfer_client = globus_sdk.TransferClient(authorizer=transfer_authorizer)

        # Save the transfer client and tokens as object attributes
        self.transfer_client = transfer_client

    def _stage_upload(self, file_uid, file_checksum):
        """
        Sends a POST to the API to stage the Globus endpoint for upload.

        :param file_uid: UID of the `File` node object.
        :file_checksum: The checksum of the raw file.
        :return: The unique file name to be used for upload.
        :rtype: str
        """
        payload = {"file_uid": file_uid, "file_checksum": file_checksum}
        response = self.session.post(
            url=f"{self.url}/globus-stage-upload/",
            data=json.dumps(payload),
        )
        if response.status_code != 200:
            raise FileUploadError
        return json.loads(response.content)["unique_file_name"]
