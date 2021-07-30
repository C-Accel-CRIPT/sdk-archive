"""
Publications

"""

from .base import BaseModel


class Publication(BaseModel):

    _class = "Publication"

    def __init__(
            self,
            title: str,
            authors: list[str] = None,
            journal: str = None,
            publisher: str = None,
            year: int = None,
            volume: int = None,
            issue: int = None,
            pages: str = None,
            doi: str = None,
            issn: str = None,
            arxiv_id: str = None,
            PMID: str = None,
            website: str = None,
            notes: str = None
    ):
        """

        :param title: Title of publications.

        :param authors: List of authors [Last name, First name middle intial or name].
        :param journal:
        :param publisher:
        :param year:
        :param volume:
        :param issue:
        :param pages:
        :param doi: DOI: digital object identifier.
        :param issn: ISSN: international standard serial number.
        :param arxiv_id: arXiv identifier.
        :param PMID: PubMed ID.
        :param website: The personal website of the user.
        :param notes: Any miscellaneous notes related to the user.

        :param _class: class of node.
        :param uid: The unique ID of the material.
        :param model_version: Version of CRIPT data model.
        :param version_control: Link to version control node.
        :param last_modified_date: Last date the node was modified.
        :param created_date: Date it was created.
        """
        super().__init__(name=title, _class=self._class, notes=notes)

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

        self._PMID = None
        self.PMID = PMID

        self._website = None
        self.website = website

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def authors(self):
        return self._authors

    @authors.setter
    def authors(self, authors):
        self._authors = authors

    @property
    def journal(self):
        return self._journal

    @journal.setter
    def journal(self, journal):
        self._journal = journal

    @property
    def publisher(self):
        return self._publisher

    @publisher.setter
    def publisher(self, publisher):
        self._publisher = publisher

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, year):
        self._year = year

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, volume):
        self._volume = volume

    @property
    def issue(self):
        return self._issue

    @issue.setter
    def issue(self, issue):
        self._issue = issue

    @property
    def pages(self):
        return self._pages

    @pages.setter
    def pages(self, pages):
        self._pages = pages

    @property
    def doi(self):
        return self._doi

    @doi.setter
    def doi(self, doi):
        self._doi = doi

    @property
    def issn(self):
        return self._issn

    @issn.setter
    def issn(self, issn):
        self._issn = issn

    @property
    def arxiv_id(self):
        return self._arxiv_id

    @doi.setter
    def arxiv_id(self, arxiv_id):
        self._arxiv_id = arxiv_id

    @property
    def PMID(self):
        return self._PMID

    @PMID.setter
    def PMID(self, PMID):
        self._PMID = PMID

    @property
    def website(self):
        return self._website

    @website.setter
    def website(self, website):
        self._website = website



