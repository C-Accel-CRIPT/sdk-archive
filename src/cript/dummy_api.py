import os
import json
import pathlib
import urllib
import glob
from typing import Union
from logging import getLogger

from beartype import beartype
from beartype.typing import Type

from cript import VERSION, NODE_CLASSES
from cript.nodes import Base, User, File
from cript.utils import display_errors
from cript.exceptions import (
    APISaveError,
    APIDeleteError,
    APISearchError,
    APIGetError,
    DuplicateNodeError,
)


logger = getLogger(__name__)


class DummyAPI:
    """The entry point for interacting with the CRIPT API."""

    version = VERSION
    keys = {}

    def __init__(self, folder: str = None):
        """
        Establishes a session with a dummy CRIPT API.
        """
        if not DummyAPI.keys:  # if empty
            DummyAPI._load_keys()

        self.name = "dummy"
        self.folder = folder
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
            with open(file, "r", encoding="UTF-8") as f:
                key_name = pathlib.Path(file).stem.replace("key_", "")
                cls.keys[key_name] = json.load(f)

    @beartype
    def refresh(self, node: Base, max_level: int = 1):
        """
        Overwrite a node's attributes with the latest values from the database.
        """
        raise NotImplementedError

    @beartype
    def save(self, node: Base, max_level: int = 1):
        """
        Create or update a node in the database.

        :param node: The node to be saved.
        :param max_level: Max depth to recursively generate nested nodes.
        """
        if node.node_type == "primary":
            if node.url:
                # Update an existing object via PUT
                response = self.session.put(url=node.url, data=node._to_json())
            else:
                # Create a new object via POST
                response = self.session.post(
                    url=f"{self.api_url}/{node.slug}/", data=node._to_json()
                )
        else:
            raise APISaveError(
                f"The save() method cannot be called on secondary nodes such as {node.node_name}"
            )

        if response.status_code in (200, 201):
            # Handle new file uploads
            if node.slug == "file" and os.path.exists(node.source):
                file_url = response.json()["url"]
                file_uid = response.json()["uid"]
                self._upload_file(file_url, file_uid, node)

            self._set_node_attributes(node, response.json())
            self._generate_nodes(node, max_level=max_level)

            # Update File node source field
            if node.slug == "file":
                self.refresh(node, max_level=max_level)

            logger.info(f"{node.node_name} node has been saved to the database.")

        else:
            try:
                # Raise error if duplicate node is found
                response_dict = json.loads(response.content)
                if "duplicate" in response_dict:
                    response_dict.pop("duplicate")  # Pop flag for display purposes
                    response_content = json.dumps(response_dict)
                    raise DuplicateNodeError(display_errors(response_content))
            except json.decoder.JSONDecodeError:
                pass
            raise APISaveError(display_errors(response.content))

    def _set_node_attributes(self, node, obj_json):
        """
        Set node attributes using data from an API response.

        :param node: The node you want to set attributes for.
        :param obj_json: The JSON representation of the node object.
        """
        for json_key, json_value in obj_json.items():
            setattr(node, json_key, json_value)

    @beartype
    def download(self, node: File, path: str = None):
        """
        Download a file from the defined storage provider.

        :param node: The :class:`File` node object.
        :param path: Path where the file should go.
        """
        storage_provider = self.storage_info["provider"]
        if not path:
            path = f"./{node.name}"

        if storage_provider == "globus":
            self._globus_https_download(node, path)
        elif storage_provider == "s3":
            pass  # Coming soon

    def delete(self, obj: Base, query: dict = None):
        """
        Delete a node in the database and clear it locally.

        :param obj: The node to be deleted itself or its class.
        :param query: A dictionary defining the query parameters (e.g., {"name": "NewMaterial"})
        """
        # Delete with node
        if isinstance(obj, Base):
            if obj.node_type == "primary":
                if obj.url:
                    url = obj.url
                else:
                    raise APIDeleteError(
                        f"This {obj.node_name} node does not exist in the database."
                    )
            else:
                raise APIDeleteError(
                    f"The delete() method cannot be called on secondary nodes such as {obj.node_name}"
                )

        # Delete with URL
        elif isinstance(obj, str):
            url = obj
            if self.api_url not in url:
                raise APIDeleteError("Invalid URL provided.")

        # Delete with search query
        elif issubclass(obj, Base) and isinstance(query, dict):
            results = self.search(node_class=obj, query=query)
            if results.count == 1:
                url = results.current["results"][0]["url"]
            elif results.count < 1:
                raise APIGetError("Your query did not match any existing nodes.")
            elif results.count > 1:
                raise APIGetError("Your query matched more than one node.")
        else:
            raise APIDeleteError(
                "Please enter a node, valid node URL, or a node class and search query."
            )

        response = self.session.delete(url)
        if response.status_code == 204:
            # Check if node exists locally
            # If it does, clear fields to indicate it has been deleted
            local_node = self._get_local_primary_node(url)
            if local_node:
                local_node.url = None
                local_node.uid = None
                local_node.created_at = None
                local_node.updated_at = None
            logger.info("The node has been deleted from the database.")
        else:
            raise APIGetError(display_errors(response.content))

    @beartype
    def search(self, node_class: Type[Base], query: dict = None):
        """
        Send a query to the API and print the results.

        :param node_class: The class of the node type to query for.
        :param query: A dictionary defining the query parameters (e.g., {"name": "NewMaterial"}).
        :return: A :class:`JSONPaginator` object containing the results.
        :rtype: cript.session.JSONPaginator
        """
        if node_class.node_type == "secondary":
            raise APISearchError(
                f"{node_class.node_name} is a secondary node, thus cannot be searched."
            )

        if isinstance(query, dict):
            query_slug = self._generate_query_slug(query)
            response = self.session.get(
                f"{self.api_url}/{node_class.slug}/?{query_slug}"
            )
        elif query is None:
            response = self.session.get(f"{self.api_url}/{node_class.slug}/")
        else:
            raise APISearchError(f"'{query}' is not a valid query.")

        if response.status_code != 200:
            raise APISearchError(display_errors(response.content))
        return JSONPaginator(self.session, response.content)

    def _generate_query_slug(self, query):
        """Generate the query URL slug."""
        slug = ""
        for key in query:
            value = query[key]
            if isinstance(value, str):
                value = urllib.parse.quote(value.encode("utf8"))
            slug += f"{key}={value}&"
        return slug

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
            if self.api_url not in obj:
                raise APIGetError("Please enter a valid node URL.")
            response = self.session.get(obj)
            if response.status_code == 200:
                obj_json = response.json()
            else:
                raise APIGetError("The specified node was not found.")
            # Define node class from URL slug
            node_slug = obj.rstrip("/").rsplit("/")[-2]
            node_class = self._define_node_class(node_slug)

        # Get node with a search query
        elif issubclass(obj, Base) and query:
            results = self.search(node_class=obj, query=query)
            if results.count < 1:
                raise APIGetError("Your query did not match any existing nodes.")
            elif results.count > 1:
                raise APIGetError("Your query mathced more than one node.")
            else:
                obj_json = results.current["results"][0]
                node_class = obj
        else:
            raise APIGetError(
                "Please enter a node URL or a node class with a search query."
            )

        # Return the local node object if it already exists
        # Otherwise, create a new node
        local_node = self._get_local_primary_node(obj_json["url"])
        if local_node:
            return local_node
        else:
            node = self._create_node(node_class, obj_json)
            self._generate_nodes(node, level=level, max_level=max_level)
            return node

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
            if key == "url":
                continue
            # Generate primary nodes
            if isinstance(value, str) and self.api_url in value:
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
                    if isinstance(value[i], str) and self.api_url in value[i]:
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

    def _define_node_class(self, key: str):
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

    def _create_node(self, node_class, obj_json):
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

        # Create node
        node = node_class(**obj_json)

        # Replace comon attributes
        node.url = url
        node.uid = uid
        node.created_at = created_at
        node.updated_at = updated_at

        return node

    def _get_local_primary_node(self, url: str):
        """
        Use a URL to get a primary node object stored in memory.

        :param url: The URL to match against existing node objects.
        :return: The matching object or None.
        :rtype: Union[cript.nodes.Base, None]
        """
        for instance in Base.__refs__:
            if hasattr(instance, "url") and url == instance.url:
                return instance
        return None

