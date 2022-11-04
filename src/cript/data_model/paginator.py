import copy
from typing import Union
from urllib.parse import urlparse
from urllib.parse import urlunparse
from urllib.parse import parse_qs
from urllib.parse import urlencode

from beartype import beartype

from cript.cache import get_cached_api_session
from cript.cache import get_cached_node
from cript.data_model.utils import get_data_model_class
from cript.data_model.utils import create_node
from cript.data_model.exceptions import InvalidPage
from cript.api.exceptions import APIError


class Paginator:
    """
    Paginator for object lists and raw JSON.

    :param url: Query URL
    :param node_name: Name of the relevant node
    :param payload: POST request payload
    :param limit: The max number of items per page.
    :param offset: The starting position of the paginator.
    :param get_level: Level to recursively get nested nodes.
    """

    @beartype
    def __init__(
        self,
        url: str,
        node_name: str,
        payload: Union[str, None] = None,
        limit: Union[int, None] = None,
        offset: Union[int, None] = None,
        get_level: int = 1,
    ):
        self.url = url
        self.api = get_cached_api_session(url)
        self.node_class = get_data_model_class(node_name)
        self.limit = limit
        self.offset = offset
        self.get_level = get_level
        self.payload = payload
        self._raw = None
        self._count = None

    def json(self):
        """
        Get the raw JSON.
        """
        if self.api is None:
            raise AttributeError("The 'api' attribute must be defined.")

        # Return previous raw if nothing changed
        if self._raw:
            return self._raw["results"]

        # Construct URL
        parsed_url = urlparse(self.url)
        parsed_qs = parse_qs(parsed_url.query)
        if self.limit:
            parsed_qs["limit"] = self.limit
        if self.offset:
            parsed_qs["offset"] = self.offset
        query = urlencode(parsed_qs, doseq=True)
        new_parts = list(parsed_url)
        new_parts[4] = query
        self.url = urlunparse(new_parts)

        # Get JSON response
        if self.payload:
            response = self.api.post(self.url, data=self.payload, valid_codes=[200])
        else:
            response = self.api.get(self.url)

        if "results" not in response:
            raise APIError(response)

        self._raw = response
        return self._raw["results"]

    def objects(self):
        """
        Use the current raw JSON to generate a list of objects.
        """
        if self._raw is None:
            self.json()

        objs_json = copy.deepcopy(self._raw["results"])
        obj_list = []
        for obj_json in objs_json:
            # Use the local object if it's in memory
            # Otherwise, create a new object
            local_obj = get_cached_node(obj_json["url"])
            if local_obj:
                obj = local_obj
            else:
                obj = create_node(self.node_class, obj_json)
                obj._generate_nested_nodes(get_level=self.get_level)
            obj_list.append(obj)

        return obj_list

    def next_page(self):
        """
        Flip to the next page.
        """
        if self._raw is None:
            self.json()

        next_url = self._raw["next"]
        if next_url:
            self.url = next_url
            self._raw = None
            self.json()
        else:
            raise InvalidPage("You're currently on the last page.")

    def previous_page(self):
        """
        Flip to the previous page.
        """
        if self._raw is None:
            self.json()

        previous_url = self._raw["previous"]
        if previous_url:
            self.url = previous_url
            self._raw = None
            self.json()
        else:
            raise InvalidPage("You're currently on the first page.")

    def count(self):
        """
        Get the total number of objects.
        """
        if self._raw is None:
            self.json()

        if self._count is None:
            self._count = self._raw["count"]

        return self._count
