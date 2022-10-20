import json

from cript.exceptions import CRIPTError


def _display_errors(message):
    """
    Prep errors sent from API for display.

    :param message: The error message.
    :return: The error message as a string.
    :rtype: str
    """
    if isinstance(message, str):
        return message

    if "detail" in message:
        message = message["detail"]
    elif "errors" in message:
        message = message["errors"]

    return json.dumps(message, indent=4)


class APIError(CRIPTError):
    """Base CRIPT API exception."""

    def __init__(self, error):
        self.error = error

    def __str__(self):
        return _display_errors(self.error)


class APISessionRequiredError(CRIPTError):
    """Raised when an active API session is required but not yet established."""

    def __init__(self):
        pass

    def __str__(self):
        return "An API session must be established before you can perform this action."
