"""
Identity for Materials

"""

from .. import CRIPTError
from ..utils import Serializable, TablePrinting, freeze_class
from ..validator import type_check_loop
from ..keys.iden import identifier_keys
from ..primary_nodes.base import CriptTypes


class IdenError(CRIPTError):
    pass


@freeze_class
class Iden(Serializable, TablePrinting, CriptTypes):
    """ Identifiers

        Unique label or descriptive information to represent a material

        Attributes
        ----------
        Attributes are dynamically created during initialization from 'identifier_keys'.

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
        * 'keys' is the official list of identifiers. `Iden.print_keys()`
        * Custom identifiers are allowed with a "plus_" added at the front
            The "plus_" will be replace with "+" when saving.

        """
    _error = IdenError
    keys = identifier_keys

    def __init__(self, **kwargs):

        # set up protected attributes
        for k in self.keys:
            setattr(self, "_" + k, None)
        self._ref_material = None

        # Add properties to Iden class
        for k, v in kwargs.items():
            if k in self.keys:  # official attributes
                setattr(self, k, v)
            elif k.startswith("plus_"):  # unoffical attributes
                setattr(self, k, v)
            elif k.startswith("+"):  # unoffical attributes from database
                k.replace("+", "plus_")
                setattr(self, k, v)
            elif k == "ref_material":
                self.ref_material = v
            else:
                raise IdenError(f" {k} is not an official identifier. Add 'plus_' if for custom identifiers.")

        self._name_stuff()

    def _name_stuff(self):
        """ Checking names and name. """
        if self.ref_material is not None:  # setting name if using ref_material
            setattr(self, "name", self.ref_material["name"])

        if self.name is not None:  # adding name to names (if its not already included)
            if self.names is not None and self.name not in self.names:
                self.names.append(self.name)
            else:
                self.names = [self.name]
        else:  # adding names[0] to name if empty
            if self.names is not None:
                self.name = self.names[0]
            else:
                raise self._error("Insufficient identifiers provided. 'name' or 'reference material' must be "
                                  "provided at a minimum.")

    @property
    def ref_material(self):
        return self._ref_material

    @ref_material.setter
    def ref_material(self, material):
        if isinstance(material, dict) and "uid" in material.keys():
            pass
        elif isinstance(material, self.cript_types["Material"]):
            material = material.reference()
        else:
            mes = f"Invalid material type. {material}"
            raise self._error(mes)

        self._ref_material = material

    def as_dict(self, **kwargs) -> dict:
        """
        return object as dictionary

        Overwriting the one in Serialization to replace "plus_" with "+"

        """
        keys = {k.lstrip("_") for k in vars(self) if "__" not in k}

        attr = dict()
        for k in keys:
            value = self._to_dict(self.__getattribute__(k), **kwargs)
            if k.startswith("plus_"):
                k = k.replace("plus_", "+")
            attr[k] = value

        return attr

    @classmethod
    def _init_(cls):
        cls.add_attributes()

    @classmethod
    def add_attributes(cls):
        """ Adds property attributes to class_"""
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

        for k, v in cls.keys.items():
            prop_ = get_property(k, identifier_keys[k]["type"], identifier_keys[k]["validator"])
            setattr(cls, k, prop_)


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
