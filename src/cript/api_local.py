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

from cript import NODE_CLASSES, NODE_NAMES, __data_model_version__
from cript.nodes.base import Base
from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes.primary.file import File
from cript.nodes.secondary.base_secondary import BaseSecondary
from cript.exceptions import (
    APISaveError,
    APIDeleteError,
    APISearchError,
    APIGetError,
)

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


def _generate_file_name(node: BasePrimary) -> str:
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
    if node not in NODE_NAMES:
        raise ValueError(f"Invalid node: {node}")


def _validate_uid(uid: str):
    if not _validate_uid_bool(uid):
        raise ValueError(f"Invalid uid: {uid}")


def _validate_uid_bool(uid: str) -> bool:
    return len(re.findall("^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$", uid)) == 1


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


def move_copy_file(old_location: Union[pathlib.Path, str], new_location: Union[pathlib.Path, str]):
    """
    Copies files from one location to a new one
    """
    if not isinstance(old_location, pathlib.Path):
        old_location = pathlib.Path(old_location)
    if not isinstance(new_location, pathlib.Path):
        new_location = pathlib.Path(new_location)
    new_location = new_location.joinpath(old_location.name)
    shutil.copy2(old_location, new_location)


def prepare_node_for_saving(node: BasePrimary, version: str) -> BasePrimary:
    node.uid = str(uuid.uuid4())
    node.url = str(f"local://cript/{node.slug}/{node.uid}/")
    node.updated_at = datetime.datetime.now().isoformat()
    node.created_at = datetime.datetime.now().isoformat()
    node.model_version = version

    # automatically assign group base on project node
    if hasattr(node, "project") and hasattr(node, "group"):
        if node.project is None:
            raise ValueError(f"{node.node_name} needs project to be defined.")

        if node.group is None:
            node.group = node.project.group

    return node


class APILocal:
    """The entry point for interacting with the CRIPT API."""

    version = __data_model_version__
    keys = {}

    def __init__(self, folder: Union[str, pathlib.Path], data_folder: Union[str, pathlib.Path] = None):
        """
        Establishes a session with a dummy CRIPT API.
        """
        if not APILocal.keys:  # if empty
            APILocal._load_keys()

        self.name = "local"
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
        logger.info(f"Connection to {self.name} API was successful!")

    def __repr__(self):
        return f"Connected to {self.name}"

    def __str__(self):
        return f"Connected to {self.name}"

    @classmethod
    def _load_keys(cls):
        """
        Load keys from file
        """
        key_files = glob.glob(str(pathlib.Path(__file__).parent) + "\\local_data\\key_*.json")
        for file in key_files:
            with open(file, "r", encoding=ENCODING) as f:
                key_name = pathlib.Path(file).stem.replace("key_", "")
                cls.keys[key_name] = json.load(f)

    def _load_database(self):
        """
        Creates a dictionary with available files.
        """
        files = glob.glob(str(self.folder / "*.json"))

        for file in files:
            try:
                node, uid = _parse_filename(file)
            except ValueError:
                logger.warning(f"Unrecognized file found in database and will be skipped. {file}")
                continue

            self.database_by_uid[uid] = file
            if node not in self.database_by_node:
                self.database_by_node[node] = {}
            self.database_by_node[node][uid] = file

    @beartype
    def save(self, node: BasePrimary, max_level: int = 1):
        """
        Create or update a node in the database.

        :param node: The node to be saved.
        :param max_level: Max depth to recursively generate nested nodes.
        """
        if not isinstance(node, BasePrimary):
            raise APISaveError(f"The save() method cannot be called on secondary nodes such as {node.node_name}")

        if node.uid:
            # update
            if node.uid in self.database_by_uid:
                node.updated_at = datetime.datetime.now().isoformat()
                self._do_save(node)
            else:
                raise APISaveError(f"The node you are saving has a uid, but it is not in the database, "
                                   f"so it can't be updated. {node.node_name}")
        else:
            # save
            node = prepare_node_for_saving(node, self.version)
            file_name = self._do_save(node)

            # add node to api database list
            self.database_by_uid[node.uid] = node
            if node.slug not in self.database_by_node:
                self.database_by_node[node.slug] = {node.uid: file_name}
            else:
                self.database_by_node[node.slug][node.uid] = file_name

        if isinstance(node, File) and os.path.exists(node.source):
            move_copy_file(node.source, self.data_folder)

    def _do_save(self, node: BasePrimary):
        file_name = self.folder / (_generate_file_name(node) + ".json")
        with open(file_name, "w", encoding=ENCODING) as f:
            f.write(node._to_json())
        logger.info(f"Update: {node.node_name}({node.uid}) node has been updated in the database.")

        return file_name

    @beartype
    def refresh(self, node: Base, max_level: int = 1):
        """
        Overwrite a node's attributes with the latest values from the database.
        """
        raise NotImplementedError

    @beartype
    def download(self, node: File, path: str = None):
        """
        Download a file from the defined storage provider.

        :param node: The :class:`File` node object.
        :param path: Path where the file should go.
        """
        raise NotImplementedError

    def delete(self, obj: Union[BasePrimary, str, type], query: dict = None):
        """
        Delete a node in the database and clear it locally.

        :param obj: The node to be deleted itself or its class.
        :param query: A dictionary defining the query parameters (e.g., {"name": "NewMaterial"})
        """
        # Delete with node
        if isinstance(obj, BaseSecondary):
            raise APIDeleteError(
                f"The delete() method cannot be called on secondary nodes such as {obj.node_name}"
            )

        # Delete with node
        if isinstance(obj, BasePrimary):
            if obj.uid:
                uid = obj.uid
            else:
                raise APIDeleteError(f"This {obj.node_name} node has not been saved to the database.")

        # Delete with UID
        elif isinstance(obj, str):
            uid = obj
            if _validate_uid_bool:
                raise APIDeleteError(f"Invalid URL provided. '{uid}'")
            if uid not in self.database_by_uid:
                raise APIDeleteError(f"UID not found in database. '{uid}'")

        # Delete with search query
        elif issubclass(obj, BasePrimary) and isinstance(query, dict):
            raise NotImplementedError
        else:
            raise APIDeleteError("Please enter a node, valid node URL, or a node class and search query.")

        # delete the file
        os.remove(self.database_by_uid[uid])

    @beartype
    def search(self, node_class: Type[Base], query: dict = None):
        """
        Send a query to the API and print the results.

        :param node_class: The class of the node type to query for.
        :param query: A dictionary defining the query parameters (e.g., {"name": "NewMaterial"}).
        :return: A :class:`JSONPaginator` object containing the results.
        :rtype: cript.session.JSONPaginator
        """
        if not isinstance(node_class, BasePrimary):
            raise APISearchError(f"{node_class.node_name} is a secondary node, thus cannot be searched.")

        raise NotImplementedError

    @beartype
    def get(
            self,
            obj: Union[str, Type[Base]],
            query: dict = None,
            level: int = 0,
            max_level: int = 1,
    ):
        """
        Get the JSON for a node and use it to generate a local node object.

        :param obj: The node's URL or class type.
        :param query: Search query if obj argument is a class type.
        :param level: Current nested node level.
        :param max_level: Max depth to recursively generate nested nodes.
        :return: The generated node object.
        :rtype: cript.nodes.Base
        """
        # Get node with a URL
        if isinstance(obj, str):
            obj_json, node_class = self._get_by_uid(obj)

        # Get node with a search query
        elif issubclass(obj, BasePrimary) and query:
            raise NotImplementedError
            # results = self.search(node_class=obj, query=query)
        else:
            raise APIGetError("Please enter a node UID.")  # or a node class with a search query

        # Return the local node object if it already exists
        # Otherwise, create a new node
        local_node = self._get_local_primary_node(obj_json["uid"])
        if local_node:
            return local_node
        else:
            node = self._create_node(node_class, obj_json)
            self._generate_nodes(node, level=level, max_level=max_level)
            return node

    def _get_by_uid(self, obj) -> tuple[dict, BasePrimary]:
        _validate_uid(obj)
        if obj not in self.database_by_uid:
            raise APIGetError("The specified node was not found.")

        with open(self.database_by_uid[obj], 'r', encoding=ENCODING) as f:
            obj_json = json.load(f)

        node_class = self._define_node_class(_parse_filename(self.database_by_uid[obj])[0])

        return obj_json, node_class

    def _generate_nodes(self, node: Base, level: int = 0, max_level: int = 1):
        """
        Generate nested node objects within a given node.

        :param node: The parent node.
        :param level: Current nested node level.
        :param max_level: Max depth to recursively generate nested nodes.
        """
        if level <= max_level:
            level += 1

        # Limit recursion to one level
        if level > max_level:
            return

        node_dict = node.__dict__
        for key, value in node_dict.items():
            # Skip the url field
            if key in ("url", "uid"):
                continue
            # Generate primary nodes
            if isinstance(value, str) and _validate_uid_bool(value):
                # Check if node already exists in memory
                local_node = self._get_local_primary_node(value)
                if local_node:
                    node_dict[key] = local_node
                else:
                    try:
                        node_dict[key] = self.get(
                            value, level=level, max_level=max_level
                        )
                    except APIGetError:
                        # Leave the URL if node is not viewable
                        pass
            # Generate secondary nodes
            elif isinstance(value, dict):
                node_class = self._define_node_class(key)
                secondary_node = node_class(**value)
                node_dict[key] = secondary_node
                self._generate_nodes(secondary_node, level=level, max_level=max_level)
            # Handle lists
            elif isinstance(value, list):
                for i in range(len(value)):
                    # Generate primary nodes
                    if isinstance(value[i], str) and _validate_uid_bool(value[i]):
                        # Check if node already exists in memory
                        local_node = self._get_local_primary_node(value[i])
                        if local_node:
                            value[i] = local_node
                        else:
                            try:
                                value[i] = self.get(
                                    value[i], level=level, max_level=max_level
                                )
                            except APIGetError:
                                # Leave the URL if node is not viewable
                                pass
                    # Generate secondary nodes
                    elif isinstance(value[i], dict):
                        node_class = self._define_node_class(key)
                        secondary_node = node_class(**value[i])
                        value[i] = secondary_node
                        self._generate_nodes(
                            secondary_node, level=level, max_level=max_level
                        )

    @staticmethod
    def _define_node_class(key: str):
        """
        Find the correct class associated with a given key.

        :param key: The key string indicating the class.
        :return: The correct node class.
        :rtype: cript.nodes.Base
        """
        for node_cls in NODE_CLASSES:
            # Use node slug
            if hasattr(node_cls, "slug") and node_cls.slug == key:
                return node_cls
            # Use node list name (e.g., properties)
            if hasattr(node_cls, "list_name") and node_cls.list_name == key:
                return node_cls
        return None

    @staticmethod
    def _create_node(node_class, obj_json):
        """
        Create a node with JSON returned from the API.

        :param node_class: The class of the node to be created.
        :param obj_json: The JSON representation of the node object.
        :return: The created node.
        :rtype: cript.nodes.Base
        """
        # Pop common attributes
        url = obj_json.pop("url")
        uid = obj_json.pop("uid")
        created_at = obj_json.pop("created_at")
        updated_at = obj_json.pop("updated_at")
        model_version = obj_json.pop("model_version")

        # Create node
        node = node_class(**obj_json)

        # Replace common attributes
        node.url = url
        node.uid = uid
        node.created_at = created_at
        node.updated_at = updated_at
        node.model_version = model_version

        return node

    @staticmethod
    def _get_local_primary_node(uid: str):
        """
        Use a URL to get a primary node object stored in memory.

        :param uid: The URL to match against existing node objects.
        :return: The matching object or None.
        :rtype: Union[cript.nodes.Base, None]
        """
        for instance in Base.__refs__:
            if hasattr(instance, "uid") and uid == instance.uid:
                return instance
        return None
