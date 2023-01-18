from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.group import Group

logger = getLogger(__name__)


class Software(BaseNode):
    """The <a href="../software" target="_blank">`Software`</a> object
    represents a computational tool, a set of computer code,
    a programming language, or a software package.

    Args:
        group (Union[Group, str]): `Group` object that manages the software object
        name (str): Software name
        version (str): Software version
        source (Union[str, None], optional): Software source
        notes (Union[str, None], optional): Software notes
        public (bool, optional): Whether the `Software` object is publicly viewable

    !!! success "Software methods inherit from the `BaseNode`"
        Since the `Software` object inherits from the <a href="../base_node" target="_blank">`BaseNode`</a> object,
        all the <a href="../base_node" target="_blank">`BaseNode`</a> object methods can be used to manipulate a `Software` object.
        These include `get()`, `create()`, `delete()`, `save()`, `search()`, `update()`, and `refresh()` methods.
        See the <a href="../base_node" target="_blank">`BaseNode`</a> documentation to learn more about these methods.
    
    ``` py title="Example"
    # get an existing group
    my_group = Group.get(name="My group")

    # create the software
    my_software = Software.create(
        group=my_group,
        name="Python",
        version="3.9",
        source="Anaconda distribution",
        notes="Used for processing NMR data",
    )
    ```

    ``` json title="Example of a software object in JSON format"
    {
        "url": "https://criptapp.org/api/software/00b0a435-b9b6-46e1-8aea-859209f42feb/",
        "uid": "00b0a435-b9b6-46e1-8aea-859209f42feb",
        "group": "https://criptapp.org/api/group/48e838bc-2b8d-45e4-b0b2-135473495381/",
        "name": "rdkit",
        "version": "2021.9",
        "source": "https://anaconda.org/rdkit/rdkit",
        "notes": null,
        "public": true,
        "created_at": "2022-10-19T20:49:52.794672Z",
        "updated_at": "2022-10-19T20:49:52.794695Z"
    }
    ```
    """

    node_name = "Software"
    slug = "software"
    alt_names = ["software"]

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        name: str,
        version: str,
        source: Union[str, None] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        **kwargs
    ):
        super().__init__(public=public, **kwargs)
        self.name = name
        self.version = version
        self.source = source
        self.notes = notes
        self.group = group
