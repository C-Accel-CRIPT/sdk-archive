from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes import Base, Reference
from cript.validators import validate_required, validate_key


logger = getLogger(__name__)


class Citation(Base):
    """
    Object representing how a :class:`Reference` object
    is applied in a given context.
    """

    node_type = "secondary"
    node_name = "Citation"
    list_name = "citations"
    required = ["reference"]

    @beartype
    def __init__(
        self,
        reference: Union[Reference, str] = None,
        type: Union[str, None] = "reference",
        notes: Union[str, None] = None,
    ):
        super().__init__()
        self.reference = reference
        self.type = type
        self.notes = notes
        validate_required(self)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = validate_key("citation-type", value)
