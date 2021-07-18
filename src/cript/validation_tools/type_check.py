from typing import get_type_hints
from functools import wraps
import builtins
import warnings
from sys import modules
from inspect import getmembers, isclass

import cript   # in use, just not recognized by pycharm

builtin_types = {getattr(builtins, d).__name__: getattr(builtins, d) for d in dir(builtins) if isinstance(getattr(builtins, d), type) and "Error" not in getattr(builtins, d).__name__ and "Warning" not in getattr(builtins, d).__name__}
cript_types = {pair[0]: pair[1] for pair in getmembers(cript, isclass)}


def type_check_property(func):
    """
    This is a decorator that can do type checking for a class property.
    :param func:
    :return:
    """
    @wraps(func)
    def _wrapper(*args, **kwargs):
        # get variable type
        arg_type = get_type_hints(args[0].__init__)[func.__name__]

        # converter to builtin types, if needed
        if arg_type in builtin_types.values():
            pass
        else:
            # generic types need parsing
            arg_type = parse_generic_type(str(arg_type))

        # get arg type tree
            if args[1] is None:
                arg_type_op= type(None)
            else:
                arg_type_op = get_arg_types(args[1])

        # do check
        check = do_type_check(arg_type_op, arg_type)
        if check is TypeError:
            raise TypeError(f"Expected {arg_type_op} but got {arg_type} for property: {func.__name__}.")

        # if pass type check, run function
        return func(*args, **kwargs)
    return _wrapper


def do_type_check(var_type, arg_type: dict):
    # get the level arg types
    current_type = list(arg_type.keys())

    # get the level type options
    if type(var_type) == dict:
        current_options = []
        next_options = []
        for i in var_type.values():
            if type(i) == list:
                current_options.append([list])
                next_options.append(i)
            else:
                current_options.append(i)
    elif type(var_type) == list:
        current_options = [list]
    else:
        current_options = [var_type]

    # do check between the two, throw error or move to next level ; stop if all values == ""
    if current_type in current_options:

        # find next arg type dict for next level
        for v in arg_type.values():
            if v != "":
                next_type = v

                state = TypeError
                for option in next_options:
                    back = do_type_check(option[1], next_type)
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

    if type_out in [int, float, str, bool, bytes] or type_out in cript_types.values():
        return {type_out: ""}

    if type_out == list or type_out[0] == tuple:
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
    elif text_in[0] == "U":
        type_out = parse_generic_type_union(text_in)
    else:
        warnings.warn(f"Type check not valid. {text_in}")
        return None

    return type_out


def parse_generic_type_union(text_in: str) -> dict:
    """
    Given a string like: Union[float, str, int, NoneType] return list of types
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
                if word == "typing.":
                    nesting = True
                    bracket_counter = 0

    # catches the situation where typing object is last in the list
    if word != "":
        types_list.append(word)

    type_out = {}
    for i, text in enumerate(types_list):
        if text in builtin_types.keys():
            type_out[i] = builtin_types[text]
        elif text == "NoneType":
            type_out[i] = None
        elif text.startswith("typing."):
            type_out[i] = parse_generic_type(text)
        elif text.startswith("cript."):
            exec(f"type_out[{i}] = " + text)
        else:
            warnings.warn(f"Type check not valid2. {text}")
            return None
    return type_out


def parse_generic_type_optional(text_in: str) -> list:
    """
    Given string like: Optional[list[cript.base.Prop]] return list of types
    :param text_in:
    :return:
    """
    text_in = text_in[9:-1]  # strips "Optional[" and "]"
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
        if text in builtin_types.keys():
            type_out.append(builtin_types[text])
        elif text == "NoneType":
            type_out.append(None)
        elif text.startswith("typing."):
            type_out.append(parse_generic_type(text))
        elif text.startswith("cript."):
            exec("type_out.append(" + text + ")")
        else:
            warnings.warn(f"Type check not valid2. {text}")
            return None
    return type_out


if __name__ == '__main__':
    test_text = "typing.Union[" \
                "float," \
                " str," \
                " int," \
                " NoneType," \
                " typing.Optional[list[str]]," \
                " typing.Optional[list[cript.base.Prop]]," \
                " cript.base.Prop," \
                " typing.Optional[list[typing.Union[str, int]]]" \
                "]"
    print(parse_generic_type(test_text))

    c = parse_generic_type("typing.Optional[list[typing.Union[int, typing.Optional[list[typing.Union[str, cript.base.Prop]]]]]")
    test_variable = [1, 2, ["hi", "fish", cript.base.Prop(key="bp", value=100)]]
    b = get_arg_types(test_variable)
    print(b)

    print(do_type_check(c, b))
