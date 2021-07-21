"""
Material Node

"""

from .base import BaseModel, Cond, Prop
from .keywords.material import *
from .utils.serializable import Serializable
from .validation_tools import *


class Identifiers(Serializable):
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
    @type_check_property
    def preferred_name(self, preferred_name):
        self._preferred_name = preferred_name

    @property
    def names(self):
        return self._names

    @names.setter
    @type_check_property
    def names(self, names):
        self._names = names

    @property
    def cas(self):
        return self._cas

    @cas.setter
    @type_check_property
    def cas(self, cas):
        self._cas = cas

    @property
    def bigsmiles(self):
        return self._bigsmiles

    @bigsmiles.setter
    @type_check_property
    def bigsmiles(self, bigsmiles):
        self._bigsmiles = bigsmiles

    @property
    def smiles(self):
        return self._smiles

    @smiles.setter
    @type_check_property
    def smiles(self, smiles):
        self._smiles = smiles

    @property
    def chem_formula(self):
        return self._chem_formula

    @chem_formula.setter
    @type_check_property
    def chem_formula(self, chem_formula):
        self._chem_formula = chem_formula

    @property
    def chem_repeat(self):
        return self._chem_repeat

    @chem_repeat.setter
    @type_check_property
    def chem_repeat(self, chem_repeat):
        self._chem_repeat = chem_repeat

    @property
    def pubchem_cid(self):
        return self._pubchem_cid

    @pubchem_cid.setter
    @type_check_property
    def pubchem_cid(self, pubchem_cid):
        self._pubchem_cid = pubchem_cid

    @property
    def inchi(self):
        return self._inchi

    @inchi.setter
    @type_check_property
    def inchi(self, inchi):
        self._inchi = inchi

    @property
    def inchi_key(self):
        return self._inchi_key

    @inchi_key.setter
    @type_check_property
    def inchi_key(self, inchi_key):
        self._inchi_key = inchi_key


class Material(BaseModel):
    op_keywords = [k for k in keywords_material_p.keys()] + [k for k in keywords_material.keys()]
    _class = "material"

    def __init__(
            self,
            identifier: list[Identifiers],
            name: str = None,
            properties: list[Prop] = None,
            keywords: list[str] = None,
            source: str = None,
            lot_number: str = None,
            storage: list[Cond] = None,
            hazard: list[str] = None,
            notes: str = None
    ):
        """

        :param name: The name of the user.
        :param identifier:
        :param properties:
        :param keywords:
        :param source:
        :param lot_number:
        :param storage:
        :param hazard:
        :param notes: Any miscellaneous notes related to the user.

        :param _class: class of node.
        :param uid: The unique ID of the material.
        :param model_version: Version of CRIPT data model.
        :param version_control: Link to version control node.
        :param last_modified_date: Last date the node was modified.
        :param created_date: Date it was created.
        """
        if name is None:
            name = identifier[0].preferred_name

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
    @type_check_property
    def identifier(self, identifier):
        self._identifier = identifier

    @property
    def properties(self):
        return self._properties

    @properties.setter
    @type_check_property
    def properties(self, properties):
        self._properties = properties

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    @type_check_property
    def keywords(self, keywords):
        self._keywords = keywords

    @property
    def source(self):
        return self._source

    @source.setter
    @type_check_property
    def source(self, source):
        self._source = source

    @property
    def lot_number(self):
        return self._lot_number

    @lot_number.setter
    @type_check_property
    def lot_number(self, lot_number):
        self._lot_number = lot_number

    @property
    def storage(self):
        return self._storage

    @storage.setter
    @type_check_property
    def storage(self, storage):
        self._storage = storage

    @property
    def hazard(self):
        return self._hazard

    @hazard.setter
    @type_check_property
    def hazard(self, hazard):
        self._hazard = hazard
