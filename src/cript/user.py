"""
User Node

"""

import re

from . import BaseModel, CRIPTError
from .utils.type_check import type_check_property


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
            c_publication: list = None,
            notes: str = None,
            **kwargs
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

        super().__init__(name=name, _class=self._class, notes=notes, **kwargs)

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

        self._c_publication = None
        self.c_publication = c_publication

    @property
    def c_group(self):
        return self._c_group

    @c_group.setter
    def c_group(self, c_group):
        self._setter_CRIPT_prop(c_group, "c_group")

    @property
    def c_publication(self):
        return self._c_publication

    @c_publication.setter
    def c_publication(self, c_publication):
        self._setter_CRIPT_prop(c_publication, "c_publication")

    @property
    def email(self):
        return self._email

    @email.setter
    @type_check_property
    def email(self, email):
        if email is None:
            self._email = email
        elif self._email_format_check(email):
            self._email = email
        else:
            msg = f"Email {email} not of correct format. (format: text@text.text)"
            raise CRIPTError(msg)

    @property
    def phone(self):
        return self._phone

    @phone.setter
    @type_check_property
    def phone(self, phone):
        if phone is None:
            self._phone = phone
        elif self._phone_format_check(phone):
            self._phone = phone
        else:
            msg = f"Phone number {phone} not of correct format. (format: numbers and dash only)"
            raise CRIPTError(msg)

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
        if orcid is None:
            self._orcid = orcid
        elif self._orcid_format_check(orcid):
            self._orcid = orcid
        elif self._orcid_format_check2(orcid):
            orcid = orcid[0:4] + "-" + orcid[4:8] + "-" + orcid[8:12] + "-" + orcid[12:]
            self._orcid = orcid
        else:
            msg = f"{orcid} invalid format, and not added to user node. (format: ####-####-####-####)"
            raise CRIPTError(msg)

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

    @staticmethod
    def _phone_format_check(phone: str) -> bool:
        """
        Check phone format
        """
        regex = r'[0-9|-]{10}'
        if re.match(regex, phone):
            return True
        else:
            return False

    @staticmethod
    def _orcid_format_check(orcid: str) -> bool:
        """
        Check orcid format   ####-####-####-####
        """
        regex = r'[0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{4}'
        if re.match(regex, orcid):
            return True
        else:
            return False

    @staticmethod
    def _orcid_format_check2(orcid: str) -> bool:
        """
        Check orcid format  (no dashes)  ################
        """
        regex = r'[0-9]{16}'
        if re.match(regex, orcid):
            return True
        else:
            return False
