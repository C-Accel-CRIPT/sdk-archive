from functools import wraps
from datetime import datetime
from pathlib import Path

from bson import ObjectId

from .. import Unit


def freeze_class(cls):
    """
    This class decorator prevents the addition of new attribute to the class after __init__.
    """
    cls.__frozen = False

    def frozensetattr(self, key, value):
        if self.__frozen and not hasattr(self, key):
            raise self._error("Class '{}' is frozen. Cannot set '{} = {}'"
                  .format(cls.__name__, key, value))
        else:
            object.__setattr__(self, key, value)

    def init_decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.__frozen = True
        return wrapper

    cls.__setattr__ = frozensetattr
    cls.__init__ = init_decorator(cls.__init__)

    return cls


def convert_to_list(func):
    """
    This function decorator allows user to enter a single attribute and it will automatically convert it to a list.
    """
    @wraps(func)
    def _convert_to_list(*args):
        # skip first arg (it is self)
        if not isinstance(args[1], (list, tuple)):
            args = list(args)
            args[1] = [args[1]]
        return func(*args)
    return _convert_to_list


def loading_with_units(type_):
    """
    This function decorator allows user to enter a single parameter and it will automatically convert it to a list.
    """
    def loading_with_units_decorator(func):
        @wraps(func)
        def _loading_with_units(*args):
            if isinstance(args[0], list) and isinstance(args[0][0], dict):
                # if args[0][0] is a dict it must be loading from the database, otherwise its a CRIPT node.
                args = list(args)
                for i, s in enumerate(args[1]):
                    args[1][i] = type_(**s, _loading=True)
            return func(*args)
        return _loading_with_units
    return loading_with_units_decorator


def loading_with_datetime(func):
    """ Converts datetime str into DateTime object. """
    @wraps(func)
    def _loading_with_datetime(*args):
        if isinstance(args[1], str):
            args = list(args)
            args[1] = datetime.fromisoformat(args[1])
        return func(*args)
    return _loading_with_datetime


def str_to_unit(func):
    """ Converts str into Unit object. """
    @wraps(func)
    def _str_to_unit(*args):
        if isinstance(args[1], list):
            args = list(args)
            for i, arg in enumerate(args):
                args[1][i] = Unit(arg)
        return func(*args)
    return _str_to_unit


def str_to_path(func):
    """ Converts datetime str into datetime object. """
    @wraps(func)
    def _str_to_path(*args):
        if isinstance(args[1], str):
            args = list(args)
            args[1] = Path(args[1])
        return func(*args)
    return _str_to_path


def str_to_ObjectId(func):
    """ Converts  str into ObjectId object. """
    @wraps(func)
    def _str_to_ObjectId(*args):
        if isinstance(args[1], str):
            args = list(args)
            args[1] = ObjectId(args[1])
        return func(*args)
    return _str_to_ObjectId

