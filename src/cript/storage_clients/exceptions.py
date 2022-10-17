from cript.exceptions import CRIPTError


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
