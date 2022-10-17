import os
import shutil
import re
import json
import pathlib
import glob
import uuid
import datetime
from typing import Union
from logging import getLogger

from beartype import beartype
from beartype.typing import Type

from cript import DATA_MODEL_NAMES
from cript.api.base import APIBase
from cript.api.exceptions import APIError
from cript.cache import api_session_cache
from cript.data_model.base import Base
from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.file import File
from cript.data_model.subobjects.base_subobject import BaseSubobject
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


def _generate_file_name(node: BaseNode) -> str:
    return f"{node.slug}_{node.uid}"


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


def _format_folder(folder: Union[str, pathlib.Path]) -> pathlib.Path:
    """
    Converts various folder inputs into an absolute pathlib.Path.
    """
    if isinstance(folder, pathlib.Path):
        return folder

    if not isinstance(folder, str):
        raise TypeError(f"'folder' must be a string or pathlib.Path.")

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
    """The entry point for interacting with a local CRIPT API."""

    def __init__(
        self,
        folder: Union[str, pathlib.Path],
        data_folder: Union[str, pathlib.Path] = None,
    ):
        """
        Establishes a session with a local CRIPT API.
        """
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
    def save_file(self, node: BaseNode):
        node.group = "N/A"
        if node.url:
            node.updated_at = datetime.datetime.now().isoformat()
        else:
            node.uid = str(uuid.uuid4())
            node.url = str(f"{self.url}/{node.slug}/{node.uid}/")
            node.updated_at = datetime.datetime.now().isoformat()
            node.created_at = datetime.datetime.now().isoformat()

        # Save to local filesystem
        file_name = self.folder / (_generate_file_name(node) + ".json")
        with open(file_name, "w", encoding=ENCODING) as f:
            f.write(node._to_json())
        logger.info(
            f"Update: {node.node_name}({node.uid}) node has been updated in the database."
        )

        # Add node to database list
        self.database_by_uid[node.uid] = node
        if node.slug not in self.database_by_node:
            self.database_by_node[node.slug] = {node.uid: file_name}
        else:
            self.database_by_node[node.slug][node.uid] = file_name

        return vars(node)

    @beartype
    def delete_file(self, node: BaseNode):
        os.remove(self.database_by_uid[node.uid])

    @beartype
    def get_file(self, uid: str):
        _validate_uid(uid)
        if uid not in self.database_by_uid:
            raise APIError("The specified node was not found.")

        with open(self.database_by_uid[uid], "r", encoding=ENCODING) as f:
            return json.load(f)