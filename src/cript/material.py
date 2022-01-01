"""
Material Node

"""
from typing import Union

from . import CRIPTError, Cond, Prop
from .base import BaseModel, ReferenceList, CriptTypes
from .load_export import loading_with_units
from .utils import GetMaterialID, Serializable, TablePrinting, freeze_class
from .validator import type_check, type_check_loop
from .keys.material import material_keywords, identifier_keys


class MaterialError(CRIPTError):
    pass


class IdenError(CRIPTError):
    pass


def get_property(prop, type_, validator):
    key = f"_{prop}"

    def get_(self):
        return getattr(self, key)

    def set_(self, value):
        type_check_loop((self, value), type_, prop)
        if validator is not None:
            value = validator(value)
        setattr(self, key, value)

    def del_(self):
        delattr(self, key)

    return property(get_, set_, del_)


def Iden(**kwargs):
    @freeze_class
    class _Iden(__Iden):
        """ Identifiers



            Attributes
            ----------
            Attributes are dynamically created.

            mat_id: int
                Local id for associating properties with a material
                Assigned automatically when added to Material Node.
                0 = whole mixture
                1+ = individual component
            ref_material:
                An already defined material.

            Notes
            -----
            * Attributes are generated at run time.
            * 'keys' has the official list of identifiers
            * Custom identifiers are allowed with a "+" add at the front

            """
        def __init__(self, **_kwargs):
            super_kwargs = {}
            if "mat_id" in _kwargs:
                super_kwargs["mat_id"] = _kwargs.pop("matid")
            if "ref_material" in _kwargs:
                super_kwargs["ref_material"] = _kwargs.pop("ref_material")

            # set
            for k_, v_ in _kwargs.items():
                setattr(self, "_" + k_, None)
                setattr(self, k_, v_)

            super().__init__(**super_kwargs)

    # Add properties to Iden class
    for k, v in kwargs.items():
        if k in identifier_keys:  # official attributes
            prop_ = get_property(k, identifier_keys[k]["type"], identifier_keys[k]["validator"])
            setattr(_Iden, k, prop_)

        elif k.startswith("+"):  # custom attributes
            setattr(_Iden, k, v)

        elif k in ["mat_id", "ref_material"]:  # skip built-in attrinutes
            pass

        else:
            raise IdenError(f" {k} is not an official identifier. Add '+' if for custom identifiers.")

    return _Iden(**kwargs)


class __Iden(Serializable):
    _error = IdenError
    keys = identifier_keys

    def __init__(
            self,
            mat_id: int = None,
            ref_material=None,
    ):

        self._mat_id = None
        self.mat_id = mat_id

        if ref_material is not None:
            self._ref_material = None
            self.ref_material = ref_material
            self._name = None
            self.name = self.ref_material["name"]
            return

        self._name_stuff()

        if not hasattr(self, "name"):
            raise self._error("Insufficient identifiers provided. 'name' or 'reference material' must be provided at a "
                              "minimum.")

    def _name_stuff(self):
        # adding name to names (if its not already included)
        if hasattr(self, "name"):
            if hasattr(self, "names") and self.name not in self.names:
                self.names.append(self.name)
            if not hasattr(self, "names"):
                setattr(self, "names", [self.name])
            return

        # defining name from names
        if hasattr(self, "names") and not hasattr(self, "name"):
            setattr(self, "name", self.names[0])

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


class IdenList(CriptTypes):
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
            if isinstance(iden, self.cript_types["__Iden"]):
                iden.mat_id = len(self._idens) + 1
                self._idens.append(iden)
            elif isinstance(iden, dict):
                if "mat_id" not in iden.keys():
                    iden["mat_id"] = len(self._idens) + 1
                self._idens.append(Iden(**iden))
            elif isinstance(iden, self.cript_types["Material"]):
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

    keys = material_keywords
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
