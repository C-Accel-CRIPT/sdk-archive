from typing import Protocol, Any, Union
from types import GenericAlias
from functools import wraps
from difflib import get_close_matches

from pint.errors import DimensionalityError

from .. import CRIPTError, Quantity


class SupportsKeyCheck(Protocol):
    keys: dict = None
    key: str = None
    value: Any = None


def keys_check(keys: dict = None):
    """ Key checks

    Checks to see if keyword is in CRIPT official keyword list, or the key has a 'plus' or '+' at the beginning.

    Parameters
    ----------
    keys: dict
        A key table can be provided or it will default to the class key list.

    """
    # build key table object if keys passed in.
    if keys is not None:
        obj = SupportsKeyCheck()
        obj.keys = keys
    else:
        obj = None

    def keys_check_decorator(func):
        @wraps(func)
        def _key_check(self: SupportsKeyCheck, key):
            if key is not None:
                if obj is not None:
                    self = obj
                do_key_check(self, key)
            value = func(self, key)
            return value
        return _key_check
    return keys_check_decorator


def do_key_check(self: SupportsKeyCheck, key: Union[list[str], str]):
    """

    Parameters
    ----------
    self: SupportsKeyCheck
        class that key is being added to
    key: str
        key to be checked

    """
    if isinstance(key, list):
        for k in key:
            do_key_check(self, k)  # recursion!
    elif isinstance(key, str):
        if key in self.keys or key.startswith(("plus", "+")):
            return
        else:
            mes = f" {key} is not a official CRIPT {self.__name__}.\n " \
                  f"Did you mean: {key_recommendation(key, list(self.keys.keys()))}\n" \
                  f"You can also check the official key list with '{self.__name__}.key_table'.\n" \
                  "Otherwise add a '+' (plus symbol) in front of your key to signify a custom condition."
            raise CRIPTError(mes)
    else:
        raise TypeError(f"The 'key/keyword' for CRIPT must be string. Invalid: {key} ({type(key)})")


def value_check(func):
    """ value checks

    """
    @wraps(func)
    def _value_check(self: SupportsKeyCheck, value):
        if value is not None:
            do_value_check(self, value)
        value = func(self, value)
        return value
    return _value_check


def do_value_check(self, value):
    """
    """
    # guard statements
    if self.key is None:
        mes = f"'key' needs to be defined first."
        raise CRIPTError(mes)

    if self.key.startswith(("plus", "+")):
        return  # no checks on custom conditions

    type_ = self.key.key_dict["type"]

    if hasattr(type_, "class_"):
        type_ = (type_, dict)

    if isinstance(type_, GenericAlias):
        _value_check_generic(self, value)
        return

    if not isinstance(value, type_):
        mes = f"Invalid 'value' type provided for {self.key}. Expected: {type_}; Received: {type(value)}"
        raise TypeError(mes)

    # Does other type specific checks
    if type_ == str:
        _value_str_check(self, value)
    elif type_ == float or type_ == int:
        _value_num_check(self, value)
    elif type_ == Quantity:
        _value_quantity_check(self, value)
    else:
        pass  # other types have no checks


def _value_str_check(self, value: str):
    """ Checks value of strings. """
    range_ = self.key.key_dict["range"]

    if not range_:  # no range check
        return
    elif isinstance(range_[0], int) and range_[0] <= len(value) <= range_[1]:  # text length check
        return
    elif isinstance(range_[0], str) and value in range_:  # multiple string options
        return
    else:
        mes = f"'Value' outside expected range for {self.key}. Expected: {range_}; Received: {value}"
        raise ValueError(mes)


def _value_num_check(self, value: Union[int, float]):
    """ Checks value of numbers. """
    range_ = self.key.key_dict["range"]

    if range_[0] <= value <= range_[1]:
        return
    else:
        mes = f"'Value' outside expected range for {self.key}. Expected: {range_}; Received: {value}"
        raise ValueError(mes)


def _value_quantity_check(self, value: Quantity):
    """ Checks value of quantities. """
    range_ = self.key.key_dict["range"]
    unit_ = self.key.key_dict["unit"]

    # Check units
    try:
        new_arg = value.to(unit_)  # Unit Conversion
    except DimensionalityError:
        mes = f"Wrong units provided for {self.key}. Expected: {unit_} or similar dimensionality; " \
              f"Received: {value.units}"
        raise CRIPTError(mes)

    # Check range
    if range_[0] <= new_arg.magnitude <= range_[1]:
        return
    else:
        mes = f"'Value' outside expected range for {self.key}. Expected: {range_}; Received: {value}"
        raise ValueError(mes)


def _value_check_generic(self, value: Union[list, tuple]):
    """ Handles GenericAlias types. Which means its a list or tuple of something."""

    # do type check
    type_ = self.key.key_dict["type"]
    split_type = [type_.__origin__, type_.__args__[0]]  # convert generic to real types

    if not isinstance(value, split_type[0]) and not all(isinstance(v, split_type[1]) for v in value):
        mes = f"Invalid 'value' type provided for {self.key}. Expected: {type_}; Received: {type(value)}"
        raise TypeError(mes)

    # do range and unit checks
    for v in value:
        if isinstance(v, str):
            _value_str_check(self, v)
        elif isinstance(v, int):
            _value_num_check(self, v)
        elif isinstance(v, Quantity):
            _value_quantity_check(self, v)


def key_recommendation(guess: str, possibilities: list) -> str:
    """ Given a bad key suggest nearest options. """
    best_guess = get_close_matches(guess, possibilities, cutoff=0.4, n=3)
    if best_guess is []:
        return ""

    return ", ".join(best_guess)
