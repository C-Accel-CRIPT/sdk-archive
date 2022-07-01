import abc
import copy
import json

from cript.exceptions import UnsavedNodeError, AddNodeError, RemoveNodeError
from cript.nodes.base import Base


class BasePrimary(Base, abc.ABC):
    slug = None
    source = None
    required = None
    unique_together = None

    def __init__(
            self):
        super().__init__()
        self.url = None
        self.uid = None

    def _to_json(self):
        node_dict = copy.deepcopy(self._clean_dict())
        for key, value in node_dict.items():
            if hasattr(value, "_prep_for_upload"):
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
        # Check if primary node has been saved
        if self.url is None:
            raise UnsavedNodeError(self.node_name)
        return self.url

    def _add_node(self, node: Base, attr_name: str):
        """
        Append a node to another node's list attribute.

        :param node: The node that will be appended.
        :param attr_name: The name of the list attribute (e.g., conditions).
        """
        if isinstance(node, BasePrimary) and node.url is None:
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
        elif isinstance(node, BasePrimary):
            if isinstance(attribute[0], str):
                # primary node attributes may be list[URL]
                attribute.remove(node.url)
            else:
                # primary nodes attributes may be list[BasePrimary]
                attribute.remove(node)
        elif isinstance(node, Base):
            # for BaseSecondary
            attribute.remove(node)
        else:
            raise RemoveNodeError(f"{self.node_name} nodes do not contain {node.node_name} nodes.")
