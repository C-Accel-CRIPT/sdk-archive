"""
Class
-----
CriptTypes
Base Model
ReferenceList

"""

from abc import ABC
from typing import Union
from datetime import datetime

from bson import ObjectId
import difflib

from .. import __version__, CRIPTError
from ..utils import GetObject, Serializable, loading_with_datetime
from ..validator import id_type_check_bool, type_check


class CriptTypes:
    """ CRIPT Types

    This class is to provide access to cript_types after they have been initiated.

    Attributes
    ----------
    cript_types: dict[str, node]
        dictionary of CRIPT types

    """
    cript_types = None

    @classmethod
    def _init_(cls):
        """ Will be called at the end of cript.__init__ """
        from .. import cript_types
        cls.cript_types = cript_types


class BaseModel(Serializable, CriptTypes, ABC):
    """ Base Model

    Attributes common to all nodes in CRIPT.

    Attributes
    ----------
    name: str
        descriptive user defined label
    notes: str
        miscellaneous information
    class_: str
        class of node
    uid: str
        unique ID of the material
    model_version: str
        version of CRIPT data model
    version_control: str
        link to version control node
    last_modified_date: datetime
        last date the node was modified
    created_date: datetime
        date it was created
    """
    _error = CRIPTError

    def __init__(
            self,
            name: str,
            notes: str = None,
            class_: str = None,
            uid: Union[str, ObjectId] = None,
            model_version: str = None,
            version_control=None,
            last_modified_date: datetime = None,
            created_date: datetime = None
    ):

        self._name = None
        self.name = name

        self._notes = None
        self.notes = notes

        self._class_ = None
        self.class_ = class_

        self._uid = None
        self.uid = uid

        if model_version is None:
            self._model_version = __version__
        else:
            self._model_version = model_version
        self._version_control = version_control

        self._last_modified_date = None
        self.last_modified_date = last_modified_date

        self._created_date = None
        self.created_date = created_date

    def __init_subclass__(cls, **kwargs):
        if "_error" in kwargs.keys():
            cls._error = kwargs["_error"]

    @property
    def name(self):
        return self._name

    @name.setter
    @type_check(str)
    def name(self, name):
        self._name = name

    @property
    def notes(self):
        return self._notes

    @notes.setter
    @type_check(str)
    def notes(self, notes):
        self._notes = notes

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        if uid is None:
            pass
        elif type(uid) is ObjectId:
            uid = str(uid)
        else:
            if not id_type_check_bool(uid):
                mes = f"{uid} is invalid uid."
                raise self._error(mes)
        self._uid = uid

    @property
    def class_(self):
        return self._class_

    @class_.setter
    def class_(self, class_):
        self._class_ = class_

    @property
    def model_version(self):
        return self._model_version

    @property
    def version_control(self):
        return self._version_control

    @property
    def last_modified_date(self):
        return self._last_modified_date

    @last_modified_date.setter
    @type_check(datetime)
    @loading_with_datetime
    def last_modified_date(self, last_modified_date):
        self._last_modified_date = last_modified_date

    @property
    def created_date(self):
        return self._created_date

    @created_date.setter
    @type_check(datetime)
    @loading_with_datetime
    def created_date(self, created_date):
        self._created_date = created_date

    def reference(self) -> dict:
        """ create reference dictionary for the node """
        ddict = self.as_dict(save=False)
        return self.create_reference(ddict)

    @staticmethod
    def create_reference(ddict) -> dict:
        """ create_reference

        Gives reference dictionary from dictionary.

        Note
        ----
        * This method may be overwritten in inheritance.

        """
        keys = ["uid", "name", "class_"]
        if "_id" in ddict.keys():
            ddict["uid"] = ddict.pop("_id")

        if not all(k in ddict.keys() and ddict[k] is not None for k in keys):
            if ddict["uid"] is None and ddict["name"] is not None:
                mes = f"'{ddict['name']}' needs to be saved before it can generate a reference."
            else:
                mes = f"{ddict} is missing one or more of the following [{keys}]"
            raise CRIPTError(mes)

        out = {}
        for key in keys:
            out[key] = ddict[key]

        return out

    @staticmethod
    def _base_reference_block():
        """ _base_reference_block

        This is to block a user from directly trying to modify a reference list without going through the
        ReferenceList class.

        """
        raise AttributeError("Use '.add()' or .remove() to modify.")


class ReferenceList(CriptTypes):
    """ Reference List

    The ReferenceList creates, and formats references. It also makes references callable and index-able.

    Attributes
    ----------
    _reference: list[dict]
        List of references
    _uids: List[str]
        List of uids (same as objs as _reference)
    _node: str
        Name of names that are stored in the reference list (used for type checking)
    limit: int
        maximum number of reference allowed
        default is 10000

    Methods
    -------
    add(item)
        Adds item to reference list
    remove(item)
        Removes item from reference list

    """

    _error = None

    def __init__(self, node: str, objs=None, _error=CRIPTError, limit: int = 10000):
        """
        Parameters
        ----------
        node: str
            Type of cript node. "User", "Group", etc.
        objs:
            objects will be passed to self.add()
        _error:
            error class of parent node
        limit: int
            maximum number of reference allowed
            default is 10000
        """
        self._reference = []
        self._uids = []
        self._node = node
        self._error = _error
        self.limit = limit
        self.count = 0

        if objs is not None:
            self.add(objs)

    def __repr__(self):
        return repr(self._reference)

    def __call__(self):
        return self._reference

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._reference[item]
        elif isinstance(item, str):
            index = self._get_index_from_name(item)
            return self._reference[index]
        elif isinstance(item, slice):
            return [self._reference[i] for i in range(*item.indices(len(self._reference)))]
        else:
            mes = "Item not found."
            raise self._error(mes)

    def __len__(self):
        return len(self._reference)

    def __iter__(self):
        for ref in self._reference:
            yield ref

    def _get_index_from_name(self, item: str) -> int:
        """

        Given a item name, return item index in list.
        This matching is done with difflib, so slight typing errors wont result in errors.

        Parameters
        ----------
        item: str
            name of item you are trying to find

        Returns
        -------
        index: int
            index of item in self._reference list

        Raises
        ------
        Exception
            If item name not found.

        """
        values = [i["name"] for i in self._reference]
        text, score = difflib.get_close_matches(item, values, n=1, cutoff=0.8)
        if score > 50:
            return values.index(text)
        else:
            mes = f"'{item}' not found."
            raise self._error(mes)

    def add(self, objs):
        """ Add

        Adds object to reference list.

        Parameters
        ----------
        objs:
            object that you want to add to the list
            Accepted objects:
                dict from database
                dict which is already a reference
                CRIPT object (CRIPT type)
                uid (str)

        Raises
        -------
        Exception
            If invalid object is provided. An object that does not lead to a valid reference.

        """
        if not isinstance(objs, list):
            objs = [objs]
        if self.count + len(objs) > self.limit:
            raise self._error(f"Attempting to exceed the limit of {self._node} that can be contained.\n "
                              f"Current amount: {self.count}\n"
                              f"Attempting to add: {len(objs)}\n"
                              f"Limit: {self.limit}")

        for obj in objs:
            # given an obj get reference dictionary
            if isinstance(obj, dict):
                ref = self._obj_is_dict(obj)
            elif isinstance(obj, str) and id_type_check_bool(obj):
                ref = self._obj_is_uid(obj)
            elif isinstance(obj, self.cript_types[self._node]):
                ref = self._obj_is_cript_node(obj)
            else:
                mes = f"Invalid reference object type for '{self._node}'. '{obj}'"
                raise self._error(mes)

            # check if reference s not already in list, and add it.
            if ref["uid"] not in self._uids:
                self._reference.append(ref)
                self._uids.append(ref["uid"])
                self.count += 1
            else:
                mes = f"Reference already in list for '{self._node}'.'{obj}'"
                raise self._error(mes)

    def _obj_is_dict(self, obj: dict) -> dict:
        """ Object is dictionary

        Given a dictionary (JSON of a CRIPT node) get reference dictionary
        Happens when passing node from cript.view() or is a reference already

        Parameters
        ----------
        obj: dict
            CRIPT node in dictionary format

        Returns
        -------
        reference
            Returns reference dictionary

        Raises
        -------
        Exception
            If invalid dictionary provided

        """
        if "_id" in obj.keys():
            return self.cript_types[self._node].create_reference(obj)
        elif "uid" in obj.keys():
            ref_fun = getattr(self.cript_types[obj["class_"]], "create_reference")
            return ref_fun(obj)
        else:
            mes = f"Invalid reference object for '{self._node}'. '{obj}'"
            raise self._error(mes)

    def _obj_is_uid(self, obj: str) -> dict:
        """ Object is uid

        User may give just uid, in which we need to go get the node from the database.

        Parameters
        ----------
        obj: str
            CRIPT database uid

        Returns
        -------
        reference
            Returns reference dictionary

        """
        obj = GetObject.get_from_uid(self._node, obj)
        return self.cript_types[self._node].create_reference(obj[0])

    @staticmethod
    def _obj_is_cript_node(obj: BaseModel) -> dict:
        """ Object is CRIPT node

        Call reference method which can be found in BaseModel class if not overwritten.

        Parameters
        ----------
        obj: BaseModel
            CRIPT Node

        Returns
        -------
        reference
            Returns reference dictionary

        """
        return obj.reference()

    def remove(self, objs):
        """ Remove

        Removes object from reference list.

        Parameters
        ----------
        objs:
            object that you want to remove to the list
            Accepted objects:
                dict from database
                dict which is already a reference
                CRIPT object (CRIPT type)
                uid (str)
                name (str)
                position in _reference list (int)

        Raises
        -------
        Exception
            If invalid object is provided. An object that does not lead to a valid removal.
            If the object is not in the list.

        """
        if not isinstance(objs, list):
            objs = [objs]

        # converter all objects into a list of uids
        remove = []  # list of uids
        for obj in objs:
            if isinstance(obj, dict):
                remove.append(obj["uid"])
            elif isinstance(obj, str) and id_type_check_bool(obj):
                remove.append(obj)
            elif isinstance(obj, str):
                remove.append(self._remove_by_name(obj))
            elif isinstance(obj, self.cript_types[self._node]):
                remove.append(obj.uid)
            elif isinstance(obj, int):
                remove.append(self._uids[obj])
            else:
                mes = f"Invalid remove object type for '{self._node}'. '{obj}'"
                raise self._error(mes)

        # loop through 'remove list' to remove objs
        for r in remove:
            if r in self._uids:
                self._remove_reference(r)
                self._uids.remove(r)
                self.count -= 1
            else:
                mes = f"{r} not in list, so it can't be removed from '{self._node}'."
                raise self._error(mes)

    def _remove_by_name(self, name: str) -> str:
        """ Remove by name

        Given a name, determine which reference it corresponds to and return uid

        Parameters
        ----------
        name: str
            name of reference to be removed

        Returns
        -------
        uid: str
            Returns uid to be added to removal list

        Raises
        -------
        Exception
            If name not found in references.

        """
        for i in self._reference:
            if i["name"] == name:
                return i["uid"]

        else:
            mes = f"{name} not found in '{self._node}'."
            raise self._error(mes)

    def _remove_reference(self, remove: str):
        """ Remove reference

        Given a list of uids, remove them from self._references.

        Parameters
        ----------
        remove: str
            uid of reference to be removed

        """
        for i in self._reference:
            if i["uid"] == remove:
                self._reference.remove(i)

    def as_dict(self, **kwags) -> list:
        """ Returns list of references for serialization."""
        return self._reference
