"""
base:

Contains BaseModel that all core CRIPT nodes inherits from.
Contains CRIPTError and CRIPTWarning

"""

from abc import ABC
from typing import Union
from json import dumps
from datetime import datetime

from bson import ObjectId

from . import __version__
from .utils.serializable import Serializable
from .utils.type_check import type_check_property, type_check, id_type_check
import cript as C


class BaseModel(Serializable, ABC):
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

    def __repr__(self):
        return dumps(self.dict_datetime_to_str(self.as_dict()), indent=2, sort_keys=True)

    def __str__(self):
        return dumps(self.dict_datetime_to_str(self.dict_remove_none(self.as_dict())), indent=2, sort_keys=True)

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
        if type(uid) is ObjectId:
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
        ddict = self.as_dict()
        return self._create_reference(ddict)

    @staticmethod
    def _create_reference(ddict) -> dict:
        """
        Gives reference dictionary from dictionary.
        * This method may be overwritten in inheritance.
        """
        keys = ["uid", "name"]
        out = {}
        for key in keys:
            out[key] = ddict[key]

        return out

    def _setter_CRIPT_prop(self, objs, prop: str):
        """
        This can set CRIPT properties
        :param objs: List of CRIPT objects or Lists of strings to add to prop
        :param prop: The property to be set
        :return:
        """
        _class = prop[2:]  # strip "c_"
        _type = C.cript_types[_class.capitalize()]

        if objs is None:
            setattr(self, f"_{prop}", None)
        elif isinstance(objs, str) and objs == "_clear":
            setattr(self, f"_{prop}", None)
        else:
            # get uid already in node
            current_uids = []
            if isinstance(getattr(self, prop), list):
                for g in getattr(self, prop):
                    if isinstance(g, dict):
                        current_uids.append(g["uid"])

            # if list not given, make it a list
            if isinstance(objs, _type) or isinstance(objs, str) or isinstance(objs, dict):
                objs = [objs]

            # loop through list
            for obj in objs:
                if isinstance(obj, dict):  # happens when loading node, or passing node from cript.view().
                    if "_id" in obj.keys():   # happens when passing node from cript.view()
                        obj["uid"] = str(obj.pop("_id"))
                    obj_info = _type._create_reference(obj)

                    if obj_info["uid"] in current_uids:
                        msg = f"{_class} {obj['uid']} already in node."
                        CRIPTWarning(msg)
                        continue

                elif isinstance(obj, str):  # user may give just id as string -> just store string, will be expanded on database upload
                    if id_type_check(obj):
                        obj_info = obj

                        if obj_info in current_uids:
                            msg = f"{_class} {obj} already in node."
                            CRIPTWarning(msg)
                            continue

                elif isinstance(obj, _type):  # user may give a CRIPT node -> then extract dictionary
                    if obj.uid is None:
                        msg = f"{_class} '{obj.name}' needs to be saved before adding it to the node."
                        CRIPTWarning(msg)
                        continue

                    obj_info = obj._reference()   # Generates reference

                    if obj_info["uid"] in current_uids:
                        msg = f"{_class} {obj} already in node."
                        CRIPTWarning(msg)
                        continue

                else:
                    msg = f"{_class} {obj} not of type {_type}. Skipped."
                    CRIPTWarning(msg)
                    continue

                if getattr(self, f"_{prop}") is None:
                    setattr(self, f"_{prop}", [])

                exec(f"self._{prop}.append(obj_info)")


class CRIPTError(Exception):

    def __init__(self, message):
        self.message = message


class CRIPTWarning(Warning):

    def __init__(self, message):
        self.message = message
