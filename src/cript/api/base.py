from cript import __api_version__


class APIBase:
    """Base API class"""

    api_version = __api_version__
    latest_session = None
