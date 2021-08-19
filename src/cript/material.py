"""
Material Node

"""
from json import dumps
from typing import Union

from . import load, CRIPTError, BaseModel, Cond, Prop
from .utils.serializable import Serializable
from cript.utils.validator.type_check import type_check_property, type_check
from .keys.material import *


class Iden(Serializable):
    def __init__(
            self,
            c_material=None,
            name: str = None,
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
        :param name: preferred name
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

        self._name = None
        self.name = name

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

        self._c_material = None
        self.c_material = c_material

    def __repr__(self):
        return dumps(self.dict_cleanup(self.as_dict()), indent=2, sort_keys=True)

    def __str__(self):
        return dumps(self.dict_cleanup(self.dict_remove_none(self.as_dict())), indent=2, sort_keys=True)

    @property
    def name(self):
        return self._name

    @name.setter
    @type_check_property
    def name(self, name):
        self._name = name

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

    @property
    def c_material(self):
        return self._c_material

    @c_material.setter
    def c_material(self, c_material):
        pass
        #BaseModel._setter_CRIPT_prop(c_material, "c_material")


class Material(BaseModel):
    op_keywords = [k for k in keywords_material_p.keys()] + [k for k in keywords_material.keys()]
    _class = "Material"

    def __init__(
            self,
            iden: "Union[list[Iden], Iden, list[Material], Material]",
            name: str = None,
            prop: Union[list[Prop], Prop] = None,
            c_process=None,
            keywords: list[str] = None,
            source: str = None,
            lot_number: str = None,
            storage: Union[list[Cond], Cond] = None,
            hazard: list[str] = None,
            notes: str = None,
            **kwargs
    ):
        """
        :param iden:

        :param name: The name of the user. (automatic populated from identifier if not given)
        :param prop: properties
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

        self._iden = None
        self.iden = iden

        self._prop = None
        self.prop = prop

        self._c_process = None
        self.c_process = c_process

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

        if name is None:
            name = self._name_from_identifier()

        super().__init__(name=name, _class=self._class, notes=notes, **kwargs)

    @property
    def iden(self):
        return self._iden

    @iden.setter
    @type_check((list[Iden], Iden, dict, "self", "list[self]"))
    def iden(self, obj):
        ddict = dict()

        if isinstance(obj, dict):
            ddict = obj
        elif isinstance(obj, Iden):
            ddict["1"] = obj.as_dict()
        elif isinstance(obj, Material):
            ddict["1"] = obj._reference
        elif isinstance(obj, list):
            for i, iden in enumerate(obj):
                if isinstance(iden, Iden):
                    ddict[f"{i+1}"] = iden.as_dict()
                elif isinstance(iden, Material):
                    ddict[f"{i+1}"] = iden._reference()
                else:
                    mes = "Invalid Identifier provided."
                    raise CRIPTError(mes)
        else:
            mes = "Invalid Identifier provided."
            raise CRIPTError(mes)

        self._iden = ddict

    @property
    def prop(self):
        return self._prop

    @prop.setter
    @type_check((list[Prop], Prop, None))
    def prop(self, prop):
        if isinstance(prop, list):
            for i, p in enumerate(prop):
                if isinstance(p, dict):
                    prop[i] = Prop(**p, _loading=True)
        elif isinstance(prop, Prop):
            prop = [prop]
        self._prop = prop

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    @type_check_property
    def keywords(self, keywords):
        self._keywords = keywords

    @property
    def c_process(self):
        return self._c_process

    @c_process.setter
    def c_process(self, c_process):
        self._setter_CRIPT_prop(c_process, "c_process")

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
    @type_check((list[Cond], Cond, None))
    def storage(self, storage):
        if isinstance(storage, list):
            for i, s in enumerate(storage):
                if isinstance(s, dict):
                    storage[i] = Cond(**s, _loading=True)
        elif isinstance(storage, Cond):
            storage = [Cond]
        self._storage = storage

    @property
    def hazard(self):
        return self._hazard

    @hazard.setter
    @type_check_property
    def hazard(self, hazard):
        self._hazard = hazard

    def _name_from_identifier(self):
        """
        Will generate a name from identifiers.
        :return:
        """
        keys = self.iden.keys()
        if len(keys) == 1:
            name = self.iden["1"]["name"]
        else:
            name = ""
            for key in keys:
                name = name + "." + self.iden[key]["name"]

        return name
