import abc
import json
from logging import getLogger

from cript.api.exceptions import APIError
from cript.cache import get_cached_api_session, get_cached_node
from cript.data_model.paginator import Paginator
from cript.data_model.utils import get_data_model_class

logger = getLogger(__name__)


class Base(abc.ABC):
    """
    The base abstract class for a CRIPT data model object.
    All data model objects inherit from this class (note that this class cannot
    be directly instantiated).
    """

    node_name = None
    alt_names = list()

    def __repr__(self):
        return self._to_json()

    def __str__(self):
        return self._to_json()

    def _to_json(self):
        return json.dumps(self._prep_for_upload(), indent=4)

    @abc.abstractmethod
    def _prep_for_upload(self):
        ...

    def _clean_dict(self):
        """
        Convert a node object to a cleaned dictionary.

        :return: The cleaned dictionary.
        :rtype: dict
        """
        return {
            k.lstrip("_"): self.__getattribute__(k) for k in vars(self) if "__" not in k
        }

    @abc.abstractmethod
    def _add_node(self, node, attr_name):
        ...

    @abc.abstractmethod
    def _remove_node(self, node, attr):
        ...

    def _generate_nested_nodes(self, get_level: int = 1, level: int = 0):
        """
        Generate nested node objects within a given node.

        :param level: Current nested node level.
        :param get_level: Level to recursively get nested nodes.
        """
        if level <= get_level:
            level += 1

        # Limit recursive node generation
        skip_nodes = False
        if level > get_level:
            skip_nodes = True

        node_dict = self.__dict__
        fields_to_skip = {
            "url",
            "_Inventory__index_table",
            "_Inventory__degenerate_index_table",
        }
        for key, value in node_dict.items():
            # Skip empty values and other fields that should be skipped
            if not value or key == "url":
                continue

            elif key == "_Inventory__index_table":
                node_dict[key] = {}
                continue
            elif key == "_Inventory__degenerate_index_table":
                node_dict[key] = set()
                continue

            # Generate nodes
            api = get_cached_api_session()
            if isinstance(value, str) and api.url in value and not skip_nodes:
                # Check if node already exists in memory
                local_node = get_cached_node(value)
                if local_node:
                    node_dict[key] = local_node
                else:
                    node_class = get_data_model_class(key)
                    try:
                        node_dict[key] = node_class.get(
                            url=value, get_level=get_level, level=level
                        )
                    except APIError:
                        # Leave the URL if node is not viewable
                        pass

            # Generate subobjects
            elif isinstance(value, dict):
                subobject_class = get_data_model_class(key)
                subobject = subobject_class(**value)
                node_dict[key] = subobject
                subobject._generate_nested_nodes(get_level=get_level, level=level)

            # Define Paginator attributes
            elif isinstance(value, Paginator):
                value.api = api
                value.obj_class = get_data_model_class(key.lstrip("_"))
                value.get_level = get_level

            # Handle lists
            elif isinstance(value, list):
                for i in range(len(value)):
                    # Generate nodes
                    if (
                        isinstance(value[i], str)
                        and api.url in value[i]
                        and not skip_nodes
                    ):
                        # Check if node already exists in memory
                        local_node = get_cached_node(value[i])
                        if local_node:
                            value[i] = local_node
                        else:
                            node_class = get_data_model_class(key)
                            try:
                                value[i] = node_class.get(
                                    url=value[i], get_level=get_level, level=level
                                )
                            except APIError:
                                # Leave the URL if node is not viewable
                                pass

                    # Generate subobjects
                    elif isinstance(value[i], dict):
                        node_class = get_data_model_class(key)
                        subobject = node_class(**value[i])
                        value[i] = subobject
                        subobject._generate_nested_nodes(
                            get_level=get_level, level=level
                        )
