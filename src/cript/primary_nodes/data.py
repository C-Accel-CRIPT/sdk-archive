"""
Data node

"""
from typing import Union

from .. import Cond, CRIPTError, Unit
from ..secondary_nodes.file import File
from ..utils import TablePrinting, freeze_class, convert_to_list, loading_with_units, str_to_unit
from ..validator import type_check
from ..keys.data import data_keys
from .base import BaseModel


class DataError(CRIPTError):
    """ Data Node Error"""
    pass


@freeze_class
class Data(TablePrinting, BaseModel, _error=DataError):
    """ Data

    The Data node contains the meta-data for any raw data file. Examples of raw data include everything from NMR
    spectra to stress-strain curves to a temperature vs. time of a chemical reaction.

    Parameters
    ----------
    type_: str
        data type
        see Data.key_table()
    labels: list[str]
        axis labels
        see Data.key_table()
    units: list[Unit]
        axis units
        see Data.key_table()
    file: File
        raw data file.
        see help(File.__init__)
    sample_prep: list[str]
        sample preparation steps
    calibration: File
        calibration file
        see help(File.__init__)
    equipment: list[str]
        equipment used to take data
    cond: list[Cond]
        equipment settings or environmental variables for data collection

    """

    keys = data_keys
    class_ = "Data"

    def __init__(
            self,
            type_: str,
            labels: list[str] = None,
            units: Union[list[Unit], list[str]] = None,
            file: File = None,
            sample_prep: Union[list[str], str] = None,
            calibration: File = None,
            equipment: Union[list[str], str] = None,
            cond: Union[list[Cond], Cond] = None,
            name: str = None,
            notes: str = None,
            **kwargs
    ):
        super().__init__(name=name, class_=self.class_, notes=notes, **kwargs)

        self._type_ = None
        self.type_ = type_

        self._labels = None
        self.labels = labels

        self._units = None
        self.units = units

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
    @type_check(str)
    def type_(self, type_):
        self._type_ = type_

    @property
    def labels(self):
        return self._labels

    @labels.setter
    @type_check(list[str])
    def labels(self, labels):
        self._labels = labels

    @property
    def units(self):
        return self._units

    @units.setter
    @type_check(list[Unit])
    @str_to_unit
    def units(self, units):
        self._units = units

    @property
    def file(self):
        return self._file

    @file.setter
    @type_check(File)
    def file(self, file):
        file = self.loading_with_file(file)
        self._file = file

    @property
    def sample_prep(self):
        return self._sample_prep

    @sample_prep.setter
    @type_check(list[str])
    def sample_prep(self, sample_prep):
        self._sample_prep = sample_prep

    @property
    def calibration(self):
        return self._calibration

    @calibration.setter
    @type_check(File)
    def calibration(self, calibration):
        calibration = self.loading_with_file(calibration)
        self._calibration = calibration

    @property
    def equipment(self):
        return self._equipment

    @equipment.setter
    @type_check(list[str])
    def equipment(self, equipment):
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
