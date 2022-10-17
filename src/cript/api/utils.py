import re
from urllib.parse import urlparse


def get_api_url(host: str, tls: bool = True):
    """
    Clean the hostname provided by the user and generate a URL.

    :param host: Hostname of the CRIPT endpoint.
    :param tls: Indicates whether to use TLS encryption for the API connection.
    :return: The API URL that will be used to connect.
    :rtype: str
    """
    host = re.sub("https://|http://", "", host).rstrip("/")
    if tls:
        protocol = "https"
    else:
        protocol = "http"
    return f"{protocol}://{host}/api"


def convert_to_api_url(url: str):
    """
    Convert a UI URL to an API URL.
    e.g., https://criptapp.org/material/ --> https://criptapp.org/api/material/

    :param url: The original UI URL that will be converted.
    :return: The converted API URL.
    :rtype: str
    """
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    netloc = parsed_url.netloc
    path = parsed_url.path

    # Return original URL if in correct format
    if path.startswith("/api/"):
        return url

    return f"{scheme}://{netloc}/api{path}"
