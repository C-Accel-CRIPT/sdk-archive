class APIAuthError(Exception):
    """Raised for errors with API authentication."""

    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error


class APIRefreshError(Exception):
    """Raised for errors with refreshing a nodes attribute values."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class APISaveError(Exception):
    """Raised for errors when saving a node to the database."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class APIDeleteError(Exception):
    """Raised for errors when deleting a node to the database."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class APISearchError(Exception):
    """Raised for errors when sending search query."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class APIGetError(Exception):
    """Raised for errors when getting an object from the API."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class UnsavedNodeError(Exception):
    """Raised when an attempt is made to add an unsaved node to another node."""

    def __init__(self, node_name):
        self.name = node_name

    def __str__(self):
        return (
            f"{self.name} nodes must be saved before they can be added to other nodes."
        )


class AddNodeError(Exception):
    """
    Raised when an attempt is made to add an unrelated node.
    e.g., Attempting to add a Condition node to a Collection node.
    """

    def __init__(self, child_node_name, parent_node_name):
        self.child_node_name = child_node_name
        self.parent_node_name = parent_node_name

    def __str__(self):
        return f"{self.child_node_name} nodes cannot be added to {self.parent_node_name} nodes."


class RemoveNodeError(Exception):
    """
    Raised when an attempt is made to remove an unrelated node.
    e.g., Attempting to remove a Condition node from a Collection node.
    """

    def __init__(self, child_node_name, parent_node_name):
        self.child_node_name = child_node_name
        self.parent_node_name = parent_node_name

    def __str__(self):
        return f"{self.parent_node_name} nodes do not contain {self.child_node_name} nodes."
