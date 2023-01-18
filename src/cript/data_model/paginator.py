import copy
from typing import Union
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from beartype import beartype

from cript.api.exceptions import APIError
from cript.cache import get_cached_api_session, get_cached_node
from cript.data_model.exceptions import InvalidPage
from cript.data_model.utils import create_node, get_data_model_class


class Paginator:
    """
    Paginator for object lists and raw JSON.

    Args:
        url (str): Query URL
        node_name (str): Name of the relevant node
        payload (Union[str, None], optional): POST request payload
        limit (Union[int, None], optional):  The max number of items per page
        offset (Union[int, None], optional): The starting position of the paginator.
        get_level (int, optional): Level to recursively get nested nodes.

    ``` py title="Example"
    paginator = Paginator(
        url="https://criptapp.org/api/collection/?format=json",
        node_name="Collection",
        limit=10,
        offset=0,
        get_level=1,
    )
    ```
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
        """Get the raw JSON response.

        Raises:
            AttributeError: If the API object is not defined
            APIError: If no results are returned

        Returns:
            results (list): The list of results


        ``` py title="Example"
        json_results = paginator.json()
        ```
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
        """Use the current raw JSON to generate a list of objects.

        Returns:
            results (list): The list of results

        ``` py title="Example"
        objects = paginator.objects()
        ```
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
        """Flip to the next page.

        Raises:
            InvalidPage: You are already viewing the last page

        ```py title="Example"
        paginator.next_page()
        ```
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
        """Flip to the previous page.

        Raises:
            InvalidPage: You are already viewing the first page

        ```py title="Example"
        paginator.previous_page()
        ```
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
        """Get the total number of objects.

        Returns:
            count (int): The number of returned results

        ```py title="Example"
        count = paginator.count()
        ```
        """
        if self._raw is None:
            self.json()

        if self._count is None:
            self._count = self._raw["count"]

        return self._count
