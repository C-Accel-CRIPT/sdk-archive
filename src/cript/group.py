"""
Group Node

"""

from . import CRIPTError
from .base import BaseModel, ReferenceList
from .utils import freeze_class
from .validator import email_format_check, type_check


class GroupError(CRIPTError):
    """ Errors from the Group Node

    """
    pass


@freeze_class
class Group(BaseModel, _error=GroupError):
    """ Group Node

        The group node represents organizations, research groups, or any group of users. It serves the same two
        purposes of users, which is to link data to the group producing it and to provide quick retrieval of other
        nodes that are directly related to the group.

        Attributes
        ----------
        base_attributes:
            See CRIPT BaseModel
        email: str
            email address of the group
        website:
            website of the group
        c_owner: User node
            CRIPT user that owns the group
        c_group: Group node
            Parent CRIPT groups
        c_collection: Collection node
            CRIPT collection owned by the group
        c_publication: Publication node
            CRIPT publication owned by the group
        c_inventory: Inventory node
            CRIPT inventory owned by the group
    """

    class_ = "Group"

    def __init__(
            self,
            name: str,
            email: str = None,
            website: str = None,
            c_owner=None,
            c_group=None,
            c_collection=None,
            c_publication=None,
            c_inventory=None,
            notes: str = None,
            **kwargs
    ):
        super().__init__(name=name, class_=self.class_, notes=notes, **kwargs)

        self._email = None
        self.email = email

        self._website = None
        self.website = website

        self._c_owner = ReferenceList("User", c_owner, self._error)
        self._c_group = ReferenceList("Group", c_group, self._error)
        self._c_publication = ReferenceList("Publication", c_publication, self._error)
        self._c_collection = ReferenceList("Collection", c_collection, self._error)
        self._c_inventory = ReferenceList("Inventory", c_inventory, self._error)

    @property
    def email(self):
        return self._email

    @email.setter
    @email_format_check
    @type_check(str)
    def email(self, email):
        self._email = email

    @property
    def website(self):
        return self._website

    @website.setter
    @type_check(str)
    def website(self, website):
        self._website = website

    @property
    def c_owner(self):
        return self._c_owner

    @c_owner.setter
    def c_owner(self, *args):
        self._base_reference_block()

    @property
    def c_group(self):
        return self._c_group

    @c_group.setter
    def c_group(self, *args):
        self._base_reference_block()

    @property
    def c_publication(self):
        return self._c_publication

    @c_publication.setter
    def c_publication(self, *args):
        self._base_reference_block()

    @property
    def c_collection(self):
        return self._c_collection

    @c_collection.setter
    def c_collection(self, *args):
        self._base_reference_block()

    @property
    def c_inventory(self):
        return self._c_inventory

    @c_inventory.setter
    def c_inventory(self, *args):
        self._base_reference_block()
