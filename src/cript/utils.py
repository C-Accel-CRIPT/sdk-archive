import hashlib
import math
import re


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


def is_valid_uid(string: str) -> bool:
    """Checks if a given string is a valid UID."""
    return (
        len(
            re.findall(
                "^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
                string,
            )
        )
        == 1
    )
