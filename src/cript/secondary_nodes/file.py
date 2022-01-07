from typing import Union
from bson import ObjectId
from pathlib import Path

from .. import CRIPTError
from ..utils import SerializableSub, freeze_class, str_to_path
from ..validator import type_check


class FileError(CRIPTError):
    pass


@freeze_class
class File(SerializableSub):
    """ File

    Links to raw data file

    Parameters
    ----------
    path: Path
        file path
    descr: str
        description (automatically extracted)
    file_name: str
        file name
    ext: str
        file extension (automatically extracted)
    uid: ObjectId
        Id to location of file
    """
    def __init__(
            self,
            path: Union[Path, str],
            descr: str = None,
            file_name: str = None,
            ext: str = None,
            uid: Union[ObjectId, str] = None
    ):

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
    @type_check(Path)
    @str_to_path
    def path(self, path):
        self._path = path

    @property
    def descr(self):
        return self._descr

    @descr.setter
    @type_check(str)
    def descr(self, descr):
        self._descr = descr

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    @type_check(str)
    def file_name(self, file_name):
        self._file_name = file_name

    @property
    def ext(self):
        return self._ext

    @ext.setter
    @type_check(str)
    def ext(self, ext):
        self._ext = ext

    @property
    def uid(self):
        return self._uid

    @uid.setter
    @type_check(ObjectId)
    def uid(self, uid):
        self._uid = uid

    def check_file(self):
        """ check that file exists. """
        if not self.path.isfile():
            raise self._errror(f"File not found. path:{self.path} ")
