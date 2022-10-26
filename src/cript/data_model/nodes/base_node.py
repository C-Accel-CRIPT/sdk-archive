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
    def save(self, get_level: int = 0, update_existing: bool = False):
        """
        Create or update a node in the database.

        :param node: The node to be saved.
        :param get_level: Level to recursively get nested nodes.
        :param update_existing: Indicates whether to update an existing node with the same unique fields.
        """
        api = get_cached_api_session(self.url)

        if self.url:
            # Update an existing object via PUT
            response = api.put(self.url, data=self._to_json(),valid_codes=[200,400])
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
                    self.save(get_level=get_level)
                    return
                else:
                    raise UniqueNodeError(response["errors"][0])

        set_node_attributes(self, response)
        self._generate_nested_nodes(get_level=get_level)
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
    def refresh(self, get_level: int = 0):
        """
        Overwrite a node's attributes with the latest values from the database.

        :param get_level: Level to recursively get nested nodes.
        """
        if self.url is None:
            raise ValueError(
                "Before you can refresh a node, you must either save it or define its URL."
            )

        api = get_cached_api_session(self.url)
        response = api.get(self.url)
        set_node_attributes(self, response)
        self._generate_nested_nodes(get_level=get_level)

    @beartype
    def update(self, get_level: int = 0, **kwargs):
        """
        Updates and immediately saves a node.

        :param get_level: Level to recursively get nested nodes.
        :param **kwargs: Arguments to update the node.
        """
        if self.url is None:
            raise ValueError(
                "Before you can update a node, you must either save it or define its URL."
            )

        set_node_attributes(self, kwargs)
        self.save(get_level=get_level)

    @classmethod
    @beartype
    def create(cls, get_level: int = 0, update_existing: bool = False, **kwargs):
        """
        Immediately creates a node.

        :param get_level: Level to recursively get nested nodes.
        :param update_existing: Indicates whether to update an existing node with the same unique fields.
        :param **kwargs: Arguments for the constructor.
        :return: The created node.
        :rtype: cript.data_model.nodes.BaseNode
        """
        node = cls(**kwargs)
        node.save(get_level=get_level, update_existing=update_existing)
        return node

    @classmethod
    @beartype
    def get(cls, get_level: int = 0, **kwargs):
        """
        Get the JSON for a node and use it to generate a local node object.

        :param get_level: Level to recursively get nested nodes.
        :param **kwargs: Query parameters.
        :return: The generated node object.
        :rtype: cript.data_model.nodes.BaseNode
        """
        level = kwargs.pop("level", 0)

        if len(kwargs) == 0:
            raise AttributeError(f"Query arguments must be provided.")

        api = get_cached_api_session()

        if "url" in kwargs:
            obj_json = api.get(kwargs["url"])
        else:
            results = cls.search(**kwargs)
            count = results.count()
            if count < 1:
                raise ValueError("Your query did not match any existing nodes.")
            elif count > 1:
                raise ValueError("Your query matched more than one node.")
            else:
                obj_json = results.json()[0]

        # Return the local node object if it already exists
        # Otherwise, create a new node
        local_node = get_cached_node(obj_json["url"])
        if local_node:
            return local_node
        else:
            node = create_node(cls, obj_json)
            node._generate_nested_nodes(get_level=get_level, level=level)
            return node

    @classmethod
    @beartype
    def search(
        cls,
        limit: Union[int, None] = None,
        offset: Union[int, None] = None,
        get_level: int = 0,
        **kwargs,
    ):
        """
        Send a query to the API and display the results.

        :param limit: The max number of items to return.
        :param offset: The starting position of the query.
        :param get_level: Level to recursively get nested nodes.
        :param **kwargs: Query parameters.
        :return: A `Paginator` object.
        :rtype: cript.data_model.paginator.Paginator
        """
        if len(kwargs) == 0:
            raise AttributeError(f"Query arguments must be provided.")

        api = get_cached_api_session()
        url = f"{api.search_url}/{cls.slug}/"
        payload = json.dumps(kwargs)
        return Paginator(
            url=url,
            node_name=cls.node_name,
            limit=limit,
            offset=offset,
            get_level=get_level,
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
