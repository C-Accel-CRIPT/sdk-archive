from typing import Union, Any
from types import GenericAlias
from functools import wraps

from .. import CRIPTError

TYPE_OPTION_IN = Union[list[type], type]
TYPE_OPTION_INTERNAL = Union[list[type], list[list[type]]]


class TypeChecker(CRIPTError):
    """ This error is thrown if code has an error, not when data has an error."""
    pass


def type_check(*type_options: TYPE_OPTION_IN):
    """
    This is a decorator that can do type checking only two levels deep
    """
    def _type_check_decorator(func):
        @wraps(func)
        def _type_check(*args, **kwargs):
            _type_check_loop(args, type_options, func)
            return func(*args, **kwargs)
        return _type_check
    return _type_check_decorator


def _type_check_loop(args: Any, type_options, func):
    # skip first arg is "self" is the first argument.
    first_arg_self = _is_class_check(args[0])
    if first_arg_self:
        slice_ = slice(1, None)
    else:
        slice_ = slice(0, None)

    # loop through arguments and check them
    for i, arg in enumerate(args[slice_]):
        arg_type = _get_arg_type(arg)
        arg_options = _get_arg_options(type_options[i], args, func)

        if not _do_check(arg_type, arg_options):
            mes = f"Expected {arg_options} but got {arg_type} for: {func.__name__}."
            if hasattr(args[0], '_error'):
                raise args._error(mes)
            else:
                raise TypeError(mes)


def _is_class_check(arg: Any) -> bool:
    """ Check if arg is custom defined class. """
    if hasattr(arg, '__dict__'):
        return True

    return False


def _get_arg_type(arg: Any) -> list[type]:
    """ Convert arg to types. """
    if isinstance(arg, (list, tuple, dict)):
        return [type(arg), type(arg[0])]

    return [type(arg)]


def _get_arg_options(type_options: TYPE_OPTION_IN, args: Any, func) -> TYPE_OPTION_INTERNAL:
    """ Convert arg_options into type list. """
    if not isinstance(type_options, list):
        type_options = [type_options]

    options = []
    for type_op in type_options:
        if type_op == "self":
            options.append([type(args[0])])
        elif type_op == "list[self]":
            options.append([list, type(args[0])])
        elif isinstance(type_op, GenericAlias):
            options.append([type_op.__origin__, type_op.__args__[0]])
        elif isinstance(type_op, type):
            options.append([type_op])
        else:
            raise TypeChecker(f"Invalid 'type' passed to {func.__name__}. Invalid '{type_op}'. ")

    options.append([None])
    return options


def _do_check(arg_type: list[type], arg_options: TYPE_OPTION_INTERNAL) -> bool:
    """ Does actual type checking"""
    for i, arg_t in enumerate(arg_type):
        arg_op = [op[i] for op in arg_options if len(op) >= i+1]
        if arg_t not in arg_op:
            return False
    return True
