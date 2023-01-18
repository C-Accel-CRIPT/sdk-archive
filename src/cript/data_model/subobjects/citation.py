from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.reference import Reference
from cript.data_model.subobjects.base_subobject import BaseSubobject

logger = getLogger(__name__)


class Citation(BaseSubobject):
    """A <a href="../citation" target="_blank">`Citation`</a>
    object represents a <a href="/../nodes/reference" target="_blank">`Reference`</a> object
    that is applied in a given context. For example, a published article may be represented by a
    <a href="/../nodes/reference" target="_blank">`Reference`</a>, and that
    <a href="/../nodes/reference" target="_blank">`Reference`</a>
    may be linked to a
    <a href="/../nodes/data" target="_blank">`Data`</a>
    object as a <a href="../citation" target="_blank">`Citation`</a>.

    Args:
        reference (Union[Reference, str]): The `Reference` node which is being cited
        type (Union[str, None], optional): The citation type
        notes (Union[str, None], optional): Citation nodes

    ``` py title="Example"
    citation = Citation(
        reference=my_reference,
        type="reference",
        notes="Data extracted from Table 2",
    )
    ```
    """

    node_name = "Citation"
    alt_names = ["citations"]

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
