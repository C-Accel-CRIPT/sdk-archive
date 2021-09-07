"""
Data node

"""
from typing import Union
from bson import ObjectId

from . import Cond, CRIPTError, Path
from .base import BaseModel
from .utils.serializable import Serializable
from .utils.printing import KeyPrinting
from .keys.data import data_keys


class DataError(CRIPTError):
    def __init__(self, *msg):
        super().__init__(*msg)


class File(Serializable):
    def __init__(
            self,
            path: Union[str, Path],
            # labels: str = None,
            # units: str = None,
            descr: str = None,
            file_name: str = None,
            ext: str = None,
            uid: Union[str, ObjectId] = None
    ):
        """

        :param path: file path
        :param descr: description
        :param ext: file extension
        """
        if not isinstance(path, Path):
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


class Data(KeyPrinting, BaseModel, _error=DataError):
    keys = data_keys
    _class = "Data"

    def __init__(
            self,
            _type: str,
            file: File = None,
            sample_prep: str = None,
            calibration: File = None,
            equipment: File = None,
            cond: Union[list[Cond], Cond] = None,
            name: str = None,
            notes: str = None
    ):
        super().__init__(name=name, _class=self._class, notes=notes)

        self._file = None
        self.file = file
        
        self._sample_prep = None
        self.sample_prep = sample_prep

        self._calibration = None
        self.calibration = calibration
        
        self._equipment = None
        self.equipment = equipment

        self._cond = None
        self.cond = cond

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, file):
        self._file = file
        
    @property
    def sample_prep(self):
        return self._sample_prep

    @sample_prep.setter
    def sample_prep(self, sample_prep):
        self._sample_prep = sample_prep

    @property
    def calibration(self):
        return self._calibration

    @calibration.setter
    def calibration(self, calibration):
        self._calibration = calibration

    @property
    def equipment(self):
        return self._equipment

    @equipment.setter
    def equipment(self, equipment):
        self._equipment = equipment

    @property
    def cond(self):
        return self._cond

    @cond.setter
    def cond(self, cond):
        self._cond = cond
