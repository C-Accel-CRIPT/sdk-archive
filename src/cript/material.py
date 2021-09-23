"""
Material Node

"""
from typing import Union

from . import CRIPTError, Cond, Prop
from .base import BaseModel, BaseSlot
from .doc_tools import loading_with_units
from .utils.serializable import Serializable
from .utils.external_database_code import GetMaterialID
from .utils.validator.type_check import type_check_property, type_check
from .utils.printing import TablePrinting
from .keys.material import *
from .utils.class_tools import freeze_class


class MaterialError(CRIPTError):
    pass


class IdenError(CRIPTError):
    pass


@freeze_class
class Iden(Serializable):
    _error = IdenError

    def __init__(
            self,
            ref_material=None,
            name: str = None,
            names: list[str] = None,
            cas: str = None,
            bigsmiles: str = None,
            smiles: str = None,
            chem_formula: str = None,
            chem_repeat: str = None,
            pubchem_cid: str = None,
            inchi: str = None,
            inchi_key: str = None,
            mat_id: int = None
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
        """
        self._mat_id = None
        self.mat_id = mat_id

        self._name = None
        self._names = None

        if ref_material is not None:
            self._ref_material = None
            self.ref_material = ref_material
            name = self.ref_material["name"]
            self.name = name
            self.names = name
            return

        self.name = name

        # adding name to names
        if names is None:
            names = [name]
        elif isinstance(names, list):
            if name not in names:
                names.append(name)

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
    def mat_id(self):
        return self._mat_id

    @mat_id.setter
    @type_check_property
    def mat_id(self, mat_id):
        self._mat_id = mat_id

    @property
    def ref_material(self):
        return self._ref_material

    @ref_material.setter
    def ref_material(self, material):
        if isinstance(material, dict) and "uid" in material.keys():
            pass
        elif isinstance(material, Material):
            material = material.reference()
        else:
            mes = f"Invalid material type. {material}"
            raise self._error(mes)

        self._ref_material = material


class IdenSlot:
    _error = None

    def __init__(self, idens=None, _error=CRIPTError):
        self._idens = []

        if idens is not None:
            self.add(idens)

    def __str__(self):
        return "".join([str(iden) for iden in self._idens])

    def __repr__(self):
        return "".join([repr(iden) for iden in self._idens])

    def __call__(self):
        return self._idens

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._idens[item]
        elif isinstance(item, slice):
            return [self._idens[i] for i in range(*item.indices(len(self._idens)))]
        else:
            mes = "Item not found."
            raise self._error(mes)

    def __len__(self):
        return len(self._idens)

    def __iter__(self):
        for iden in self._idens:
            yield iden

    def add(self, idens):
        if not isinstance(idens, list):
            idens = [idens]

        for iden in idens:
            if isinstance(iden, Iden):
                iden.mat_id = len(self._idens) + 1
                self._idens.append(iden)
            elif isinstance(iden, dict):
                if "mat_id" not in iden.keys():
                    iden["mat_id"] = len(self._idens) + 1
                self._idens.append(Iden(**iden))
            elif isinstance(iden, Material):
                iden = Iden(ref_material=iden)
                iden.mat_id = len(self._idens) + 1
                self._idens.append(iden)
            else:
                mes = f"Invalid object type for Iden. '{iden}'"
                raise self._error(mes)

    def remove(self, idens):
        if not isinstance(idens, list):
            idens = [idens]

        for iden in idens:
            if isinstance(iden, int) and iden < len(self._idens):
                del self._idens[iden]
            else:
                mes = f"Invalid object type for Iden. '{iden}'"
                raise self._error(mes)

    def as_dict(self, **kwags) -> list:
        """ Returns list of references for serialization."""
        return [iden.as_dict(**kwags) for iden in self._idens]


@freeze_class
class Material(TablePrinting, BaseModel, _error=MaterialError):
    keys = keywords_material_p | keywords_material
    class_ = "Material"

    def __init__(
            self,
            iden,
            name: str = None,
            prop: Union[list[Prop], Prop] = None,
            c_process=None,
            c_parent_material=None,
            keywords: list[str] = None,
            source: str = None,
            lot_number: str = None,
            storage: Union[list[Cond], Cond] = None,
            hazard: list[str] = None,
            notes: str = None,
            **kwargs
    ):
        """
        :param iden: See help(Iden.__init__) for details

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

        self._iden = IdenSlot(iden, _error=self._error)

        self._prop = None
        self.prop = prop

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

        self._c_process = BaseSlot("Process", c_process, self._error)
        self._c_parent_material = BaseSlot("Material", c_parent_material, self._error)

        if name is None:
            name = self._name_from_identifier()

        super().__init__(name=name, class_=self.class_, notes=notes, **kwargs)

    @property
    def iden(self):
        return self._iden

    @iden.setter
    def iden(self, *args):
        self._base_slot_block()

    @property
    def prop(self):
        return self._prop

    @prop.setter
    @type_check((list[Prop], Prop, None))
    def prop(self, prop):
        prop = loading_with_units(prop, Prop)
        self._prop = prop

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
    @type_check((list[Cond], Cond, None))
    def storage(self, storage):
        storage = loading_with_units(storage, Cond)
        self._storage = storage

    @property
    def hazard(self):
        return self._hazard

    @hazard.setter
    @type_check_property
    def hazard(self, hazard):
        self._hazard = hazard

    @property
    def c_process(self):
        return self._c_process

    @c_process.setter
    def c_process(self, *args):
        self._base_slot_block()

    @property
    def c_parent_material(self):
        return self._c_parent_material

    @c_parent_material.setter
    def c_parent_material(self, *args):
        self._base_slot_block()

    def _name_from_identifier(self):
        """
        Will generate a name from identifiers.
        :return:
        """
        if len(self.iden) == 1:
            name = self.iden[0].name
        else:
            name = ""
            for iden in self.iden:
                name += iden.name + "."
            name = name[:-1]

        return name

    def _get_mat_id(self, target: str) -> int:
        """given a string (likely chemical name) find mat_id."""
        return GetMaterialID.get_id(target, self)
