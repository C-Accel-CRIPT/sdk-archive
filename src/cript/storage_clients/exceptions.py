from cript.exceptions import CRIPTError


class InvalidAuthCode(CRIPTError):
    """
    Raised when an Authentication code to connect to a storage client is invalid
    """

    def __init__(self):
        pass

    def __str__(self):
        return "Unable to authenticate with storage client. Please use a valid authentication code"


class FileUploadError(CRIPTError):
    """Raised when a file upload fails."""

    def __init__(self):
        pass

    def __str__(self):
        return "File upload could not be completed."


class FileDownloadError(CRIPTError):
    """Raised when a file download fails."""

    def __init__(self):
        pass

    def __str__(self):
        return "File download could not be completed."
