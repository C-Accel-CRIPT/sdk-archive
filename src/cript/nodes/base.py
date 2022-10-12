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

    def __init__(self):
        self.__refs__.add(self)  # Add instance to __refs__

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
