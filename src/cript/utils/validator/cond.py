from functools import wraps
from difflib import get_close_matches

from pint.errors import DimensionalityError

from ... import CRIPTError, Quantity


def cond_keys_check(func):
    """
    Validates:
    key: if its a valid Key
    value: validates its in range
    :return:
    """
    @wraps(func)
    def _cond_key_check(*args, **kwargs):
        if args[1] is not None:
            _cond_keys_check_switch(func.__name__, *args)
        value = func(*args, **kwargs)
        return value
    return _cond_key_check


def _cond_keys_check_switch(param, *args):
    """
    Switches between key, value
    :param args: args[0] is 'self'; args[1] is key, or value
    :return: either return args[1] as is, or in database approved units
    """
    if param == "key":
        return _cond_keys_check_key(*args)
    elif args[0].key is not None:
        if param == "value":
            if "+" not in args[0].key:
                return _cond_keys_check_value(*args)
            else:
                return  # no checks on custom conditions
        elif param == "uncer":
            if "+" not in args[0].key:
                return _cond_keys_check_uncer(*args)
            else:
                return  # no checks on custom conditions
        else:
            mes = f"This decorator does not support '{param}'."
            CRIPTError(mes)
    else:
        mes = f"'key' needs to be defined before '{param}'."
        CRIPTError(mes)


def _cond_keys_check_key(*args):
    if isinstance(args[1], str):
        if args[1] in args[0].keys.keys() or args[1][0] == "+":
            return
        else:
            table = _recommendation_table(*args)
            mes = f" {args[1]} is not a official CRIPT condition.\nWere you trying to enter:" + table + \
                  "\nOtherwise add a '+' (plus symbol) in front of your key to signify a custom condition."
            raise CRIPTError(mes)
    else:
        raise TypeError(f"The 'key' for CRIPT.Cond must be string. Invalid: {args[1]}")


def _recommendation_table(*args) -> str:
    best_guess = get_close_matches(args[1], list(args[0].keys.keys()), cutoff=0.4)
    if best_guess is []:
        return ""
    else:
        row_format = "{:<20}" * 2 + "{:<50}"
        text_out = "\n"
        text_out = text_out + "\n" + row_format.format("key", "unit", "descr")
        text_out = text_out + "\n" + "-" * 60
        for i in best_guess:
            text_out = text_out + "\n" + row_format.format(i, args[0].keys[i]["unit"], args[0].keys[i]["descr"])
        text_out = text_out + "\n"

    return text_out


def _cond_keys_check_value(*args):
    """
    Given a 'value' do type, range, and unit check.
    :param args: args[0] is 'self'; args[1] is new value
    :return:
    """
    type_ = args[0].keys[args[0].key]["type"]
    range_ = args[0].keys[args[0].key]["range"]
    unit_ = args[0].keys[args[0].key]["unit"]

    if isinstance(args[1], type_):
        pass
    else:
        mes = f"Invalid 'value' type provided for {args[0].key}. Expected: {type_}; Received: {type(args[1])}"
        raise TypeError(mes)

    if type_ == str:
        if not range_:  # no range check
            return
        elif isinstance(range_[0], int) and range_[0] <= len(args[1]) <= range_[1]:  # text length check
            return
        elif isinstance(range_[0], str) and args[1] in range_:  # multiple string options
            return
        else:
            mes = f"'Value' outside expected range for {args[0].key}. Expected: {range_}; Received: {args[1]}"
            raise ValueError(mes)

    elif type_ == float or type_ == int:
        if range_[0] <= args[1] <= range_[1]:
            return
        else:
            mes = f"'Value' outside expected range for {args[0].key}. Expected: {range_}; Received: {args[1]}"
            raise ValueError(mes)

    elif type_ == Quantity:
        try:
            new_arg = args[1].to(unit_)  # Unit Conversion
        except DimensionalityError:
            mes = f"Wrong units provided for {args[0].key}. Expected: {unit_} or similar dimensionality; " \
                 f"Received: {args[1].units}"
            raise CRIPTError(mes)
        if range_[0] <= new_arg.magnitude <= range_[1]:  # range check
            return
        else:
            mes = f"'Value' outside expected range for {args[0].key}. Expected: {range_}; Received: {args[1]}"
            raise ValueError(mes)


def _cond_keys_check_uncer(*args):
    type_ = args[0].keys[args[0].key]["type"]
    unit_ = args[0].keys[args[0].key]["unit"]

    if isinstance(args[1], type_):
        pass
    else:
        mes = f"Invalid 'uncertainty' type provided for {args[0].key}. Expected: {type_}; Received: {type(args[1])}"
        raise TypeError(mes)

    if type_ == str:
        return

    elif type_ == float or type_ == int:
        return

    elif type_ == Quantity:
        try:
            new_arg = args[1].to(unit_)  # Unit Conversion
        except DimensionalityError:
            mes = f"Wrong units provided for {args[0].key}. Expected: {unit_} or similar dimensionality; " \
                 f"Received: {args[1].units}"
            raise CRIPTError(mes)
