from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.reference import Reference
from cript.nodes.secondary.base_secondary import BaseSecondary
from cript.validators import validate_key


logger = getLogger(__name__)


class Citation(BaseSecondary):
    """
    Object representing how a `Reference` object
    is applied in a given context.
    """

    node_name = "Citation"
    list_name = "citations"

    @beartype
    def __init__(
        self,
        reference: Union[Reference, str],
        type: Union[str, None] = "reference",
        notes: Union[str, None] = None,
    ):
        super().__init__()
        self.reference = reference
        self.type = type
        self.notes = notes

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = validate_key("citation-type", value)
