"""
Material Node

"""
from typing import Type, Union

import pint

from .base import BaseModel
from .keywords.material import *

u = pint.UnitRegistry()
uq = u.Quantity


class Identifiers:
    def __init__(
            self,
            preferred_name: str,
            names: list[str] = None,
            cas: str = None,
            bigsmiles: str = None,
            smiles: str = None,
            chem_formula: str = None,
            chem_repeat: str = None,
            pubchem_cid: str = None,
            inchi: str = None,
            inchi_key: str = None
    ):
        """

        :param preferred_name: preferred name

        :param names: additional names, abbreviations, short hands for the material
        :param cas: CAS number
        :param bigsmiles: bigSMILES Line Notation
        :param smiles: simplified molecular-input line-entry system
        :param chem_formula: chemical formula
        :param chem_repeat: chemical formula of repeating unit
        :param pubchem_cid: PubChem CID
        :param inchi: IUPAC International Chemical Identifier
        :param inchi_key: a hashed version of the full InChI

        :param mat_id:
        :param main_uid:
        """

        self.mat_id = None
        self.main_uid = None

        self._preferred_name = None
        self.preferred_name = preferred_name

        self._names = None
        self.names = names

        self._cas = None
        self.cas = cas

        self._bigsmiles = None
        self.bigsmiles = bigsmiles

        self._smiles = None
        self.smiles = smiles

        self._chem_formula = None
        self.chem_formula = chem_formula

        self._chem_repeat = None
        self.chem_repeat = chem_repeat

        self._pubchem_cid = None
        self.pubchem_cid = pubchem_cid

        self._inchi = None
        self.inchi = inchi

        self._inchi_key = None
        self.inchi_key = inchi_key

    @property
    def preferred_name(self):
        return self._preferred_name

    @preferred_name.setter
    def preferred_name(self, preferred_name):
        self._preferred_name = preferred_name

    @property
    def names(self):
        return self._names

    @names.setter
    def names(self, names):
        self._names = names

    @property
    def cas(self):
        return self._cas

    @cas.setter
    def cas(self, cas):
        self._cas = cas

    @property
    def bigsmiles(self):
        return self._bigsmiles

    @bigsmiles.setter
    def bigsmiles(self, bigsmiles):
        self._bigsmiles = bigsmiles

    @property
    def smiles(self):
        return self._smiles

    @smiles.setter
    def smiles(self, smiles):
        self._smiles = smiles

    @property
    def chem_formula(self):
        return self._chem_formula

    @chem_formula.setter
    def chem_formula(self, chem_formula):
        self._chem_formula = chem_formula

    @property
    def chem_repeat(self):
        return self._chem_repeat

    @chem_repeat.setter
    def chem_repeat(self, chem_repeat):
        self._chem_repeat = chem_repeat

    @property
    def pubchem_cid(self):
        return self._pubchem_cid

    @pubchem_cid.setter
    def pubchem_cid(self, pubchem_cid):
        self._pubchem_cid = pubchem_cid

    @property
    def inchi(self):
        return self._inchi

    @inchi.setter
    def inchi(self, inchi):
        self._inchi = inchi

    @property
    def inchi_key(self):
        return self._inchi_key

    @inchi_key.setter
    def inchi_key(self, inchi_key):
        self._inchi_key = inchi_key


class Conditions:
    def __init__(
            self,
            time=None,
            temp: float = None,
            pres: float = None,
            unit: u.Quantity = None,
            solvent=None,
            standard=None,
            relative=None
    ):
        """
        
        :param time: 
        :param temp: 
        :param pres:
        :param unit:
        :param solvent: 
        :param standard: 
        :param relative: 
        """

        self._time = None
        self.time = time

        self._temp = None
        self.temp = temp

        self._pres = None
        self.pres = pres

        self._unit = None
        self.unit = unit

        self._solvent = None
        self.solvent = solvent

        self._standard = None
        self.standard = standard

        self._relative = None
        self.relative = relative

    @property
    def time(self):
        return self.time

    @time.setter
    def time(self, time):
        self._time = time

    @property
    def temp(self):
        return self._temp

    @temp.setter
    def temp(self, temp):
        self._temp = temp

    @property
    def pres(self):
        return self._pres

    @pres.setter
    def pres(self, pres):
        self._pres = pres

    @property
    def solvent(self):
        return self._solvent

    @solvent.setter
    def solvent(self, solvent):
        self._solvent = solvent

    @property
    def standard(self):
        return self._standard

    @standard.setter
    def standard(self, standard):
        self._standard = standard

    @property
    def relative(self):
        return self._relative

    @relative.setter
    def relative(self, relative):
        self._relative = relative

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, unit):
        self._unit = unit



class Properties:
    def __init__(
            self,
            mat_id: int,
            key: str,
            value: Union[float, str],
            uncertainty: float = None,
            unit: u.Quantity = None,
            component: str = None,
            method: str = None,
            data_uid: str = None,
            conditions: list[Conditions] = None
    ):
        """

        :param mat_id:
        :param key:
        :param value:
        :param uncertainty:
        :param unit:
        :param component:
        :param method:
        :param data_uid:
        :param conditions:
        """

        self._mat_id = None
        self.mat_id = mat_id

        self._key = None
        self.key = key

        self._value = None
        self.value = value

        self._uncertainty = None
        self.uncertainty = uncertainty

        self._unit = None
        self.unit = unit

        self._component = None
        self.component = component

        self._method = None
        self.method = method

        self._data_uid = None
        self.data_uid = data_uid

        self._conditions = None
        self.conditions = conditions

    @property
    def mat_id(self):
        return self._mat_id

    @mat_id.setter
    def mat_id(self, mat_id):
        self._mat_id = mat_id

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def uncertainty(self):
        return self._uncertainty

    @uncertainty.setter
    def uncertainty(self, uncertainty):
        self._uncertainty = uncertainty

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, unit):
        self._unit = unit

    @property
    def component(self):
        return self._component

    @component.setter
    def component(self, component):
        self._component = component

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, method):
        self._method = method

    @property
    def data_uid(self):
        return self._data_uid

    @data_uid.setter
    def data_uid(self, data_uid):
        self._data_uid = data_uid

    @property
    def conditions(self):
        return self._conditions

    @conditions.setter
    def conditions(self, conditions):
        self._conditions = conditions


class Material(BaseModel):
    keywords_options = [k for k in material_keywords_polymer.keys()] + [k for k in material_keywords_monomer.keys()]
    _class = "material"

    def __init__(
            self,
            name: str,
            identifier: list[Identifiers],
            properties: list[Properties] = None,
            keywords: list[str] = None,
            source: str = None,
            lot_number: str = None,
            storage: str = None,
            hazard: list[str] = None,
            notes: str = None
    ):
        """

        :param name: The name of the user.
        :param identifier:

        :param notes: Any miscellaneous notes related to the user.

        :param _class: class of node.
        :param uid: The unique ID of the material.
        :param model_version: Version of CRIPT data model.
        :param version_control: Link to version control node.
        :param last_modified_date: Last date the node was modified.
        :param created_date: Date it was created.
        """

        super().__init__(name=name, _class=self._class, notes=notes)

        self._identifier = None
        self.identifier = identifier

        self._properties = None
        self.properties = properties

        self._keywords = None
        self.keywords = keywords

        self._source = None
        self.source = source

        self._lot_number = None
        self.lot_number = lot_number

        self._storage = None
        self.storage = storage

        self._hazard = None
        self.hazard = hazard

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        self._identifier = identifier

    @property
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, properties):
        self._properties = properties

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        self._keywords = keywords

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = source

    @property
    def lot_number(self):
        return self._lot_number

    @lot_number.setter
    def lot_number(self, lot_number):
        self._lot_number = lot_number

    @property
    def storage(self):
        return self._storage

    @storage.setter
    def storage(self, storage):
        self._storage = storage

    @property
    def hazard(self):
        return self._hazard

    @hazard.setter
    def hazard(self, hazard):
        self._hazard = hazard
