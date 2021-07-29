"""
User Node

"""
import cript.group

from .base import BaseModel


class User(BaseModel):
    _class = "user"

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
            c_groups: list = None,
            notes: str = None
    ):
        """

        :param name: The name of the user.
        :param email: The email id of the user.

        :param phone: The telephone number of the user.
        :param website: The personal website of the user.
        :param twitter: The Twitter handle of the user.
        :param orcid: The ORCID (https://orcid.org/) iD of the user.
        :param organization: The organization the user belongs to.
        :param position: The position/title of the user in their organization.
        :param notes: Any miscellaneous notes related to the user.

        :param c_groups: CRIPT groups you belong to

        :param _class: class of node.
        :param uid: The unique ID of the material.
        :param model_version: Version of CRIPT data model.
        :param version_control: Link to version control node.
        :param last_modified_date: Last date the node was modified.
        :param created_date: Date it was created.
        """

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

        self._c_groups = None
        self.c_groups = c_groups

        # publication

    @property
    def c_groups(self):
        return self._c_groups

    @c_groups.setter
    def c_groups(self, c_groups):
        for group in c_groups:
            if not isinstance(group, cript.group.Group):
                msg = f"Group {group} not of type `Group`."
                raise UserError(msg)
            self._groups.append(group)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, phone):
        self._phone = phone

    @property
    def website(self):
        return self._website

    @website.setter
    def website(self, website):
        self._website = website

    @property
    def twitter(self):
        return self._twitter

    @twitter.setter
    def twitter(self, twitter):
        self._twitter = twitter

    @property
    def orcid(self):
        return self._orcid

    @orcid.setter
    def orcid(self, orcid):
        self._orcid = orcid

    @property
    def organization(self):
        return self._organization

    @organization.setter
    def organization(self, organization):
        self._organization = organization

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
