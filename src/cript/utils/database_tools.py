from functools import wraps

from .. import CRIPTError


def login_check(func):
    """
    Check if user is logged in. (i.e. checks if CriptDB.user is has uid.)
    :param func:
    :return:
    """
    @wraps(func)
    def _login_check(*args, **kwargs):
        # if creating a user, allow!
        if args[0].user is None:
            try:
                if args[1].class_ == "User":
                    pass
                else:
                    raise AttributeError
            except AttributeError:
                raise CRIPTError("Login before trying to save. To login type: cript.CriptDB.user = 'your user id' ")

            value = func(*args, **kwargs)

            # Login user after creation
            args[0].user = value
            return value
        else:
            # if logged in, continue
            value = func(*args, **kwargs)
            return value

    return _login_check







#
# from functools import wraps
#
#
# def wrapper(func):
#     @wraps(func)
#     def _wrapper(*args, **kwargs):
#         # do something before
#         value = func(*args, **kwargs)
#         # do something after
#         return value
#     return _wrapper