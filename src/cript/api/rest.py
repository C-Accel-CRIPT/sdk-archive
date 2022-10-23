import warnings
import json
from getpass import getpass
from logging import getLogger
from distutils.version import StrictVersion
from urllib.parse import urlparse

import requests
from beartype import beartype

from cript.api.base import APIBase
from cript.data_model.nodes.user import User
from cript.data_model.utils import create_node
from cript.cache import cache_api_session
from cript.api.utils import get_api_url
from cript.api.utils import convert_to_api_url
from cript.storage_clients import GlobusClient
from cript.storage_clients import AmazonS3Client
from cript.api.exceptions import APIError
from cript.api.exceptions import _display_errors
from cript.api.exceptions import UniqueNodeError


logger = getLogger(__name__)


class API(APIBase):
    """The entry point for interacting with the CRIPT API."""

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
        response = self.session.get(f"{self.url}/session-info/")
        if response.status_code == 200:
            response_json = response.json()
            self.latest_api_version = response_json["latest_version"]
            self.user = create_node(User, response.json()["user_info"])
            self.storage_info = response.json()["storage_info"]
            self.vocab = response.json().get("vocab")
        elif response.status_code == 404:
            raise APIError("Please provide a valid host.")
        else:
            raise APIError(response.content)

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
        """Performs an HTTP GET request and handles errors."""
        url = convert_to_api_url(url)
        response = self.session.get(url=url)
        if response.status_code != 200:
            raise APIError("The specified node was not found.")
        return json.loads(response.content)

    @beartype
    def post(self, url: str, data: str = None, valid_codes: list = [201]):
        """Performs an HTTP POST request and handles errors."""
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
    def put(self, url: str, data: str = None):
        """Performs an HTTP PUT request and handles errors."""
        url = convert_to_api_url(url)
        response = self.session.put(url=url, data=data)
        if response.status_code != 200:
            try:
                # Check if a duplicate error was returned
                response_dict = json.loads(response.content)
                if "duplicate" in response_dict:
                    duplicate_url = response_dict.pop("duplicate")
                    if duplicate_url is not None:
                        # Update existing duplicate node
                        self.url = duplicate_url
                        self.save()
                        return
                    else:
                        response_content = json.dumps(response_dict)
                        raise UniqueNodeError(_display_errors(response_content))
            except json.decoder.JSONDecodeError:
                error = f"Server error {response.status_code}"
                raise APIError(error)

        return json.loads(response.content)

    @beartype
    def delete(self, url: str):
        """Performs an HTTP DELETE request and handles errors."""
        url = convert_to_api_url(url)
        response = self.session.delete(url)
        if response.status_code != 204:
            try:
                error = json.loads(response.content)
            except json.decoder.JSONDecodeError:
                error = f"Server error {response.status_code}"
            raise APIError(error)
