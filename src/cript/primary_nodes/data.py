"""
Data node

"""
from typing import Union

from .. import Cond, CRIPTError
from ..secondary_nodes.file import File
from ..utils import TablePrinting, freeze_class, convert_to_list, loading_with_units
from ..validator import type_check
from ..keys.data import data_keys
from .base import BaseModel


class DataError(CRIPTError):
    pass


@freeze_class
class Data(TablePrinting, BaseModel, _error=DataError):
    """

    :param type_: See Data.key_table()
    :param file: Raw data file. See help(File.__init__)
    :param sample_prep: Text write up of how sample was prepared.
    :param calibration: Calibration file. See help(File.__init__)
    :param equipment: Equipment file. See help(File.__init__)
    :param cond: Condition. See help(Cond.__init__) and Cond.key_table()
    :param name: The user-defined name for the process.
    :param notes: Any miscellaneous notes related to the user.
    """

    keys = data_keys
    class_ = "Data"

    def __init__(
            self,
            type_: str,
            file: File = None,
            sample_prep: str = None,
            calibration: File = None,
            equipment: File = None,
            cond: Union[list[Cond], Cond] = None,
            name: str = None,
            notes: str = None,
            **kwargs
    ):

        super().__init__(name=name, class_=self.class_, notes=notes, **kwargs)

        self._type_ = None
        self.type_ = type_

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
    def type_(self):
        return self._type_

    @type_.setter
    def type_(self, type_):
        self._type_ = type_

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, file):
        file = self.loading_with_file(file)
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
        calibration = self.loading_with_file(calibration)
        self._calibration = calibration

    @property
    def equipment(self):
        return self._equipment

    @equipment.setter
    def equipment(self, equipment):
        equipment = self.loading_with_file(equipment)
        self._equipment = equipment

    @property
    def cond(self):
        return self._cond

    @cond.setter
    @type_check(list[Cond])
    @loading_with_units
    @convert_to_list
    def cond(self, cond):
        self._cond = cond

    def loading_with_file(self, obj):
        if isinstance(obj, dict):
            obj = File(**obj)
        elif isinstance(obj, File):
            pass
        elif obj is None:
            pass
        else:
            mes = "Invalid File object."
            raise self._error(mes)

        return obj
