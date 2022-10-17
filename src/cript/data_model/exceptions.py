from cript.exceptions import CRIPTError


class UniqueNodeError(CRIPTError):
    """
    Raised when a node is saved using a combination of field
    values that the database enforces as a unique set.
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class UnsavedNodeError(CRIPTError):
    """Raised when an attempt is made to add an unsaved node to another node."""

    def __init__(self, node_name):
        self.name = node_name

    def __str__(self):
        return (
            f"{self.name} nodes must be saved before they can be added to other nodes."
        )


class AddNodeError(CRIPTError):
    """
    Raised when an attempt is made to add an unrelated node.
    e.g., Attempting to add a Condition node to a Collection node.
    """

    def __init__(self, child_node_name, parent_node_name):
        self.child_node_name = child_node_name
        self.parent_node_name = parent_node_name

    def __str__(self):
        return f"{self.child_node_name} nodes cannot be added to {self.parent_node_name} nodes."


class RemoveNodeError(CRIPTError):
    """
    Raised when an attempt is made to remove an unrelated node.
    e.g., Attempting to remove a Condition node from a Collection node.
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class FileSizeLimitError(CRIPTError):
    """Raised when a file size exceeds the defined limit."""

    def __init__(self, max_size):
        self.max_size = max_size

    def __str__(self):
        return f"The file size exceeds the maximum limit of {self.max_size}."


class InvalidPage(CRIPTError):
    """Raised when attempting to get an invalid page via a paginator."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
