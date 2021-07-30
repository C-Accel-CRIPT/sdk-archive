"""
User Node

"""

import warnings
import re

import cript.group
from .base import BaseModel, CRIPTWarning
from .utils.type_check import *


class User(BaseModel):
    _class = "User"

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
            c_group: list = None,
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

        :param c_group: CRIPT group you belong to

        :param notes: Any miscellaneous notes related to the user.
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

        self._c_group = None
        self.c_group = c_group

        # publication

    @property
    def c_group(self):
        return self._c_group

    @c_group.setter
    def c_group(self, c_group):
        if c_group is None:
            self._c_group = None
        else:
            current_group_uids = [g[0] for g in self.c_group]
            for group in c_group:
                if type(group) is list:
                    self._c_group.append(group)
                if not isinstance(group, cript.group.Group):
                    msg = f"Group {group} not of type `Group` and not added to user node."
                    warnings.warn(msg, CRIPTWarning)
                    continue
                if group.uid is None:
                    msg = f"Group {group} needs to be saved before adding it to the user node."
                    warnings.warn(msg, CRIPTWarning)
                    continue
                if group.uid in current_group_uids:
                    msg = f"Group {group} already added to user node."
                    warnings.warn(msg, CRIPTWarning)
                    continue

                self._c_group.append([group.uid, group.name])

    @property
    def email(self):
        return self._email

    @email.setter
    @type_check_property
    def email(self, email):
        if self._email_format_check(email):
            self._email = email
        else:
            msg = f"Email {email} not of correct format. (text@text.text)"
            warnings.warn(msg, CRIPTWarning)

    @property
    def phone(self):
        return self._phone

    @phone.setter
    @type_check_property
    def phone(self, phone):
        self._phone = phone

    @property
    def website(self):
        return self._website

    @website.setter
    @type_check_property
    def website(self, website):
        self._website = website

    @property
    def twitter(self):
        return self._twitter

    @twitter.setter
    @type_check_property
    def twitter(self, twitter):
        self._twitter = twitter

    @property
    def orcid(self):
        return self._orcid

    @orcid.setter
    @type_check_property
    def orcid(self, orcid):
        self._orcid = orcid

    @property
    def organization(self):
        return self._organization

    @organization.setter
    @type_check_property
    def organization(self, organization):
        self._organization = organization

    @property
    def position(self):
        return self._position

    @position.setter
    @type_check_property
    def position(self, position):
        self._position = position

    @staticmethod
    def _email_format_check(email: str) -> bool:
        """
        Check email is text@text.text
        """
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.match(regex, email):
            return True
        else:
            return False
