



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
        output = _cond_keys_check_switch(func.__name__, *args)
        value = func(args[0], output)
        # do something after
        return value
    return _cond_key_check