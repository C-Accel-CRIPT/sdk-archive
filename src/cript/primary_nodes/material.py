"""
Material Node

"""
from typing import Union

from .. import CRIPTError
from ..secondary_nodes.spec import Spec
from ..secondary_nodes.iden import Iden, IdenList
from ..secondary_nodes.prop import Prop
from ..secondary_nodes.load import load
from ..utils import TablePrinting, freeze_class, convert_to_list, loading_with_units
from ..mongodb import GetMaterialID
from ..validator import type_check, keys_check
from ..keys.material import material_keywords
from .base import BaseModel, ReferenceList


class MaterialError(CRIPTError):
    """ Material Error """
    pass


@freeze_class
class Material(TablePrinting, BaseModel, _error=MaterialError):
    """

    Attributes
    ----------
    base_attributes:
        see CRIPT BaseModel
    iden: list[Iden]
        material identity
        see `help(Iden)`
    name: str
        name of the material
        (automatically populated from identifier if not given)
    prop: list[Prop]
        material properties
        see `help(Prop)`
    spec: Spec
        material specification
        see `help(Spec)`
    keywords: list[str]  (has keys)
        words that classify the material
        see `Material.key_table()`
    c_process: Process
        process that produced the material
    c_material_parent: list[Material]
        material that are parents of this material

    """

    keys = material_keywords
    class_ = "Material"

    def __init__(
            self,
            iden: Union[list[Iden], Iden] = None,
            name: str = None,
            prop: Union[list[Prop], Prop] = None,
            spec: Spec = None,
            keywords: Union[list[str], str] = None,
            c_process=None,
            c_material_copy=None,
            c_material_parent=None,
            notes: str = None,
            **kwargs
    ):
        if iden is None and c_material_copy is None:
            raise self._error("'iden' or 'c_matreial_copy' is required parameters.")

        self._iden = IdenList(iden, _error=self._error)

        self._prop = None
        self.prop = prop

        self._keywords = None
        self.keywords = keywords

        self._spec = None
        self.spec = spec

        self._c_process = ReferenceList("Process", c_process, self._error)

        self._c_parent_material = ReferenceList("Material", c_material_parent, self._error)

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
    @type_check(list[Prop])
    @convert_to_list
    @loading_with_units(Prop)
    def prop(self, prop):
        self._prop = prop

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    @keys_check
    @type_check(list[str])
    @convert_to_list
    def keywords(self, keywords):
        self._keywords = keywords

    @property
    def spec(self):
        return self._spec

    @spec.setter
    @type_check(Spec)
    def spec(self, spec):
        self._spec = spec

    @property
    def c_process(self):
        return self._c_process

    @c_process.setter
    def c_process(self, *args):
        self._base_reference_block()

    @property
    def c_material_parent(self):
        return self._c_parent_material

    @c_material_parent.setter
    def c_material_parent(self, *args):
        self._base_reference_block()

    def _do_copy(self, mat):
        if isinstance(mat, dict) and "class_" in mat:
            mat = load(mat)
        if isinstance(mat, self.cript_types["Material"]):
            raise self._error(f"You can only copy from a Material Node. Given type:{type(mat)}")

        return mat.iden, mat.prop, mat.spec, mat.keywords, mat.name, mat.notes

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
