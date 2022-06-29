import json
import abc
from weakref import WeakSet
from logging import getLogger


logger = getLogger(__name__)


class Base(abc.ABC):
    """
    The base abstract class for a CRIPT node.
    All nodes inherit from this class (note that this class cannot be directly
    instantiated).
    """

    __refs__ = WeakSet()  # Stores all node instances in memory

    node_name = None
    list_name = None
    required = None

    def __init__(self):
        self.__refs__.add(self)  # Add instance to __refs__

    def __repr__(self):
        return self._to_json()

    def __str__(self):
        return self._to_json()

    def print_json(self):
        print(self._to_json())

    def _to_json(self):
        return json.dumps(self._prep_for_upload(), indent=4)

    @abc.abstractmethod
    def _prep_for_upload(self):
        ...

    # def _prep_for_upload(self):
    #     """
    #     Convert a node into a dict that can be sent to the API.
    #
    #     :return: The converted dict.
    #     :rtype: dict
    #     """
    #     node_dict = copy.deepcopy(self._clean_dict())
    #     for key, value in node_dict.items():
    #         # Check if the value is a node
    #         if isinstance(value, Base):
    #             if value.node_type == "primary":
    #                 # Check if primary node has been saved
    #                 if value.url is None:
    #                     raise UnsavedNodeError(value.node_name)
    #                 node_dict[key] = value.url
    #             elif value.node_type == "secondary":
    #                 node_dict[key] = value._prep_for_upload()
    #         elif isinstance(value, list):
    #             for i in range(len(value)):
    #                 if isinstance(value[i], Base):
    #                     if value[i].node_type == "primary":
    #                         # Check if primary node has been saved
    #                         if value[i].url is None:
    #                             raise UnsavedNodeError(value[i].node_name)
    #                         value[i] = value[i].url
    #                     elif value[i].node_type == "secondary":
    #                         value[i] = value[i]._prep_for_upload()
    #     return node_dict

    def _clean_dict(self):
        """
        Convert a node object to a cleaned dictionary.

        :return: The cleaned dictionary.
        :rtype: dict
        """
        return {k.lstrip("_"): self.__getattribute__(k) for k in vars(self)}

    @abc.abstractmethod
    def _add_node(self, node, attr_name):
        ...

    @abc.abstractmethod
    def _remove_node(self, node, attr):
        ...

    # def _add_node(self, node, attr_name):
    #     """
    #     Append a node to another node's list attribute.
    #
    #     :param node: The node that will be appended.
    #     :param attr_name: The name of the list attribute (e.g., conditions).
    #     """
    #     if node.node_type == "primary" and node.url is None:
    #         raise UnsavedNodeError(node.node_name)
    #     elif hasattr(self, attr_name):
    #         getattr(self, attr_name).append(node)
    #     else:
    #         raise AddNodeError(node.node_name, self.node_name)
    #
    # def _remove_node(self, node, attr):
    #     """
    #     Remove a node from another node's list attribute.
    #
    #     :param node: The node that will be removed or it's position in the list.
    #     :param attr: The name of the list attribute (e.g., conditions).
    #     """
    #     if isinstance(node, int):
    #         getattr(self, attr).pop(node)
    #     elif hasattr(self, attr):
    #         if node.node_type == "primary":
    #             getattr(self, attr).remove(node.url)
    #         elif node.node_type == "secondary":
    #             getattr(self, attr).remove(node)
    #     else:
    #         raise RemoveNodeError(node.node_name, self.node_name)
