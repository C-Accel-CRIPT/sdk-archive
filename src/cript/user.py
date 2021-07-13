from typing import List
from typing import Union
from bson.objectid import ObjectId

from .base import BaseModel
#from .group import Group


class UserError(Exception):
    """Base class to handle errors associated with the user model."""

    pass


class User(BaseModel):
    """Base class for representing a user.
    Parameters
    ----------
    ** required **
    name: str
        The name of the user.
    email: str
        The email id of the user.

    ** optional **
    phone: str
        The telephone number of the user.
    website: str
        The personal website of the user.
    twitter: str
        The Twitter handle of the user.
    orcid: str
        The ORCID (https://orcid.org/) iD of the user.
    organization: str
        The organization the user belongs to.
    position: str
        The position/title of the user in their organization.
    notes: str
        Any miscellaneous notes related to the user.

    groups: list[Group]
        The list of groups this user belongs to.
    """

    _class = "user"
    meta = {
        'db_alias': "core",
        "collection": "user"
    }

    def __init__(
        self,
        name: str,
        email: str,
        phone: str = None,
        website: str = None,
        twitter: str = None,
        orcid: str = None,
        organization: str = None,
        position: str = None,
        notes: str = None,
    ):
        super().__init__(name=name, _class=self._class, notes=notes)

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

        # self._groups = []
        # self.groups = None

    @property
    def groups(self):
        """List of groups the user belongs to."""
        return self._groups

    @groups.setter
    def groups(self, groups):
        for group in groups:
            if not isinstance(group, Group):
                msg = f"Group {group} not of type `data_model.group.Group`"
                raise UserError(msg)
            self._groups.append(group)

    @property
    def email(self):
        """Email address of the user."""
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def phone(self):
        """Telephone number of the user."""
        return self._phone

    @phone.setter
    def phone(self, phone):
        self._phone = phone

    @property
    def website(self):
        """Web address of the user."""
        return self._website

    @website.setter
    def website(self, website):
        self._website = website

    @property
    def twitter(self):
        """Twitter handle of the user."""
        return self._twitter

    @twitter.setter
    def twitter(self, twitter):
        self._twitter = twitter

    @property
    def orcid(self):
        """ORCiD ID of the user."""
        return self._orcid

    @orcid.setter
    def orcid(self, orcid):
        self._orcid = orcid

    @property
    def organization(self):
        """Organization of the user."""
        return self._organization

    @organization.setter
    def organization(self, organization):
        self._organization = organization

    @property
    def position(self):
        """Position of the user within their organization."""
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
