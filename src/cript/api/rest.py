import json
import warnings
from distutils.version import StrictVersion
from getpass import getpass
from logging import getLogger
from urllib.parse import urlparse

import requests
from beartype import beartype

from cript.api.base import APIBase
from cript.api.exceptions import APIError
from cript.api.utils import convert_to_api_url, get_api_url
from cript.cache import cache_api_session
from cript.data_model.nodes.user import User
from cript.data_model.utils import create_node
from cript.storage_clients import AmazonS3Client, GlobusClient

logger = getLogger(__name__)


class API(APIBase):
    """The entry point for interacting with the remote CRIPT REST API.

    Args:
        host (str, optional): The hostname of the relevant CRIPT instance (e.g., criptapp.org)
        token (str, optional): The API token used for authentication
        tls (bool, optional): Indicates whether to use TLS encryption for the API connection

    Raises:
        APIError: A valid host was not specified or found, or the connection failed

    ``` py title="Example"
    host = "criptapp.org"
    token = os.environ.get("CRIPT_API_KEY")
    api = cript.API(host, token)
    ```
    """

    def __init__(self, host: str = None, token: str = None, tls: bool = True):
        if host is None:
            host = input("Host: ")
        if token is None:
            token = getpass("API Token: ")

        self.url = get_api_url(host, tls)
        self.search_url = f"{self.url}/search"
        self.host = urlparse(self.url).netloc
        self.latest_api_version = None
        self.user = None
        self.storage_info = None
        self.vocab = None

        self.session = requests.Session()
        self.session.headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "Accept": f"application/json; version={self.api_version}",
        }

        # Test API authentication by fetching session info
        try:
            response = self.session.get(f"{self.url}/session-info/")
        except Exception as e:
            raise APIError(
                "Connection API failed, please review your host and token"
            ) from e
        if response.status_code == 200:
            response_json = response.json()
            self.latest_api_version = response_json["latest_version"]
            self.user = create_node(User, response.json()["user_info"])
            self.storage_info = response.json()["storage_info"]
            self.vocab = response.json().get("vocab")
        elif response.status_code == 404:
            raise APIError("Please provide a valid host.")
        else:
            raise APIError(str(response.content))

        logger.info(f"Connection to {self.url} API was successful!")

        # Define storage client
        provider = self.storage_info["provider"]
        if provider == "globus":
            self.storage_client = GlobusClient(self)
        elif provider == "s3":
            self.storage_client = AmazonS3Client(self)

        # Warn user if an update is required
        if StrictVersion(self.api_version) < StrictVersion(self.latest_api_version):
            warnings.warn(response.json()["version_warning"], stacklevel=2)

        # Add session to cache
        cache_api_session(self)

    def __repr__(self):
        return f"Connected to {self.url}"

    def __str__(self):
        return f"Connected to {self.url}"

    @beartype
    def get(self, url: str):
        """Performs an HTTP GET request and handles errors.

        Args:
            url (str): URL of the CRIPT node

        Raises:
            APIError: The specified node was not found

        Returns:
            response (dict): Response of the GET request
        
        ``` py title="Example"
        url = "https://criptapp.org/api/collection/30b17158-45f0-402d-a696-5de5fb172931/"
        response = api.get(url)
        ```
        """
        url = convert_to_api_url(url)
        response = self.session.get(url=url)
        if response.status_code != 200:
            raise APIError("The specified node was not found.")
        return json.loads(response.content)

    @beartype
    def post(self, url: str, data: str = None, valid_codes: list = [201]):
        """Performs an HTTP POST request and handles errors.

        Args:
            url (str): URL of the CRIPT node
            data (str, optional): Data payload to POST
            valid_codes (list, optional): Response codes to consider the request a success

        Raises:
            APIError: The response did not contain a valid response code

        Returns:
            response (dict): Response of the POST request
    
        ``` py title="Example"
        url = "https://criptapp.org/api/collection/30b17158-45f0-402d-a696-5de5fb172931/"
        response = api.post(
            url=url,
            data=json.dumps({"name": "My new collection", project=project}),
        )
        ```
        """
        url = convert_to_api_url(url)
        response = self.session.post(url=url, data=data)
        if response.status_code not in valid_codes:
            try:
                error = json.loads(response.content)
            except json.decoder.JSONDecodeError:
                error = f"Server error {response.status_code}"
            raise APIError(error)
        return json.loads(response.content)

    @beartype
    def put(self, url: str, data: str = None, valid_codes: list = [200]):
        """Performs an HTTP PUT request and handles errors.

        Args:
            url (str): URL of the CRIPT node
            data (str, optional): Data payload to POST
            valid_codes (list, optional): Response codes to consider the request a success

        Raises:
            APIError: The response did not contain a valid response code

        Returns:
            response (dict): Response of the PUT request

        ``` py title="Example"
        url = "https://criptapp.org/api/collection/30b17158-45f0-402d-a696-5de5fb172931/"
        response = api.put(
            url=url,
            data=json.dumps({"name": "My edited collection"}),
        )
        ```
        """
        url = convert_to_api_url(url)
        response = self.session.put(url=url, data=data)
        if response.status_code not in valid_codes:
            try:
                error = json.loads(response.content)
            except json.decoder.JSONDecodeError:
                error = f"Server error {response.status_code}"
            raise APIError(error)
        return json.loads(response.content)

    @beartype
    def delete(self, url: str):
        """Performs an HTTP DELETE request and handles errors.

        Args:
            url (str): URL of the CRIPT node

        Raises:
            APIError: The response did not contain a valid response code

        ``` py title="Example"
        url = "https://criptapp.org/api/collection/30b17158-45f0-402d-a696-5de5fb172931/"
        api.delete(url=url)
        ```
        """
        url = convert_to_api_url(url)
        response = self.session.delete(url)
        if response.status_code != 204:
            try:
                error = json.loads(response.content)
            except json.decoder.JSONDecodeError:
                error = f"Server error {response.status_code}"
            raise APIError(error)
