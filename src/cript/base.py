from abc import ABC
from bson import ObjectId
from json import dumps
from typing import Union
from datetime import datetime
import warnings

from pint.unit import Unit

from . import __version__
from .utils.serializable import Serializable
from .utils.type_check import *


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
        :param name: The name of the user.

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
        """
        keys = ["uid", "name"]
        out = {}
        for key in keys:
            out[key] = ddict[key]

        return out

    def _setter_CRIPT_prop(self, objs, prop: str):
        """
        This can set CRIPT properties
        :param objs: List of CRIPT objects or List of Lists of strings to add to prop
        :param prop: The property to be set
        :return:
        """
        _class = prop[2:]  # strip "c_"
        _type = cript.cript_types[_class.capitalize()]

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
                        warnings.warn(msg, CRIPTWarning)
                        continue

                elif isinstance(obj, str):  # user may give just id as string -> just store string, will be expanded on database upload
                    if id_type_check(obj):
                        obj_info = obj

                        if obj_info in current_uids:
                            msg = f"{_class} {obj} already in node."
                            warnings.warn(msg, CRIPTWarning)
                            continue

                elif isinstance(obj, _type):  # user may give a CRIPT node -> then extract dictionary
                    if obj.uid is None:
                        msg = f"{_class} '{obj.name}' needs to be saved before adding it to the node."
                        warnings.warn(msg, CRIPTWarning)
                        continue

                    obj_info = obj._reference()   # Generates reference

                    if obj_info["uid"] in current_uids:
                        msg = f"{_class} {obj} already in node."
                        warnings.warn(msg, CRIPTWarning)
                        continue

                else:
                    msg = f"{_class} {obj} not of type {_type}. Skipped."
                    warnings.warn(msg, CRIPTWarning)
                    continue

                if getattr(self, f"_{prop}") is None:
                    setattr(self, f"_{prop}", [])

                exec(f"self._{prop}.append(obj_info)")


class Cond(Serializable):
    def __init__(
            self,
            key: str = None,
            value: Union[float, str, int] = None,
            unit: Unit = None,
            uncer: Union[float, str] = None,
            data_uid=None,
    ):
        """

        :param key: time, temp, pres, solvent, standard, relative, atmosphere
        :param unit:
        """

        self._key = None
        self.key = key

        self._value = None
        self.value = value

        self._unit = None
        self.unit = unit

        self._uncer = None
        self.uncer = uncer

        self._data_uid = None
        self.data_uid = data_uid

    @property
    def key(self):
        return self._key

    @key.setter
    @type_check_property
    def key(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    @type_check_property
    def value(self, value):
        self._value = value

    @property
    def unit(self):
        return self._unit

    @unit.setter
    @type_check_property
    def unit(self, unit):
        self._unit = unit

    @property
    def uncer(self):
        return self._uncer

    @uncer.setter
    @type_check_property
    def uncer(self, uncer):
        self._uncer = uncer

    @property
    def data_uid(self):
        return self._data_uid

    @data_uid.setter
    @type_check_property
    def data_uid(self, data_uid):
        self._data_uid = data_uid


class Prop(Serializable):
    def __init__(
            self,
            key: str,
            value: Union[float, int, str],
            unit: Unit = None,
            uncer: Union[float, int, str] = None,
            method: str = None,
            mat_id: int = None,
            component: str = None,
            data_uid: str = None,
            conditions: list[Cond] = None
    ):
        """

        :param mat_id:
        :param key:
        :param value:
        :param uncer:
        :param unit:
        :param component:
        :param method:
        :param data_uid:
        :param conditions:
        """

        self._mat_id = None
        self.mat_id = mat_id

        self._key = None
        self.key = key

        self._value = None
        self.value = value

        self._uncer = None
        self.uncer = uncer

        self._unit = None
        self.unit = unit

        self._component = None
        self.component = component

        self._method = None
        self.method = method

        self._data_uid = None
        self.data_uid = data_uid

        self._conditions = None
        self.conditions = conditions

    @property
    def mat_id(self):
        return self._mat_id

    @mat_id.setter
    @type_check_property
    def mat_id(self, mat_id):
        self._mat_id = mat_id

    @property
    def key(self):
        return self._key

    @key.setter
    @type_check_property
    def key(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    @type_check_property
    def value(self, value):
        self._value = value

    @property
    def uncer(self):
        return self._uncer

    @uncer.setter
    @type_check_property
    def uncer(self, uncer):
        self._uncer = uncer

    @property
    def unit(self):
        return self._unit

    @unit.setter
    @type_check_property
    def unit(self, unit):
        self._unit = unit

    @property
    def component(self):
        return self._component

    @component.setter
    @type_check_property
    def component(self, component):
        self._component = component

    @property
    def method(self):
        return self._method

    @method.setter
    @type_check_property
    def method(self, method):
        self._method = method

    @property
    def data_uid(self):
        return self._data_uid

    @data_uid.setter
    @type_check_property
    def data_uid(self, data_uid):
        self._data_uid = data_uid

    @property
    def conditions(self):
        return self._conditions

    @conditions.setter
    @type_check_property
    def conditions(self, conditions):
        self._conditions = conditions


class CRIPTError(Exception):

    def __init__(self, message):
        self.message = message


class CRIPTWarning(Warning):

    def __init__(self, message):
        self.message = message


def load(ddict: dict):
    ddict["uid"] = str(ddict.pop("_id"))
    class_ = ddict.pop("class_")
    obj = cript.cript_types[class_](**ddict)
    return obj
