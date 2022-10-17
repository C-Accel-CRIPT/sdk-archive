import abc
import copy
import json
from logging import getLogger
from typing import Union
from urllib.parse import urlparse

from beartype import beartype

from cript.data_model.base import Base
from cript.data_model.paginator import Paginator
from cript.cache import cache_node
from cript.cache import get_cached_api_session
from cript.cache import get_cached_node
from cript.utils import is_valid_uid
from cript.data_model.utils import set_node_attributes
from cript.data_model.utils import create_node
from cript.data_model.exceptions import UniqueNodeError
from cript.data_model.exceptions import UnsavedNodeError
from cript.data_model.exceptions import AddNodeError
from cript.data_model.exceptions import RemoveNodeError


logger = getLogger(__name__)


class BaseNode(Base, abc.ABC):
    slug = None

    def __init__(
        self,
        url: str = None,
        uid: str = None,
        public: bool = False,
        created_at: str = None,
        updated_at: str = None,
    ):
        super().__init__()
        self.url = url
        self.uid = uid
        self.public = public
        self.created_at = created_at
        self.updated_at = updated_at

        # Add node to cache
        cache_node(self)

    @beartype
    def save(self, max_level: int = 0, update_existing: bool = False, api=None):
        """
        Create or update a node in the database.

        :param node: The node to be saved.
        :param max_level: Max depth to recursively generate nested nodes.
        :param update_existing: Indicates whether to update an existing node with the same unique fields.
        """
        api = get_cached_api_session(self.url)

        if api.host == "localhost":
            response = api.save_file(self)
        elif self.url:
            # Update an existing object via PUT
            response = api.put(self.url, data=self._to_json())
        else:
            # Create a new object via POST
            response = api.post(
                url=f"{api.url}/{self.slug}/",
                data=self._to_json(),
                valid_codes=[201, 400],
            )

            # Check if a unique error was returned
            if "unique" in response:
                unique_url = response.pop("unique")
                if unique_url and update_existing == True:
                    # Update existing unique node
                    self.url = unique_url
                    self.save(max_level=max_level, api=api)
                    return
                else:
                    raise UniqueNodeError(response["errors"][0])

        set_node_attributes(self, response)
        self._generate_nested_nodes(max_level=max_level)
        logger.info(f"{self.node_name} node has been saved to the database.")

    @beartype
    def delete(self):
        """
        Delete a node in the database and clear it locally.
        """
        if not self.url:
            raise ValueError(
                f"This {self.node_name} node does not exist in the database."
            )

        api = get_cached_api_session(self.url)
        api.delete(self.url)
        self.url = None
        self.uid = None
        self.created_at = None
        self.updated_at = None
        logger.info("The node has been deleted from the database.")

    @beartype
    def refresh(self, max_level: int = 0):
        """
        Overwrite a node's attributes with the latest values from the database.

        :param max_level: Max depth to recursively generate nested nodes.
        """
        if self.url is None:
            raise ValueError(
                "Before you can refresh a node, you must either save it or define its URL."
            )

        api = get_cached_api_session(self.url)
        response = api.get(self.url)
        set_node_attributes(self, response)
        self._generate_nested_nodes(max_level=max_level)

    @beartype
    def update(self, max_level: int = 0, **kwargs):
        """
        Update and and immediately save a node.

        :param max_level: Max depth to recursively generate nested nodes.
        """
        if self.url is None:
            raise ValueError(
                "Before you can update a node, you must either save it or define its URL."
            )

        set_node_attributes(self, kwargs)
        self.save(max_level=max_level)

    @classmethod
    @beartype
    def create(
        cls, max_level: int = 0, update_existing: bool = False, api=None, **kwargs
    ):
        """
        Immediately creates a node.

        :param max_level: Max depth to recursively generate nested nodes.
        :param update_existing: Indicates whether to update an existing node with the same unique fields.
        """
        node = cls(**kwargs)
        node.save(max_level=max_level, update_existing=update_existing, api=api)
        return node

    @classmethod
    @beartype
    def get(cls, query: Union[str, dict], level: int = 0, max_level: int = 0):
        """
        Get the JSON for a node and use it to generate a local node object.

        :param query: The node's URL, UID, or a query.
        :param level: Current nested node level.
        :param max_level: Max depth to recursively generate nested nodes.
        :return: The generated node object.
        :rtype: cript.nodes.BaseNode
        """
        if isinstance(query, str):
            if is_valid_uid(query):
                api = get_cached_api_session()
                # Get node with UID
                if api.host == "localhost":
                    obj_json = api.get_file(query)
                else:
                    query = f"{api.url}/{cls.slug}/{query}/"
                    obj_json = api.get(query)
            else:
                # Get node with a URL
                api = get_cached_api_session(query)
                host = urlparse(query).netloc
                if host != api.host:
                    raise ValueError("Invalid URL")
                obj_json = api.get(query)

        # Get node with a search query
        elif isinstance(query, dict):
            api = get_cached_api_session()
            results = cls.search(query=query)
            count = results.count()
            if count < 1:
                raise ValueError("Your query did not match any existing nodes.")
            elif count > 1:
                raise ValueError("Your query matched more than one node.")
            else:
                obj_json = results.json()[0]

        else:
            raise TypeError("Please enter a valid node URL, UID or search query.")

        # Return the local node object if it already exists
        # Otherwise, create a new node
        local_node = get_cached_node(obj_json["url"])
        if local_node:
            return local_node
        else:
            node = create_node(cls, obj_json)
            node._generate_nested_nodes(level=level, max_level=max_level)
            return node

    @classmethod
    @beartype
    def search(
        cls,
        query: dict,
        limit: Union[int, None] = None,
        offset: Union[int, None] = None,
        max_level: int = 0,
    ):
        """
        Send a query to the API and display the results.

        :param query: A dictionary defining the query parameters (e.g., {"name": "NewMaterial"}).
        :param limit: The max number of items to return.
        :param offset: The starting position of the query.
        :param max_level: Max depth to recursively generate nested nodes.
        :return: A `Paginator` object.
        :rtype: cript.paginator.Paginator
        """
        if not isinstance(query, dict):
            raise TypeError(f"Query must be a dict, not {type(query)}")

        if isinstance(query, dict):
            api = get_cached_api_session()
            url = f"{api.search_url}/{cls.slug}/"
            payload = json.dumps(query)
            return Paginator(
                url=url,
                node_name=cls.node_name,
                limit=limit,
                offset=offset,
                max_level=max_level,
                payload=payload,
            )

    def _to_json(self):
        node_dict = copy.deepcopy(self._clean_dict())

        for key, value in node_dict.items():
            if isinstance(value, Paginator):
                node_dict[key] = value.url
            elif hasattr(value, "_prep_for_upload"):
                node_dict[key] = value._prep_for_upload()
            elif isinstance(value, list):
                for i in range(len(value)):
                    if hasattr(value[i], "_prep_for_upload"):
                        value[i] = value[i]._prep_for_upload()

        return json.dumps(node_dict, indent=4)

    def _prep_for_upload(self, first: bool = False):
        """
        Convert a node into a dict that can be sent to the API.

        :return: The converted dict.
        :rtype: dict
        """
        # Check if node has been saved
        if self.url is None:
            raise UnsavedNodeError(self.node_name)
        return self.url

    def _add_node(self, node: Base, attr_name: str):
        """
        Append a node to another node's list attribute.

        :param node: The node that will be appended.
        :param attr_name: The name of the list attribute (e.g., conditions).
        """
        if isinstance(node, BaseNode) and node.url is None:
            raise UnsavedNodeError(node.node_name)

        if hasattr(self, attr_name):
            getattr(self, attr_name).append(node)
        else:
            raise AddNodeError(node.node_name, self.node_name)

    def _remove_node(self, node: Base, attr: str):
        """
        Remove a node from another node's list attribute.

        :param node: The node that will be removed or it's position in the list.
        :param attr: The name of the list attribute (e.g., conditions).
        """
        if not hasattr(self, attr):
            raise RemoveNodeError(f"The node does not have attribute: {attr}")

        attribute = getattr(self, attr)

        if isinstance(node, int) and 0 < node <= len(attribute):
            attribute.pop(node)
        elif isinstance(node, BaseNode):
            if isinstance(attribute[0], str):
                # node attributes may be list[URL]
                attribute.remove(node.url)
            else:
                # node attributes may be list[BaseNode]
                attribute.remove(node)
        elif isinstance(node, Base):
            # for BaseSubobject
            attribute.remove(node)
        else:
            raise RemoveNodeError(
                f"{self.node_name} nodes do not contain {node.node_name} nodes."
            )
