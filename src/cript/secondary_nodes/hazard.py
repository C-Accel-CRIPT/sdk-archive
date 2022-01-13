"""

Hazard Node

"""

from ..utils import Serializable, convert_to_list
from ..validator import type_check


class Hazard(Serializable):
    """ Hazards

    hazards of a material

    Attributes
    ----------
    diamond: list[str]
        NFPA classification diamond
        [Health Hazards, Fire Hazards, Instability Hazards, Specific Hazards]
    signal_word: str
        word used to notify the severity of the hazard
        “Danger” is used for the more severe hazards
        “Warning” is used for the less severe hazards
    hazard_statements: list[str]
        GHS label elements
    precautionary_statements: list[str]
        GHS label elements
    pictograms: list[str]
        hazard communication standard pictogram
        Health Hazard, Flame, Exclamation Mark, Gas Cylinder, Corrosion, Exploding Bomb, Flame Over Circle,
        Environment, Skull and Crossbones
    sds: str
        safety data sheet link
    storage_class: list[str]
        storage classification
    protective_equipment: list[str]
        protective equipment


    Notes
    -----
    * GHS = Globally Harmonized System

    """

    def __init__(self,
                 diamond: list[str] = None,
                 signal_word: str = None,
                 hazard_statements: list[str] = None,
                 precautionary_statements: list[str] = None,
                 pictograms: list[str] = None,
                 sds: str = None,
                 storage_class: list[str] = None,
                 protective_equipment: list[str] = None
                 ):
        self._diamond = None
        self.diamond = diamond

        self._signal_word = None
        self.signal_word = signal_word

        self._hazard_statements = None
        self.hazard_statements = hazard_statements

        self._precautionary_statements = None
        self.precautionary_statements = precautionary_statements

        self._pictograms = None
        self.pictograms = pictograms

        self._sds = None
        self.sds = sds

        self._storage_class = None
        self.storage_class = storage_class

        self._protective_equipment = None
        self.protective_equipment = protective_equipment

    @property
    def diamond(self):
        return self._diamond

    @diamond.setter
    @type_check(list[str])
    @convert_to_list
    def diamond(self, diamond):
        self._diamond = diamond

    @property
    def signal_word(self):
        return self._signal_word

    @signal_word.setter
    @type_check(str)
    def signal_word(self, signal_word):
        self._signal_word = signal_word

    @property
    def hazard_statements(self):
        return self._hazard_statements

    @hazard_statements.setter
    @type_check(list[str])
    @convert_to_list
    def hazard_statements(self, hazard_statements):
        self._hazard_statements = hazard_statements

    @property
    def precautionary_statements(self):
        return self._precautionary_statements

    @precautionary_statements.setter
    @type_check(list[str])
    @convert_to_list
    def precautionary_statements(self, precautionary_statements):
        self._precautionary_statements = precautionary_statements

    @property
    def pictograms(self):
        return self._pictograms

    @pictograms.setter
    @type_check(list[str])
    @convert_to_list
    def pictograms(self, pictograms):
        self._pictograms = pictograms

    @property
    def sds(self):
        return self._sds

    @sds.setter
    @type_check(str)
    def sds(self, sds):
        self._sds = sds

    @property
    def storage_class(self):
        return self._storage_class

    @storage_class.setter
    @type_check(list[str])
    @convert_to_list
    def storage_class(self, storage_class):
        self._storage_class = storage_class

    @property
    def protective_equipment(self):
        return self._protective_equipment

    @protective_equipment.setter
    @type_check(list[str])
    @convert_to_list
    def protective_equipment(self, protective_equipment):
        self._protective_equipment = protective_equipment
