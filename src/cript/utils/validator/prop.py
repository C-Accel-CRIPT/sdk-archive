from functools import wraps


def prop_keys_check(func):
    """
    Validates:
    key: if its a valid Key
    value: validates its in range
    """
    @wraps(func)
    def _cond_key_check(*args, **kwargs):
        # do something before
        #_cond_keys_check_switch(func.__name__, *args)
        value = func(*args, **kwargs)
        # do something after
        return value
    return _cond_key_check
