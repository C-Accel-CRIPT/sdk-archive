"""
base:

Contains BaseModel, BaseReference, and load

"""
from abc import ABC
from typing import Union
from datetime import datetime

from bson import ObjectId
from fuzzywuzzy import process

from . import __version__, CRIPTError
from .utils.serializable import Serializable
from .utils.validator.type_check import type_check_property, id_type_check_bool, id_type_check
from .utils.external_database_code import GetObject


class CriptTypes:
    cript_types = None

    @classmethod
    def _init_(cls):
        from . import cript_types
        cls.cript_types = cript_types


class BaseModel(Serializable, CriptTypes, ABC):

    def __init__(
        self,
        name: str,
        _class: str = None,
        notes: str = None,

        uid: Union[str, ObjectId] = None,
        model_version: str = None,
        version_control=None,
        last_modified_date: datetime = None,
        created_date: datetime = None
    ):
        """
        :param name: Descriptive name

        :param notes: Any miscellaneous notes related to the user.
        :param _class: class of node.
        :param uid: The unique ID of the material.
        :param model_version: Version of CRIPT data model.
        :param version_control: Link to version control node.
        :param last_modified_date: Last date the node was modified.
        :param created_date: Date it was created.
        """

        self._name = None
        self.name = name

        self._notes = None
        self.notes = notes

        self._class_ = None
        self.class_ = _class

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

    @property
    def name(self):
        return self._name

    @name.setter
    @type_check_property
    def name(self, name):
        self._name = name

    @property
    def notes(self):
        return self._notes

    @notes.setter
    @type_check_property
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
            if not id_type_check(uid):
                mes = f"{uid} is invalid uid."
                raise CRIPTError(mes)
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
    def last_modified_date(self, last_modified_date):
        self._last_modified_date = last_modified_date

    @property
    def created_date(self):
        return self._created_date

    @created_date.setter
    def created_date(self, created_date):
        self._created_date = created_date

    def _reference(self) -> dict:
        """
        From a filled out node, create reference dictionary.
        :return:
        """
        ddict = self.as_dict(save=False)
        return self._create_reference(ddict)

    @staticmethod
    def _create_reference(ddict) -> dict:
        """
        Gives reference dictionary from dictionary.
        * This method may be overwritten in inheritance.
        """
        keys = ["uid", "name"]
        if "_id" in ddict.keys():
            ddict["uid"] = ddict.pop("_id")

        if not all(k in ddict.keys() and ddict[k] is not None for k in keys):
            if ddict["uid"] is None and ddict["name"] is not None:
                mes = f"'{ddict['name']}' needs to be saved before it can generate a reference."
            else:
                mes = f"{ddict} is missing one or more of the following keys()"
            raise CRIPTError(mes)

        out = {}
        for key in keys:
            out[key] = ddict[key]

        return out


class BaseReference(CriptTypes):
    _error = CRIPTError

    def __init__(self, node: str, objs=None):
        self._reference = []
        self._uids = []
        self._node = node

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
        else:
            mes = "Item not found."
            raise self._error(mes)

    def _get_index_from_name(self, item: str) -> int:
        values = [i["name"] for i in self._reference]
        text, score = process.extractOne(item, values)
        if score > 50:
            return values.index(text)
        else:
            mes = f"'{item}' not found."
            raise self._error(mes)

    def add(self, objs):
        if not isinstance(objs, list):
            objs = [objs]

        for obj in objs:
            if isinstance(obj, dict):
                ref = self._obj_is_dict(obj)
            elif isinstance(obj, str) and id_type_check_bool(obj):
                ref = self._obj_is_uid(obj)
            elif isinstance(obj, self.cript_types[self._node]):
                ref = self._obj_is_cript_node(obj)
            else:
                mes = f"Invalid reference object type. '{obj}'"
                raise self._error(mes)

            if ref["uid"] not in self._uids:
                self._reference.append(ref)
                self._uids.append(ref["uid"])
            else:
                mes = f"Reference already in list.'{obj}'"
                raise self._error(mes)

    def _obj_is_dict(self, obj: dict) -> dict:
        """
        Happens when passing node from cript.view() or is a referance already
        """
        if "_id" in obj.keys():
            return self.cript_types[self._node]._create_reference(obj)
        elif "uid" in obj.keys():
            return obj
        else:
            mes = f"Invalid reference object. '{obj}'"
            raise self._error(mes)

    def _obj_is_uid(self, obj: str) -> dict:
        """
        User may give just id as string
        """
        obj = GetObject.get_from_uid(self._node, obj)
        return self.cript_types[self._node]._create_reference(obj[0])

    @staticmethod
    def _obj_is_cript_node(obj: str) -> dict:
        """
        User may give a CRIPT node
        """
        return obj._reference()

    def remove(self, objs):
        if not isinstance(objs, list):
            objs = [objs]

        remove = []
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
                mes = f"Invalid remove object type. '{obj}'"
                raise self._error(mes)

        for r in remove:
            if r in self._uids:
                self._remove_reference(r)
                self._uids.remove(r)
            else:
                mes = f"{r} not in list, so it can't be removed."
                raise self._error(mes)

    def _remove_by_name(self, name: str):
        for i in self._reference:
            if i["name"] == name:
                return i["uid"]

        else:
            mes = f"{name} not found."
            raise self._error(mes)

    def _remove_reference(self, remove: str):
        for i in self._reference:
            if i["uid"] == remove:
                self._reference.remove(i)

    def as_dict(self, **kwags):
        return self._reference


class Load:
    """Given a document from the database convert it into a CRIPT object."""
    cript_types = None

    def __call__(self, ddict):
        if self.cript_types is None:
            load._init_()
        if "_id" in ddict.keys():
            ddict["uid"] = str(ddict.pop("_id"))
        class_ = ddict.pop("class_")
        obj = self.cript_types[class_](**ddict)
        return obj

    @classmethod
    def _init_(cls):
        from . import cript_types
        cls.cript_types = cript_types


load = Load()
