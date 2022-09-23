import json

import requests
from logging import getLogger
import globus_sdk
from globus_sdk.scopes import ScopeBuilder

from cript.nodes.primary.file import File
from cript.exceptions import APIFileUploadError
from cript.exceptions import APIFileDownloadError


logger = getLogger(__name__)


class GlobusClient:
    def __init__(self, api):
        self.api = api
        self.session = self.api.session
        self.api_url = self.api.api_url
        self.endpoint_id = self.api.storage_info["endpoint_id"]
        self.native_client_id = self.api.storage_info["native_client_id"]
        self.storage_path = self.api.storage_info["path"]
        self.transfer_client = None
        self.tokens = None

    def https_download(self, node: File, path: str):
        """
        Download a file from a Globus endpoint.
        :param node: The `File` node object.
        :param path: Path where the file should go.
        """
        if self.transfer_client is None:
            auth_client, tokens = self._globus_user_auth(
                self.endpoint_id, self.native_client_id
            )
            self._globus_set_transfer_client(auth_client, tokens)

        # Stage the transfer
        globus_url = self._globus_stage_download(node.uid)
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

    def https_upload(self, file_url, file_uid, node):
        """
        Upload a file to a Globus endpoint via HTTPS.
        :param file_url: URL of the `File` node object.
        :param file_uid: UID of the `File` node object.
        :param node: The `File` node object.
        """
        if self.transfer_client is None:
            auth_client, tokens = self._globus_user_auth(
                self.endpoint_id, self.native_client_id
            )
            self._globus_set_transfer_client(auth_client, tokens)

        # Stage the transfer
        unique_file_name = self._globus_stage_upload(file_uid, node.checksum)
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
            self.api.delete(node)
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
        self.transfer_client = transfer_client
        self.tokens = tokens

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
