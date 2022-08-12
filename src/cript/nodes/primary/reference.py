from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes.primary.group import Group


logger = getLogger(__name__)


class Reference(BasePrimary):
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
    ):
        super().__init__(public=public)
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
