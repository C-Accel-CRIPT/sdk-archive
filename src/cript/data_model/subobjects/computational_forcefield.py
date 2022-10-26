from typing import Union
from logging import getLogger

from beartype import beartype

from cript.data_model.nodes.data import Data
from cript.data_model.subobjects.base_subobject import BaseSubobject
from cript.data_model.subobjects.citation import Citation


logger = getLogger(__name__)


class ComputationalForcefield(BaseSubobject):
    """
    Object representing the computational forcefield of a
    virtual `Material`.
    """

    node_name = "ComputationalForcefield"

    @beartype
    def __init__(
        self,
        key: str,
        building_block: str,
        coarse_grained_mapping: Union[str, None] = None,
        implicit_solvent: Union[str, None] = None,
        source: Union[str, None] = None,
        description: Union[str, None] = None,
        data: Union[Data, str, None] = None,
        citations: list[Union[Citation, dict]] = None,
    ):
        super().__init__()
        self.key = key
        self.description = description
        self.building_block = building_block
        self.coarse_grained_mapping = coarse_grained_mapping
        self.implicit_solvent = implicit_solvent
        self.source = source
        self.data = data
        self.citations = citations if citations else []
