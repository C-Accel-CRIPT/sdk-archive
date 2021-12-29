"""
General validation codes

"""

from .. import CRIPTError


def id_type_check(uid: str) -> bool:
    """Check if uid is a string and correct length. (returns True or throws an error)"""
    if type(uid) != str:
        msg = f"uids should be type 'str'. The provided uid is {type(uid)}."
        raise CRIPTError(msg)
    if len(uid) != 24:
        msg = f"uids are 24 letters or numbers long. The provided uid is {len(uid)} long."
        raise CRIPTError(msg)

    return True


def id_type_check_bool(uid: str) -> bool:
    """Check if uid is a string and correct length. (returns bool)"""
    try:
        return id_type_check(uid)
    except CRIPTError:
        return False
