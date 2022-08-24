import re
import hashlib
import math
import json
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
    if not path.startswith("/api/"):
        return f"{scheme}://{netloc}/api{path}"
    return url


def auto_assign_group(group, parent):
    """
    Decide whether to inherit the group from a node's parent.
    e.g., Experiment could inherit the group of it's parent Collection.

    :param group: Current value of the node's group field.
    :param parent: The parent node of the relevant node.
    :return: The :class:`Group` object that will be assigned to the node.
    :rtype: cript.nodes.Group
    """
    if parent and not group:
        return parent.group
    return group


def sha256_hash(file_path):
    """
    Generate a SHA256 hash of a file.

    :param file_path: Path to the file.
    :return: SHA256 has of the file.
    :rtype: str
    """
    sha256_hash_ = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash_.update(byte_block)
        return str(sha256_hash_.hexdigest())


def convert_file_size(size_bytes):
    """
    Converts file size from bytes to other units.

    :param size_bytes: Some number of bytes to be converted.
    :return: The converted file size.
    :rtype: str
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


def display_errors(response):
    """
    Prep errors sent from API for display.

    :param response: The API error response.
    :return: The error message as JSON.
    :rtype: str
    """
    try:
        response_dict = json.loads(response)
    except json.decoder.JSONDecodeError:
        return "Server error."

    if "detail" in response_dict:
        ret = response_dict["detail"]
    elif "errors" in response_dict:
        ret = response_dict["errors"]
    else:
        ret = response_dict

    return json.dumps(ret, indent=4)
