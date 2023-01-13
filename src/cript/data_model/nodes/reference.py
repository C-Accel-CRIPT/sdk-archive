from logging import getLogger
from typing import Union

from beartype import beartype

from cript.cache import get_cached_api_session
from cript.data_model.exceptions import UniqueNodeError
from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.group import Group
from cript.data_model.utils import set_node_attributes

logger = getLogger(__name__)


class Reference(BaseNode):
    """Object representing a bibliographic resource."""

    node_name = "Reference"
    slug = "reference"

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        title: str,
        doi: Union[str, None] = None,
        authors: Union[list[str], None] = None,
        journal: Union[str, None] = None,
        publisher: Union[str, None] = None,
        year: Union[int, None] = None,
        volume: Union[int, None] = None,
        issue: Union[int, None] = None,
        pages: Union[list[int], None] = None,
        issn: Union[str, None] = None,
        arxiv_id: Union[str, None] = None,
        pmid: Union[int, None] = None,
        website: Union[str, None] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        **kwargs,
    ):
        super().__init__(public=public, **kwargs)
        self.title = title
        self.doi = doi
        self.authors = authors if authors else []
        self.journal = journal
        self.publisher = publisher
        self.year = year
        self.volume = volume
        self.issue = issue
        self.pages = pages if pages else []
        self.issn = issn
        self.arxiv_id = arxiv_id
        self.pmid = pmid
        self.website = website
        self.notes = notes
        self.group = group

    @beartype
    def save(self, get_level: int = 1, update_existing: bool = False):
        """
        Create or update a node in the database.

        :param get_level: Level to recursively get nested nodes.
        :param update_existing: Indicates whether to update an existing node with
                                the same unique fields.
        """
        api = get_cached_api_session(self.url)

        # Create a new object via POST
        response = api.post(
            url=f"{api.url}/{self.slug}/",
            data=self._to_json(),
            valid_codes=[201, 400],
        )

        # Check if a unique error was returned
        if "unique" in response:
            unique_url = response.pop("unique")
            if unique_url and update_existing:
                # Update existing unique node
                self.url = unique_url
                self.save(get_level=get_level)
                return
            else:
                raise UniqueNodeError(response["errors"][0])

        set_node_attributes(self, response)
        self._generate_nested_nodes(get_level=get_level)
        logger.info(f"{self.node_name} node has been saved to the database.")
