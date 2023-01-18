from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.group import Group
from cript.data_model.paginator import Paginator

logger = getLogger(__name__)


class Project(BaseNode):
    """The <a href="../project" target="_blank">`Project`</a> object represents
    a logical grouping of <a href="../collection" target="_blank">`Collection`</a>,
    <a href="../material target="_blank">`Material`</a>, and
    <a href="../file" target="_blank">`File`</a> objects. A 
    <a href="../project" target="_blank">`Project`</a> is the highest-level
    organizational node in the CRIPT data model.

    Args:
        name (str): Project name
        collections (str, optional): URL for list of collections inside the project
        materials (str, optional): URL for list of materials inside the project
        files (str, optional): URL for list of files inside the project
        notes (Union[str, None], optional): Project notes
        public (bool, optional): Whether this project is publicly viewable
        group (Union[Group, str], optional): `Group` object that manages the project


    !!! warning "Projects names must be unique"
        Each <a href="../project target="_blank">`Project`</a> name must be unique within a
        <a href="../group" target="_blank">`Group`</a> node.     

    !!! success "Project methods inherit from the `BaseNode`"
        Since the `Project` object inherits from the <a href="../base_node" target="_blank">`BaseNode`</a> object,
        all the <a href="../base_node" target="_blank">`BaseNode`</a> object methods can be used to manipulate a `Project`. These include
        `get()`, `create()`, `delete()`, `save()`, `search()`, `update()`, and `refresh()` methods.
        See the <a href="../base_node" target="_blank">`BaseNode`</a> documentation to learn more about these methods.

    ``` py title="Example"
    # get an existing group
    my_group = Group.get(name="My Group")

    # create a new project in the existing group
    my_project = Project.create(
        name="My project",
        group=my_group,
        notes="My first project",
    )

    # get another project
    my_other_project = Project.get(
        name="My other project name",
        group=my_group,
    )
    ```

    !!! question "Why is `Group` needed when getting a project?"
        <a href="../project" target="_blank">`Project`</a> names are only unique within a group, not across all groups,
        so when getting a `Project` via name,
        the associated <a href="../group" target="_blank">`Group`</a> node must also be specified.


    ``` json title="Example of a project in JSON format"
    {
        "url": "https://criptapp.org/api/project/474dbb8b-43b6-4ed0-8de8-2ca03d206cb4/",
        "uid": "474dbb8b-43b6-4ed0-8de8-2ca03d206cb4",
        "group": "https://criptapp.org/api/group/c34d5484-4675-4050-944f-e6451ecc6bb0/",
        "name": "My First Project",
        "collections": "https://criptapp.org/api/project/474dbb8b-43b6-4ed0-8de8-2ca03d206cb4/collections/",
        "materials": "https://criptapp.org/api/project/474dbb8b-43b6-4ed0-8de8-2ca03d206cb4/materials/",
        "files": "https://criptapp.org/api/project/474dbb8b-43b6-4ed0-8de8-2ca03d206cb4/files/",
        "notes": "",
        "public": true,
        "created_at": "2022-11-04T16:16:43.198676Z",
        "updated_at": "2022-11-04T16:16:43.198694Z"
    }
    ```
    """

    node_name = "Project"
    slug = "project"

    @beartype
    def __init__(
        self,
        name: str,
        collections: str = None,
        materials: str = None,
        files: str = None,
        notes: Union[str, None] = None,
        public: bool = False,
        group: Union[Group, str] = None,
        **kwargs
    ):
        super().__init__(public=public, **kwargs)
        self.name = name
        self.collections = collections
        self.materials = materials
        self.files = files
        self.notes = notes
        self.group = group

    @property
    def collections(self):
        return self._collections

    @collections.setter
    def collections(self, value):
        if value:
            self._collections = Paginator(url=value, node_name="Collection")

    @property
    def materials(self):
        return self._materials

    @materials.setter
    def materials(self, value):
        if value:
            self._materials = Paginator(url=value, node_name="Material")

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, value):
        if value:
            self._files = Paginator(url=value, node_name="File")
