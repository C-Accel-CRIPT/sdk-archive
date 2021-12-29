"""
Material Node

"""
from typing import Union

from . import CRIPTError, Cond, Prop
from .base import BaseModel, ReferenceList
from .utils import GetMaterialID, Serializable, TablePrinting, freeze_class, loading_with_units
from .validator import type_check
from .keys.material import *


class MaterialError(CRIPTError):
    pass


class IdenError(CRIPTError):
    pass


@freeze_class
class Iden(Serializable):
    """

    Parameters
    ----------
    name: str
        preferred name
    names: list[str]
        additional names, abbreviations, short hands for the material
    cas: str
        CAS number
    bigsmiles: str
        bigSMILES Line Notation
    smiles: str
        simplified molecular-input line-entry system (SMILES)
    chem_formula: str
        chemical formula
    chem_repeat: str
        chemical formula of repeating unit
    pubchem_cid: str
        PubChem CID
    inchi: str
        IUPAC International Chemical Identifier
    inchi_key: str
        a hashed version of the full InChI
    mat_id: int
        Local id for associating properties with a material
        Assigned automatically when added to Material Node.
        0 = whole mixture
        1+ = individual component
    ref_material:


    """

    _error = IdenError

    def __init__(
            self,
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
            mat_id: int = None,
            ref_material=None
    ):

        self._mat_id = None
        self.mat_id = mat_id

        self._name = None
        self._names = None

        if ref_material is not None:
            self._ref_material = None
            self.ref_material = ref_material
            name = self.ref_material["name"]
            self.name = name
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
    @type_check(str)
    def name(self, name):
        self._name = name

    @property
    def names(self):
        return self._names

    @names.setter
    @type_check([str, list[str]])
    def names(self, names):
        self._names = names

    @property
    def cas(self):
        return self._cas

    @cas.setter
    @type_check(str)
    def cas(self, cas):
        self._cas = cas

    @property
    def bigsmiles(self):
        return self._bigsmiles

    @bigsmiles.setter
    @type_check(str)
    def bigsmiles(self, bigsmiles):
        self._bigsmiles = bigsmiles

    @property
    def smiles(self):
        return self._smiles

    @smiles.setter
    @type_check(str)
    def smiles(self, smiles):
        self._smiles = smiles

    @property
    def chem_formula(self):
        return self._chem_formula

    @chem_formula.setter
    @type_check(str)
    def chem_formula(self, chem_formula):
        self._chem_formula = chem_formula

    @property
    def chem_repeat(self):
        return self._chem_repeat

    @chem_repeat.setter
    @type_check(str)
    def chem_repeat(self, chem_repeat):
        self._chem_repeat = chem_repeat

    @property
    def pubchem_cid(self):
        return self._pubchem_cid

    @pubchem_cid.setter
    @type_check(str)
    def pubchem_cid(self, pubchem_cid):
        self._pubchem_cid = pubchem_cid

    @property
    def inchi(self):
        return self._inchi

    @inchi.setter
    @type_check(str)
    def inchi(self, inchi):
        self._inchi = inchi

    @property
    def inchi_key(self):
        return self._inchi_key

    @inchi_key.setter
    @type_check(str)
    def inchi_key(self, inchi_key):
        self._inchi_key = inchi_key

    @property
    def mat_id(self):
        return self._mat_id

    @mat_id.setter
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


class IdenList:
    """ Identifiers List

    The Identifier List creates, and manages identifiers in the Material Node.

    Attributes
    ----------
    _idens: list[dict]
        List of Iden objects

    Methods
    -------
    add(item)
        Adds item to reference list
    remove(item)
        Removes item from reference list

    """
    _error = None

    def __init__(self, idens=None, _error=CRIPTError):
        """
        Parameters
        ----------
        idens:
            objects will be passed to self.add()
        _error:
            error class of parent node
        """
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
        """ Add

        Adds object to reference list.

        Parameters
        ----------
        idens:
            idens that you want to add to the list
            Accepted objects:
                Iden class
                Material node (will be converted to Iden automatically)

        Raises
        -------
        Exception
            If invalid object is provided. An object that does not lead to a valid reference.

        """
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
        """ Remove

        Removes object from reference list.

        Parameters
        ----------
        idens:
            object that you want to remove to the list
            Accepted objects:
                position in _reference list (int)

        Raises
        -------
        Exception
            If invalid object is provided. An object that does not lead to a valid removal.
            If the object is not in the list.

        """
        if not isinstance(idens, list):
            idens = [idens]

        for iden in idens:
            if isinstance(iden, int) and iden < len(self._idens):
                del self._idens[iden]
            else:
                mes = f"Invalid object provide, only index accepted."
                raise self._error(mes)

    def as_dict(self, **kwags) -> list:
        """ Returns list of references for serialization."""
        return [iden.as_dict(**kwags) for iden in self._idens]


@freeze_class
class Material(TablePrinting, BaseModel, _error=MaterialError):
    """

    Parameters
    ----------
    base_attributes:
        See CRIPT BaseModel
    iden: Iden
        See help(Iden) for details
    name: str
        The name of the user. (automatically populated from identifier if not given)
    prop: list[Prop], Prop
        properties
    keywords:

    source:

    lot_number:

    storage:

    hazard:

    """

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

        self._iden = IdenList(iden, _error=self._error)

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

        self._c_process = ReferenceList("Process", c_process, self._error)
        self._c_parent_material = ReferenceList("Material", c_parent_material, self._error)

        if name is None:
            name = self._name_from_identifier()

        super().__init__(name=name, class_=self.class_, notes=notes, **kwargs)

    @property
    def iden(self):
        return self._iden

    @iden.setter
    def iden(self, *args):
        self._base_reference_block()

    @property
    def prop(self):
        return self._prop

    @prop.setter
    @type_check([list[Prop], Prop])
    def prop(self, prop):
        prop = loading_with_units(prop, Prop)
        self._prop = prop

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    @type_check(str)
    def keywords(self, keywords):
        self._keywords = keywords

    @property
    def source(self):
        return self._source

    @source.setter
    @type_check(str)
    def source(self, source):
        self._source = source

    @property
    def lot_number(self):
        return self._lot_number

    @lot_number.setter
    @type_check(str)
    def lot_number(self, lot_number):
        self._lot_number = lot_number

    @property
    def storage(self):
        return self._storage

    @storage.setter
    @type_check([list[Cond], Cond])
    def storage(self, storage):
        storage = loading_with_units(storage, Cond)
        self._storage = storage

    @property
    def hazard(self):
        return self._hazard

    @hazard.setter
    @type_check(str)
    def hazard(self, hazard):
        self._hazard = hazard

    @property
    def c_process(self):
        return self._c_process

    @c_process.setter
    def c_process(self, *args):
        self._base_reference_block()

    @property
    def c_parent_material(self):
        return self._c_parent_material

    @c_parent_material.setter
    def c_parent_material(self, *args):
        self._base_reference_block()

    def _name_from_identifier(self):
        """ Will generate a name from identifiers."""
        if len(self.iden) == 1:  # single component
            name = self.iden[0].name
        else:  # mixture, concatenate names
            name = ""
            for iden in self.iden:
                name += iden.name + "."
            name = name[:-1]

        return name

    def _get_mat_id(self, target: str) -> int:
        """ Given a target (chemical name, cas number or some other identity) find material id. """
        return GetMaterialID.get_id(target, self)
