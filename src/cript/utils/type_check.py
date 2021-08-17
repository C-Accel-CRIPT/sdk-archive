from typing import get_type_hints, get_origin, _UnionGenericAlias, Union
from types import GenericAlias
from functools import wraps
import builtins
import warnings
from inspect import getmembers, isclass

import pint

import cript

builtin_types = {getattr(builtins, d).__name__: getattr(builtins, d) for d in dir(builtins) if isinstance(getattr(builtins, d), type) and "Error" not in getattr(builtins, d).__name__ and "Warning" not in getattr(builtins, d).__name__}
pint_types = {pair[0]: pair[1] for pair in getmembers(pint, isclass)}


def custom_formatwarning(msg, *args, **kwargs):
    return "Warning: " + str(msg) + '\n'


warnings.formatwarning = custom_formatwarning


def type_check(type_options: Union[tuple, type]):
    """
    This is a decorator that can do type checking only two levels deep
    """
    def _type_check_decorator(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            try:
                _do_check(*args, type_options, func)
            except Exception:
                pass

            return func(*args, **kwargs)
        return _wrapper
    return _type_check_decorator


def _do_check(args, type_options, func):

    arg =args[1]

    # arg pre- processing
    if isinstance(arg, (list, tuple, dict)):
        arg_generic = True
        arg_layer_1 = type(arg)
        if isinstance(arg, (list, tuple)):
            arg_layer_2 = type(arg[0])
        elif isinstance(arg, dict):
            arg_layer_2 = (type(list(arg.keys())[0]), type(list(arg.values())[0]))
    else:
        arg_generic = False

    # type_options pre-processing
    if type_options == "self" or type_options == "list[self]":
        type_options = type(args[0])
    elif "self" in type_options:
        new_type_op = []
        for t in type_options:
            if t == "self":
                new_type_op.append(type(args[0]))
            elif t == "list[self]":
                new_type_op.append(list[type(args[0])])
            else:
                new_type_op.append(t)

    # make input to tuple if not
    if isinstance(type_options, type):
        type_options = (type_options,)

    # make list to check for GenericAlias
    type_list = []  # 1: Generic, 0: not generic
    for i in type_options:
        if type(i) is GenericAlias:
            type_list.append(1)
        else:
            type_list.append(0)

    op_generic = any(type_list)

    # Options
    if arg_generic and op_generic:
        result = False
        for i in type_options:
            if type(i) is GenericAlias:
                layer_1 = get_origin(i)
                layer_2 = i.__args__
                if isinstance(arg_layer_1, layer_1):
                    if arg_layer_2 == layer_2:
                        result = True
                        break
    elif arg_generic:
        result = False
    elif op_generic:
        type_options = tuple([a for a,b in zip(type_options, type_list) if b])
        result = isinstance(arg, type_options)
    else:
        result = isinstance(arg, type_options)

    if not result:
        raise TypeError(f"Expected {type_options} but got {arg} for property: {func.__name__}.")


def type_check_property(func):
    """
    This is a decorator that can do type checking for a class property.
    :param func:
    :return:
    """
    @wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            # get variable type
            arg_type_op = get_type_hints(args[0].__init__)[func.__name__]

            # converter to builtin types, if needed
            if arg_type_op in builtin_types.values():
                pass
            elif type(arg_type_op) is _UnionGenericAlias:
                # unions and optionals
                arg_type_op = parse_generic_type(str(arg_type_op))
            elif type(arg_type_op) is GenericAlias:
                arg_type_op = parse_generic_alias_type(str(arg_type_op))
            else:
                raise KeyError

            # get arg type tree
            if args[1] is None:
                arg_type = {None: ""}
            else:
                arg_type = get_arg_types(args[1])

            # do check
            check = do_type_check(arg_type, arg_type_op)
            if check is TypeError:
                raise TypeError(f"Expected {arg_type_op} but got {arg_type} for property: {func.__name__}.")

        except KeyError:
            warnings.warn(f"No type hint provided for {func.__name__}, so type check not possible.")

        # if pass type check, run function
        return func(*args, **kwargs)
    return _wrapper


def do_type_check(arg_type: dict, arg_type_op):
    """
    Does actual type check
    :param arg_type:
    :param arg_type_op:
    :return:
    """

    # get the level arg types
    current_types = list(arg_type.keys())

    # get the level type options
    if type(arg_type_op) == dict:
        current_options = []
        next_options = []
        for i in arg_type_op.values():
            if type(i) == list:
                current_options.append(list)
                next_options.append(i)
            else:
                current_options.append(i)
    elif type(arg_type_op) == list:
        current_options = [list]
    else:
        current_options = [arg_type_op]

    # do check between the two, throw error or move to next level ; stop if all values == ""
    if all(item in current_options for item in current_types):

        # find next arg type dict for next level
        for v in arg_type.values():
            if v != "":
                next_type = v

                state = TypeError
                for option in next_options:
                    back = do_type_check(next_type, option[1])
                    if back is None:
                        return None
            else:
                return None

    return TypeError


def get_arg_types(arg) -> dict:
    """
    Takes in any argument and returns a nested dictionary of data types.
    {list:
        {
        int: "",
        str: "",
        }
    }

    :param arg:
    :return: nested dictionary
    """

    type_out = type(arg)

    if type_out in builtin_types.values() or\
            type_out in pint_types.values() or\
            type_out in cript.cript_types.values():
        return {type_out: ""}

    if type_out == list or type_out == tuple:
        list_type = {}
        for i in arg:
            if type(i) not in list_type.keys():
                list_type.update(get_arg_types(i))
        return {type_out: list_type}

    if type_out == dict:
        pass
    if type_out == set:
        pass


def parse_generic_type(text_in: str):
    """
    This will parse a type hint that contains typing parameters and convert Unions to dictionaries,
    and Optionals (Compound objects) to lists with the first element being the highest element in the tree and the
    last element as the base element.

    Unions:
    {
        1: "type 1",
        2: "type 2",
        ...
    }

    Optional:
    ["first type",...,"last type"]

    :param text_in:
    :return:
    """
    text_in = text_in[7:]  # strips the first "typeing."
    if text_in[0] == "O":
        type_out = parse_generic_type_optional(text_in)

        # Add None as option
        type_out = {1: type_out, 2: None}

    elif text_in[0] == "U":
        type_out = parse_generic_type_union(text_in)

    else:
        warnings.warn(f"Type check not valid. {text_in}")
        return None

    return type_out


def parse_generic_type_union(text_in: str) -> dict:
    """
    Given a string like: Union[float, str, int, NoneType] return dict of types
    :param text_in:
    :return:
    """
    text_in = text_in[6:]  # strips "Union["
    types_list = []
    word = ""
    bracket_counter = 0  # it counts up when it sees [ and should count down to zero when it closes them all
    nesting = False  # used if another typing class found.
    for letter in text_in:
        if nesting:
            word = word + letter
            if letter == "[":
                bracket_counter += 1
            if letter == "]":
                bracket_counter -= 1
                if bracket_counter == 0:
                    nesting = False
        else:
            if letter == " ":
                pass
            elif letter == "," or letter == "]":
                types_list.append(word)
                word = ""
            else:
                word = word + letter
                if word == "typing." or word == "list[":
                    nesting = True
                    bracket_counter = 0

    # catches the situation where typing object is last in the list
    if word != "":
        types_list.append(word)

    type_out = {}
    for i, text in enumerate(types_list):
        type_out[i] = text_to_type(text)

    return type_out


def parse_generic_type_optional(text_in: str) -> list:
    """
    Given string like: Optional[list[cript.base.Prop]] return list of types
    :param text_in:
    :return:
    """
    text_in = text_in[9:-1]  # strips "Optional[" and "]"

    if "[" not in text_in:
        return text_to_type(text_in)

    types_list = []
    word = ""
    for letter in text_in:
        if letter == "[":
            types_list.append(word)
            types_list.append(text_in[len(word)+1:-1])  # +1 removes "[" ;  the -1 removes "]"
            break
        else:
            word = word + letter

    type_out = []
    for text in types_list:
        type_out.append(text_to_type(text))

    return type_out


def parse_generic_alias_type(text_in: str):

    types_list = []
    word = ""
    bracket_counter = 0  # it counts up when it sees [ and should count down to zero when it closes them all
    nesting = False  # used if another typing class found.
    for letter in text_in:
        if letter == "[":
            bracket_counter += 1
            types_list.append(word)
            word = ""
        elif letter == "]":
            if word != "":
                types_list.append(word)
            bracket_counter -= 1
        else:
            word = word + letter

    type_out = {}
    for i, text in enumerate(types_list):
        type_out[i] = text_to_type(text)

    return type_out


def text_to_type(text: str):
    """
    Convert string to type
    :param text:
    :return:
    """
    if text in builtin_types.keys():
        return builtin_types[text]
    elif text == "NoneType":
        return None
    elif text.startswith("typing."):
        return parse_generic_type(text)
    elif text.startswith("cript.") and text.split(".")[-1] in cript.cript_types.keys():
        return cript.cript_types[text.split(".")[-1]]
    # elif text.startswith("pint.") and text.split(".")[-1] in pint_types.keys():
    #     return pint_types[text.split(".")[-1]]
    else:
        warnings.warn(f"Type check not valid. {text}")
        return None


def id_type_check(uid: str):
    if type(uid) != str:
        msg = f"uids should be type 'str'. The provided uid is {type(uid)}."
        raise cript.CRIPTError(msg)
    if len(uid) != 24:
        msg = f"uids are 24 letters or numbers long. The provided uid is {len(uid)} long."
        raise cript.CRIPTError(msg)

    return True


def id_type_check_bool(uid: str) -> bool:
    try:
        return id_type_check(uid)
    except cript.CRIPTError:
        return False
