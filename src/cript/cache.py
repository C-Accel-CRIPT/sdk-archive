import weakref
from urllib.parse import urlparse

from cript.api.base import APIBase
from cript.api.exceptions import APISessionRequiredError

# Stores all API sessions
api_session_cache = weakref.WeakValueDictionary()

# Stores all nodes
node_cache = weakref.WeakSet()


def cache_api_session(api):
    """
    Adds an API session to the local cache.
    """
    api_session_cache[api.host] = api
    APIBase.latest_session = api


def cache_node(node):
    """
    Adds a node to the local cache.
    """
    node_cache.add(node)


def get_cached_api_session(url: str = None):
    """
    Gets an API object from the local cache using a URL
    or returning the latest established session.
    """
    if url:
        host = urlparse(url).netloc
        api = api_session_cache.get(host)
        if api is None:
            raise APISessionRequiredError
        return api

    # Default to latest session
    return APIBase.latest_session


def get_cached_node(url: str):
    """
    Gets a node from the local cache using it's URL.
    """
    for instance in node_cache:
        if hasattr(instance, "url") and url == instance.url:
            return instance
    return None
