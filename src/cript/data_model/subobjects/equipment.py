from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.file import File
from cript.data_model.subobjects.base_subobject import BaseSubobject
from cript.data_model.subobjects.citation import Citation
from cript.data_model.subobjects.condition import Condition

logger = getLogger(__name__)


class Equipment(BaseSubobject):
    """The <a href="../equiupment" target="_blank">`Equipment`</a> object
    represents a piece of laboratory equipment. It can be used in a
    <a href="/../nodes/process" target="_blank">`Process`</a>.

    Args:
        key (str): Equipment key
        description (Union[str, None], optional): Equipment description
        conditions (list[Union[Condition, dict]], optional): `Condition` objects associated with this equipment
        files (list[Union[File, dict]], optional): `File` objects associated with this equipment
        citations (list[Union[Citation, dict]], optional): `Citation` objects associated with this equipment

    ``` py title="Example"
    equipment = Equipment(
        key="burner",
        description="general-purpose bunsen burner",
    )
    ```
    """

    node_name = "Equipment"
    alt_names = ["equipment"]

    @beartype
    def __init__(
        self,
        key: str,
        description: Union[str, None] = None,
        conditions: list[Union[Condition, dict]] = None,
        files: list[Union[File, dict]] = None,
        citations: list[Union[Citation, dict]] = None,
    ):
        super().__init__()
        self.key = key
        self.description = description
        self.conditions = conditions if conditions else []
        self.files = files if files else []
        self.citations = citations if citations else []
