from functools import wraps
from difflib import get_close_matches

from ... import CRIPTError


def cond_keys_check(func):
    """
    Validates:
    key: if its a valid Key
    value: validates its in range
    :return:
    """
    @wraps(func)
    def _cond_key_check(*args, **kwargs):
        # do something before
        _cond_keys_check_switch(func.__name__, *args)
        value = func(*args, **kwargs)
        # do something after
        return value
    return _cond_key_check


def _cond_keys_check_switch(param, *args):
    if param == "key":
        _cond_keys_check_key(*args)
    elif args[0].key is not None:
        if param == "value":
            _cond_keys_check_value(*args)
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
        TypeError(f"The 'key' for CRIPT.Cond must be string. Invalid: {args[1]}")


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


def _cond_keys_check_value(args):
    type_ = args[0].keys[args[0].key]["type"]
    if isinstance(args[1], type_):
        range = args[0].keys[args[0].key]["range"]
        if isinstance(type_, list):
            if args[1] in args[0].keys.keys():
                return
            else:
                table = _recommendation_table(args)
                mes = f" {args[1]} is not a official CRIPT condition.\n Were you trying to enter:" + table + \
                      "Otherwise add a '+' (plus symbol) in front of your key to signify a custom condition."
    else:
        TypeError(f"The 'key' for CRIPT.Cond must be string. Invalid: {args[1]}")
