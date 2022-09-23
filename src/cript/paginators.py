import json


class SearchPaginator:
    """Paginator for JSON content returned from searches."""

    def __init__(self, session, content, payload=None):
        self._session = session
        self.payload = payload
        self.current = content
        self.count = self.current["count"]

    def __repr__(self):
        return json.dumps(self.current, indent=4)

    def __str__(self):
        return json.dumps(self.current, indent=4)

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, value):
        self._current = json.loads(value)

    @property
    def next(self):
        """Flip to the next page."""
        next_url = self.current["next"]
        if next_url:
            response = self._session.post(url=next_url, data=self.payload)
            self.current = response.content
        else:
            raise AttributeError("You've reached the end of the query.")

    @property
    def previous(self):
        """Flip to the previous page."""
        previous_url = self.current["previous"]
        if previous_url:
            response = self._session.post(url=previous_url, data=self.payload)
            self.current = response.content
        else:
            raise AttributeError("You've reached the beginning of the query.")
