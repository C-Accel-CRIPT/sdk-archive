
import re
from functools import wraps

from .. import CRIPTError


_error = CRIPTError


def email_format_check(func):
    """
    Check email is text@text.text
    """
    @wraps(func)
    def _email_format_check(*args, **kwargs):
        email = args[1]
        if email is not None:
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if not re.match(regex, email):
                msg = f"Email {email} not of correct format. (format: text@text.text)"
                if hasattr(args[0], "_error"):
                    raise args[0]._error(msg)
                else:
                    global _error
                    raise _error

        value = func(args[0], email)
        return value
    return _email_format_check


def phone_format_check(func):
    """
    Check phone format
    """
    @wraps(func)
    def _phone_format_check(*args, **kwargs):
        phone = args[1]
        if phone is not None:
            if re.match(r'[0-9]{10}', phone):
                phone = phone[0:3] + "-" + phone[3:6] + "-" + phone[6:]
            elif re.match(r'[0-9|-]{12}', phone):
                pass
            else:
                msg = f"Phone number {phone} not of correct format. (format: numbers and dash only)"
                if hasattr(args[0], "_error"):
                    raise args[0]._error(msg)
                else:
                    global _error
                    raise _error

        value = func(args[0], phone)
        return value
    return _phone_format_check


def orcid_format_check(func):
    """
    Check orcid format   ####-####-####-####
    """
    @wraps(func)
    def _orcid_format_check(*args, **kwargs):
        orcid = args[1]
        if orcid is not None:
            if re.match(r'[0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{4}', orcid):
                pass
            elif re.match(r'[0-9]{16}', orcid):
                orcid = orcid[0:4] + "-" + orcid[4:8] + "-" + orcid[8:12] + "-" + orcid[12:]
            else:
                msg = f"{orcid} invalid format, and not added to user node. (format: ####-####-####-####)"
                if hasattr(args[0], "_error"):
                    raise args[0]._error(msg)
                else:
                    global _error
                    raise _error

        value = func(args[0], orcid)
        return value

    return _orcid_format_check
