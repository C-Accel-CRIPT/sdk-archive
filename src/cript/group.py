"""
Group Node

"""
import re
import warnings

from .base import BaseModel, CRIPTWarning
from .utils.type_check import *


class Group(BaseModel):
    _class = "Group"

    def __init__(
            self,
            name: str,
            email: str = None,
            website: str = None,
            c_owner: list = None,
            c_collection: list = None,
            c_group: list = None,
            notes: str = None,
            **kwargs
    ):
        """
        :param name: The name of the group.
        :param email: The email address of the group.

        :param website: The website of the group.

        :param c_owner:
        :param c_collection: CRIPT collection
        :param c_group: CRIPT groups that own this own

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

        self._website = None
        self.website = website

        self._c_owner = None
        self.c_owner = c_owner

        self._c_collection = None
        self.c_collection = c_collection

        self._c_group = None
        self.c_group = c_group

        # publication

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
            warnings.warn(msg, CRIPTWarning)

    @property
    def website(self):
        return self._website

    @website.setter
    @type_check_property
    def website(self, website):
        self._website = website

    @property
    def c_owner(self):
        return self._c_owner

    @c_owner.setter
    @type_check_property
    def c_owner(self, c_owner):
        self._c_owner = c_owner

    @property
    def c_group(self):
        return self._c_group

    @c_group.setter
    def c_group(self, c_group):
        self._set_CRIPT_prop(c_group, "c_group")

    @property
    def c_collection(self):
        return self._c_collection

    @c_collection.setter
    def c_collection(self, c_collection):
        self._set_CRIPT_prop(c_collection, "c_collection")

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