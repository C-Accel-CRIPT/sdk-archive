from typing import Union
from bson import ObjectId
from pathlib import Path


from ..utils import SerializableSub, freeze_class


@freeze_class
class File(SerializableSub):
    """

    :param path: file path
    :param descr: description
    :param ext: file extension
    """

    def __init__(
            self,
            path: Union[str, Path] = None,
            # labels: str = None,
            # units: str = None,
            descr: str = None,
            file_name: str = None,
            ext: str = None,
            uid: Union[str, ObjectId] = None
    ):

        if path is not None and not isinstance(path, Path):
            path = Path(path)

        self._path = None
        self.path = path

        self._descr = None
        self.descr = descr

        if file_name is None:
            file_name = path.stem
        self._file_name = None
        self.file_name = file_name

        if ext is None:
            ext = path.suffix
        self._ext = None
        self.ext = ext

        self._uid = None
        self.uid = uid

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def descr(self):
        return self._descr

    @descr.setter
    def descr(self, descr):
        self._descr = descr

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        self._file_name = file_name

    @property
    def ext(self):
        return self._ext

    @ext.setter
    def ext(self, ext):
        self._ext = ext

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        self._uid = uid
