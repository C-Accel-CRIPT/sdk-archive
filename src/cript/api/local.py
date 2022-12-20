import datetime
import glob
import json
import os
import pathlib
import shutil
import uuid
from logging import getLogger
from typing import Union

from beartype import beartype

from cript import DATA_MODEL_NAMES
from cript.api.base import APIBase
from cript.api.exceptions import APIError
from cript.api.utils import get_slug_from_url
from cript.cache import api_session_cache
from cript.utils import is_valid_uid

logger = getLogger(__name__)

ENCODING = "UTF-8"


def dict_remove_none(ddict: dict) -> dict:
    """Remove 'key, value' pair form dictionary if value is None or []."""
    _dict = {}
    for k, v in ddict.items():
        if v is None or v == []:
            continue
        elif isinstance(v, dict):
            _dict[k] = dict_remove_none(v)
        elif isinstance(v, list):
            _list = []
            for obj in v:
                if isinstance(obj, dict):
                    obj = dict_remove_none(obj)
                _list.append(obj)
            _dict[k] = _list
        else:
            _dict[k] = v

    return _dict


def _parse_filename(filename: str) -> tuple[str, str]:
    # parsing
    filename = pathlib.Path(filename)
    split = filename.stem.split("_")
    node = split[0]
    uid = split[1]

    # validate
    _validate_node_name(node)
    _validate_uid(uid)

    return node, uid


def _validate_node_name(node: str):
    if node not in DATA_MODEL_NAMES:
        raise ValueError(f"Invalid node: {node}")


def _validate_uid(uid: str):
    if not is_valid_uid(uid):
        raise ValueError(f"Invalid uid: {uid}")


def _get_uid_from_url(url: str):
    return url.rstrip("/").split("/")[-1]


def _format_folder(folder: Union[str, pathlib.Path]) -> pathlib.Path:
    """
    Converts various folder inputs into an absolute pathlib.Path.
    """
    if isinstance(folder, pathlib.Path):
        return folder

    if not isinstance(folder, str):
        raise TypeError(f"'folder' {folder} must be a string or pathlib.Path.")

    if not os.path.isabs(folder):
        folder = os.path.abspath(folder)

    return pathlib.Path(folder)


def make_new_folder(folder: pathlib.Path):
    if not os.path.isdir(folder):
        os.makedirs(folder)


def move_copy_file(
    old_location: Union[pathlib.Path, str], new_location: Union[pathlib.Path, str]
):
    """
    Copies files from one location to a new one
    """
    if not isinstance(old_location, pathlib.Path):
        old_location = pathlib.Path(old_location)
    if not isinstance(new_location, pathlib.Path):
        new_location = pathlib.Path(new_location)
    new_location = new_location.joinpath(old_location.name)
    shutil.copy2(old_location, new_location)


class APILocal(APIBase):
    """
    The entry point for interacting with your local filesystem.

    :param folder: Path to a folder on your local filesystem.
    """

    def __init__(
        self,
        folder: Union[str, pathlib.Path],
        data_folder: Union[str, pathlib.Path] = None,
    ):
        self.url = "http://localhost/api"
        self.host = "localhost"
        # database folder
        self.folder: pathlib.Path = _format_folder(folder)
        make_new_folder(self.folder)
        # data folder
        if data_folder is None:
            data_folder = self.folder.joinpath("data")
        self.data_folder: pathlib.Path = _format_folder(data_folder)
        make_new_folder(self.data_folder)

        self.database_by_node = {}
        self.database_by_uid = {}
        self._load_database()

        logger.info(f"Connection to {self.url} API was successful!")

        # Save session to cache
        api_session_cache[self.host] = self
        APIBase.latest_session = self

    def __repr__(self):
        return f"Connected to {self.url}"

    def __str__(self):
        return f"Connected to {self.url}"

    def _load_database(self):
        """
        Creates a dictionary with available files.
        """
        files = glob.glob(str(self.folder / "*.json"))

        for file in files:
            try:
                node, uid = _parse_filename(file)
            except ValueError:
                logger.warning(
                    f"Unrecognized file found in database and will be skipped. {file}"
                )
                continue

            self.database_by_uid[uid] = file
            if node not in self.database_by_node:
                self.database_by_node[node] = {}
            self.database_by_node[node][uid] = file

    @beartype
    def get(self, url: str):
        """Simulates an HTTP GET request to the local filesystem."""
        uid = _get_uid_from_url(url)
        if uid not in self.database_by_uid:
            raise APIError("The specified node was not found.")

        with open(self.database_by_uid[uid], "r", encoding=ENCODING) as f:
            return json.load(f)

    @beartype
    def post(self, url: str, data: str, *args, **kwargs):
        """Simulates an HTTP POST request to the local filesystem."""
        data_dict = json.loads(data)
        slug = get_slug_from_url(url)
        uid = str(uuid.uuid4())

        # Prep for save
        data_dict["uid"] = uid
        data_dict["url"] = f"{self.url}/{slug}/{uid}/"
        data_dict["updated_at"] = datetime.datetime.now().isoformat()
        data_dict["created_at"] = datetime.datetime.now().isoformat()

        # Save to local filesystem
        file_name = self.folder / f"{slug}_{uid}.json"
        with open(file_name, "w", encoding=ENCODING) as f:
            f.write(data)

        return data_dict

    @beartype
    def put(self, url: str, data: str, *args, **kwargs):
        """Simulates an HTTP PUT request to the local filesystem."""
        data_dict = json.loads(data)
        uid = data_dict["uid"]
        slug = get_slug_from_url(url)

        # Prep for save
        data_dict["updated_at"] = datetime.datetime.now().isoformat()

        # Save to local filesystem
        file_name = self.folder / f"{slug}_{uid}.json"
        with open(file_name, "w", encoding=ENCODING) as f:
            f.write(data)

        return data_dict

    @beartype
    def delete(self, url: str):
        """Simulates an HTTP DELETE request to the local filesystem."""
        uid = _get_uid_from_url(url)
        os.remove(self.database_by_uid[uid])
