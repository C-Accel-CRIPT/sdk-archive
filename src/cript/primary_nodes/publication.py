"""
Publications

"""
from typing import Union

from .. import CRIPTError
from ..utils import freeze_class
from ..validator import type_check
from .base import BaseModel, ReferenceList


class PublicationError(CRIPTError):
    """ Errors from the Publication Node

    """
    pass


@freeze_class
class Publication(BaseModel, _error=PublicationError):
    """ Publication Node


    Attributes
    ----------
    base_attributes:
        See help(BaseModel)
    title: str
        Title of publication
    authors: list[str]
        List of authors [First name middle initial or name, Last name].
    journal: str
        Journal of the publication
    publisher: str
        Publisher of publication
    year: int
        Year of publication
    volume: int
        Volume of publication
    issue: int
        Issue of publication
    pages: int, list[int]
        Pages of publication [start page, end page]
    doi: str
        DOI: digital object identifier
    issn: str
        ISSN: international standard serial number
    arxiv_id: str
        arXiv identifier
    pmid: str
        PMID: PubMed ID
    website: str
        website where the publication can be accessed
    c_collection: Collection node
        CRIPT collection owned by the group
    """

    class_ = "Publication"

    def __init__(
            self,
            title: str,
            doi: str,
            name: str = None,
            authors: list[str] = None,
            journal: str = None,
            publisher: str = None,
            year: int = None,
            volume: int = None,
            issue: int = None,
            pages: Union[int, list[int]] = None,
            issn: str = None,
            arxiv_id: str = None,
            pmid: str = None,
            website: str = None,
            funding: str = None,
            notes: str = None,
            c_collection=None,
            **kwargs
    ):
        if name is None:
            name = title

        super().__init__(name=name, class_=self.class_, notes=notes, **kwargs)

        self._title = None
        self.title = title

        self._authors = None
        self.authors = authors

        self._journal = None
        self.journal = journal

        self._publisher = None
        self.publisher = publisher

        self._year = None
        self.year = year

        self._volume = None
        self.volume = volume

        self._issue = None
        self.issue = issue

        self._pages = None
        self.pages = pages

        self._doi = None
        self.doi = doi

        self._issn = None
        self.issn = issn

        self._arxiv_id = None
        self.arxiv_id = arxiv_id

        self._pmid = None
        self.pmid = pmid

        self._website = None
        self.website = website

        self._funding = None
        self.funding = funding

        self._c_collection = ReferenceList("Collection", c_collection, self._error)

    @property
    def title(self):
        return self._title

    @title.setter
    @type_check(str)
    def title(self, title):
        self._title = title

    @property
    def authors(self):
        return self._authors

    @authors.setter
    @type_check([str, list[str]])
    def authors(self, authors):
        self._authors = authors

    @property
    def journal(self):
        return self._journal

    @journal.setter
    @type_check(str)
    def journal(self, journal):
        self._journal = journal

    @property
    def publisher(self):
        return self._publisher

    @publisher.setter
    @type_check(str)
    def publisher(self, publisher):
        self._publisher = publisher

    @property
    def year(self):
        return self._year

    @year.setter
    @type_check(int)
    def year(self, year):
        self._year = year

    @property
    def volume(self):
        return self._volume

    @volume.setter
    @type_check(int)
    def volume(self, volume):
        self._volume = volume

    @property
    def issue(self):
        return self._issue

    @issue.setter
    @type_check(int)
    def issue(self, issue):
        self._issue = issue

    @property
    def pages(self):
        return self._pages

    @pages.setter
    @type_check([int, list[int]])
    def pages(self, pages):
        self._pages = pages

    @property
    def doi(self):
        return self._doi

    @doi.setter
    @type_check(str)
    def doi(self, doi):
        self._doi = doi

    @property
    def issn(self):
        return self._issn

    @issn.setter
    @type_check(str)
    def issn(self, issn):
        self._issn = issn

    @property
    def arxiv_id(self):
        return self._arxiv_id

    @arxiv_id.setter
    @type_check(str)
    def arxiv_id(self, arxiv_id):
        self._arxiv_id = arxiv_id

    @property
    def pmid(self):
        return self._pmid

    @pmid.setter
    @type_check(str)
    def pmid(self, pmid):
        self._pmid = pmid

    @property
    def website(self):
        return self._website

    @website.setter
    @type_check(str)
    def website(self, website):
        self._website = website

    @property
    def funding(self):
        return self._funding

    @funding.setter
    @type_check(str)
    def funding(self, funding):
        self._funding = funding

    @property
    def c_collection(self):
        return self._c_collection

    @c_collection.setter
    def c_collection(self, *args):
        self._base_reference_block()
