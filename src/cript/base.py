from abc import abstractmethod
from typing import Union
from bson.objectid import ObjectId
from json import dumps

from src.cript import __version__
from src.cript.utils.serializable import Serializable


class BaseAttributeError(Exception):
    pass


class BaseModelError(Exception):
    pass


class BaseModel(Serializable, object):
    """Base (abstract) class to represent a data model.
    Parameters
    ----------
    name: str, required
        User specific name of the node.
    notes: str, optional
        A free form space to add non-property information.
    """

    def __init__(
        self,
        name: str,
        _class: str = None,
        notes: str = None
    ):

        self._name = None
        self.name = name

        self._notes = None
        self.notes = notes

        self._class_ = _class

        self._uid = None
        self._model_version = __version__
        self._version_control = None
        self._last_modified_date = None
        self._created_date = None

    def __repr__(self):
        return dumps(self._to_dict(self), indent=2, sort_keys=True)

    @property
    def name(self):
        """User specific name of the node."""
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def notes(self):
        """ A free form space to add non-property information."""
        return self._notes

    @notes.setter
    def notes(self, notes):
        self._notes = notes

    @property
    def uid(self):
        """Unique ID of the node."""
        return self._uid

    @property
    def class_(self):
        """Version of the data model."""
        return self._class_

    @property
    def model_version(self):
        """Version of the data model."""
        return self._model_version

    @property
    def version_control(self):
        """Version control reference of the data model."""
        return self._version_control

    @property
    def last_modified_date(self):
        """Date the node was last modified."""
        return self._last_modified_date

    @property
    def created_date(self):
        """Date the node was created."""
        return self._created_date




class BaseAttribute:
    """Base class to represent an attribute.
    Parameters
    ----------
    key: str, required
        The attribute type.
    value: float, required
        The numerical value of the attribute.
    units: str, required
        The units of value.
    uncertainty: float, optional
        The uncertainty in the quantity value.
    method: str, optional
        The method with which the attribute was determined.
    notes: str, optional
        Any miscellaneous text notes related to the attribute.
    """

    def __init__(
        self,
        key: str = None,
        value: float = None,
        units: str = None,
        uncertainty: float = None,
        method: str = None,
        notes: str = None,
    ):
        super().__init__(notes=notes)

        self._key = None
        self.key = key

        self._value = None
        self.value = value

        self._units = None
        self.units = units

        self._uncertainty = None
        self.uncertainty = uncertainty

        self._method = None
        self.method = method

    def __repr__(self):
        """Text friendly representation of the attribute."""
        typ = self.__class__.__name__
        if self.uncertainty:
            return f"{typ} <{self.value} +/- {self.uncertainty} (Units: {self.units})>"
        else:
            return f"{typ} <{self.value} (Units: {self.units})>"

    @property
    @abstractmethod
    def supported_keys(self):
        """List of attribute keys with built-in units/range-validation support."""
        raise NotImplementedError

    @property
    def key(self):
        """Attribute key."""
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @property
    def value(self):
        """Attribute value."""
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def units(self):
        """Units of attribute value."""
        return self._units

    @units.setter
    def units(self, units):
        self._units = units

    @property
    def uncertainty(self):
        """Uncertainty in attribute value."""
        return self._uncertainty

    @uncertainty.setter
    def uncertainty(self, uncertainty):
        self._uncertainty = uncertainty

    @property
    def method(self):
        """Method of determination of attribute value."""
        return self._method

    @method.setter
    def method(self, method):
        self._method = method