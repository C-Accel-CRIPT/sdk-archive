"""
Group Node

"""

from . import CRIPTError
from .base import BaseModel, BaseSlot
from .utils.validator.type_check import type_check_property
from .utils.validator.user import email_format_check
from .utils.class_tools import freeze_class


class GroupError(CRIPTError):
    pass


@freeze_class
class Group(BaseModel, _error=GroupError):
    class_ = "Group"

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

        super().__init__(name=name, class_=self.class_, notes=notes, **kwargs)

        self._email = None
        self.email = email

        self._website = None
        self.website = website

        self._c_owner = BaseSlot("User", c_owner, self._error)
        self._c_group = BaseSlot("Group", c_group, self._error)
        self._c_publication = BaseSlot("Publication", c_publication, self._error)
        self._c_collection = BaseSlot("Collection", c_collection, self._error)
        self._c_inventory = BaseSlot("Inventory", c_inventory, self._error)

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
        
    @property
    def c_owner(self):
        return self._c_owner

    @c_owner.setter
    def c_owner(self, *args):
        self._base_slot_block()

    @property
    def c_group(self):
        return self._c_group

    @c_group.setter
    def c_group(self, *args):
        self._base_slot_block()

    @property
    def c_publication(self):
        return self._c_publication

    @c_publication.setter
    def c_publication(self, *args):
        self._base_slot_block()

    @property
    def c_collection(self):
        return self._c_collection

    @c_collection.setter
    def c_collection(self, *args):
        self._base_slot_block()

    @property
    def c_inventory(self):
        return self._c_inventory

    @c_inventory.setter
    def c_inventory(self, *args):
        self._base_slot_block()
