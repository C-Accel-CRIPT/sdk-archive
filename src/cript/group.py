"""
Group Node

"""

from .base import BaseModel


class Group(BaseModel):


    _class = "group"

    def __init__(
            self,
            name: str,
            email: str = None,
            website: str = None,
            owner: str = None,
            collection: str = None,
            parent_group: str = None,
            publication: str = None,
            notes: str = None
    ):
        """

        :param name: The name of the group. [it must be unique within the databse]

        :param email: The email address of the group.
        :param website: The website of the group.
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

        self._website = None
        self.website = website

        self._owner = None
        self.owner = owner

        # collection
        # parent group
        # publication

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def website(self):
        return self._website

    @website.setter
    def website(self, website):
        self._website = website

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, owner):
        self._owner = owner
