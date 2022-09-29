import json
import copy
from urllib.parse import urlparse
from urllib.parse import urlunparse
from urllib.parse import parse_qs
from urllib.parse import urlencode

from cript.exceptions import InvalidPage


class Paginator:
    """Paginator for object lists and raw JSON."""

    def __init__(
        self,
        url,
        api=None,
        obj_class=None,
        payload=None,
        limit=None,
        offset=None,
        max_level=0,
    ):
        """
        Initializes a Paginator object.

        :param url: Query URL
        :param api: API object instance
        :param obj_class: Relevant class for object generation
        :param limit: The max number of items per page.
        :param offset: The starting position of the paginator.
        :param max_level: Max depth to recursively generate nested primary objects.
        :param payload: POST request payload
        """
        self.url = url
        self.api = api
        self.obj_class = obj_class
        self.limit = limit
        self.offset = offset
        self.max_level = max_level
        self.payload = payload
        self._raw = None
        self._count = None

    def json(self):
        """Get the raw JSON."""
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
            response = self.api.session.post(self.url, data=self.payload)
        else:
            response = self.api.session.get(self.url)

        self._raw = response.json()
        return self._raw["results"]

    def objects(self):
        """Use the current raw JSON to generate a list of objects."""
        if self._raw is None:
            self.json()

        if self.obj_class is None:
            raise AttributeError("The 'obj_class' attribute must be defined.")

        objs_json = copy.deepcopy(self._raw["results"])
        obj_list = []
        for obj_json in objs_json:
            # Use the local object if it's in memory
            # Otherwise, create a new object
            local_obj = self.api._get_local_primary_node(obj_json["url"])
            if local_obj:
                obj = local_obj
            else:
                obj = self.api._create_node(self.obj_class, obj_json)
                self.api._generate_nodes(obj, max_level=self.max_level)
            obj_list.append(obj)

        return obj_list

    def next_page(self):
        """Flip to the next page."""
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
        """Flip to the previous page."""
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
        """Get the total number of objects."""
        if self._raw is None:
            self.json()

        if self._count is None:
            self._count = self._raw["count"]

        return self._count
