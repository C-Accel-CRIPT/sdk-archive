"""
Group Node

"""

from . import CRIPTError
from .base import BaseModel, BaseReference
from .utils.validator.type_check import type_check_property
from .utils.validator.user import email_format_check


class GroupError(CRIPTError):
    def __init__(self, *msg):
        super().__init__(*msg)


class Group(BaseModel):
    _class = "Group"
    _error = GroupError

    def __init__(
            self,
            name: str,
            email: str = None,
            website: str = None,
            c_owner: list = None,
            c_collection: list = None,
            c_group: list = None,
            c_publication: list = None,
            c_inventory=None,
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

        self.c_owner = BaseReference("User", c_owner)
        self.c_group = BaseReference("Group", c_group)
        self.c_publication = BaseReference("Publication", c_publication)
        self.c_collection = BaseReference("Collection", c_collection)
        self.c_inventory = BaseReference("Inventory", c_inventory)

    @property
    def email(self):
        return self._email

    @email.setter
    @email_format_check
    @type_check_property
    def email(self, email):
        self._email = email

    @property
    def website(self):
        return self._website

    @website.setter
    @type_check_property
    def website(self, website):
        self._website = website
