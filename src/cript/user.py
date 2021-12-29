"""
User Node

"""

from . import CRIPTError
from .base import BaseModel, ReferenceList
from .utils import freeze_class
from .validator import email_format_check, phone_format_check, orcid_format_check, type_check


class UserError(CRIPTError):
    """ Errors from the User Node

    """
    pass


@freeze_class
class User(BaseModel, _error=UserError):
    """ User Node

        The user node represents any researcher or individual who interacts with the CRIPT platform. It serves two main
        purposes: it is to provides a link to data that the individual has contributed to the database, and it provides
        a quick retrieval of other nodes that are directly related to the user.

        Attributes
        ----------
        base_attributes:
            See CRIPT BaseModel
        email: str
            email of the user
        orcid: str
            ORCID (https://orcid.org/) id of the user
        organization: str
            organization the user belongs to
        position: str
            position/title of the user in their organization
        phone: str
            telephone number of the user
        website: str
            personal website of the user
        twitter: str
            Twitter handle of the user
        c_group: Group node
            CRIPT group you belong to
        c_publication: Publication nodes
            CRIPT publication authored by the user
        """

    class_ = "User"

    def __init__(
            self,
            name: str,
            email: str,
            orcid: str = None,
            organization: str = None,
            position: str = None,
            phone: str = None,
            website: str = None,
            twitter: str = None,
            c_group=None,
            c_publication=None,
            notes: str = None,
            **kwargs
    ):
        super().__init__(name=name, class_=self.class_, notes=notes, **kwargs)

        self._email = None
        self.email = email

        self._phone = None
        self.phone = phone

        self._website = None
        self.website = website

        self._twitter = None
        self.twitter = twitter

        self._orcid = None
        self.orcid = orcid

        self._organization = None
        self.organization = organization

        self._position = None
        self.position = position

        self._c_group = ReferenceList("Group", c_group, _error=self._error)
        self._c_publication = ReferenceList("Publication", c_publication, _error=self._error)

    @property
    def email(self):
        return self._email

    @email.setter
    @email_format_check
    @type_check(str)
    def email(self, email):
        self._email = email

    @property
    def phone(self):
        return self._phone

    @phone.setter
    @phone_format_check
    @type_check(str)
    def phone(self, phone):
        self._phone = phone

    @property
    def website(self):
        return self._website

    @website.setter
    @type_check(str)
    def website(self, website):
        self._website = website

    @property
    def twitter(self):
        return self._twitter

    @twitter.setter
    @type_check(str)
    def twitter(self, twitter):
        self._twitter = twitter

    @property
    def orcid(self):
        return self._orcid

    @orcid.setter
    @orcid_format_check
    @type_check(str)
    def orcid(self, orcid):
        self._orcid = orcid

    @property
    def organization(self):
        return self._organization

    @organization.setter
    @type_check(str)
    def organization(self, organization):
        self._organization = organization

    @property
    def position(self):
        return self._position

    @position.setter
    @type_check(str)
    def position(self, position):
        self._position = position

    @property
    def c_group(self):
        return self._c_group

    @c_group.setter
    def c_group(self, *arg):
        self._base_reference_block()

    @property
    def c_publication(self):
        return self._c_publication

    @c_publication.setter
    def c_publication(self, *arg):
        self._base_reference_block()
