from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.group import Group
from cript.data_model.nodes.project import Project
from cript.data_model.subobjects.base_subobject import BaseSubobject
from cript.data_model.subobjects.identifier import Identifier
from cript.data_model.subobjects.property import Property
from cript.data_model.utils import auto_assign_group

logger = getLogger(__name__)


class Material(BaseNode):
    """The <a href="../material" target="_blank">`Material`</a> object represents a
    single physical or virtual material, chemical, mixture or compound.

    Args:
        project (Union[Project, str]): The parent `Project` object
        name (str): Material name
        identifiers (list[Union[Identifier, dict]], optional): List of material `Identifier` objects
        components (list[Union[BaseNode, str]], optional): List of material components
        keywords (Union[list[str], None], optional): List of material kewords
        properties (list[Union[Property, dict]], optional): List of material `Property` objects
        process (Union[BaseNode, str, None], optional): `Process` object associated with the material
        computational_forcefield (Union[BaseSubobject, dict, None], optional): `ComputationalForcefield` object associated with the material
        notes (Union[str, None], optional): Material notes
        public (bool, optional): Whether the material is publicly viewable
        group (Union[Group, str], optional): `Group` object which manages the material

    !!! warning "Material names must be unique"
        Each <a href="../material" target="_blank">`Material`</a> name must be unique within a given
        <a href="../project" target="_blank">`Project`</a> node.     

    !!! success "Use <a href='../base_node' target='_blank'>`BaseNode`</a> methods to manipulate this object"
        Since this object inherits from the <a href="../base_node" target="_blank">`BaseNode`</a> object,
        all the <a href="../base_node" target="_blank">`BaseNode`</a> object methods can be used to manipulate it.
        These include `get()`, `create()`, `delete()`, `save()`, `search()`, `update()`, and `refresh()` methods.
        See the <a href="../base_node" target="_blank">`BaseNode`</a> documentation to learn more about these methods
        and see examples of their use.

    !!! note "Allowed `Material` keywords"
        The allowed `Material` keywords are listed in the
        <a href="https://criptapp.org/keys/material-keyword/" target="_blank">CRIPT controlled vocabulary</a>
        
    ``` py title="Example"
    # get an existing project
    my_project = Project.get(name="My project")

    # create a new material in the existing project
    material = Material.create(
        project=my_project
        name="PEDOT:PSS",
        keywords=["polymer_blend", "block"],
    )
    ```

    ``` json title="Example of a material in JSON format"
    {
        "url": "https://criptapp.org/api/material/c27e320e-23f6-47d5-8348-1b842e7b9767/",
        "uid": "c27e320e-23f6-47d5-8348-1b842e7b9767",
        "group": "https://criptapp.org/api/group/30bad7ab-ed35-4659-a56f-9fc384d996f4/",
        "project": "https://criptapp.org/api/project/ab890408-4da1-4311-aa7e-6a4f7897619f/",
        "name": "polystyrene",
        "identifiers": [
            {
                "key": "preferred_name",
                "value": "polystyrene"
            },
            {
                "key": "names",
                "value": [
                    "poly(styrene)",
                    "poly(vinylbenzene)"
                ]
            },
            {
                "key": "chem_repeat",
                "value": "C8H8"
            },
            {
                "key": "chemical_id",
                "value": "100-42-5"
            },
            {
                "key": "bigsmiles",
                "value": "*{[<][<]CC([>])c1ccccc1[>]}*"
            }
        ],
        "components": [],
        "keywords": [],
        "notes": "",
        "properties": [
            {
                "key": "color",
                "value": "white",
                "unit": null,
                "uncertainty": null,
                "uncertainty_type": null,
                "type": null,
                "method": null,
                "components": [],
                "components_relative": [],
                "structure": null,
                "sample_preparation": null,
                "set_id": null,
                "conditions": [],
                "data": null,
                "computations": [],
                "citations": [],
                "notes": null
            },
            {
                "key": "mw_d",
                "value": 1.03,
                "unit": null,
                "uncertainty": 0.02,
                "uncertainty_type": null,
                "type": null,
                "method": "sec",
                "components": [],
                "components_relative": [],
                "structure": null,
                "sample_preparation": null,
                "set_id": null,
                "conditions": [],
                "data": "https://criptapp.org/api/data/6f66cba6-f6c3-421f-9384-07105cb540fa/",
                "computations": [],
                "citations": [],
                "notes": null
            },
            {
                "key": "phase",
                "value": "solid",
                "unit": null,
                "uncertainty": null,
                "uncertainty_type": null,
                "type": null,
                "method": null,
                "components": [],
                "components_relative": [],
                "structure": null,
                "sample_preparation": null,
                "set_id": null,
                "conditions": [],
                "data": null,
                "computations": [],
                "citations": [],
                "notes": null
            },
            {
                "key": "mw_n",
                "value": 5.2,
                "unit": "kilogram / mole",
                "uncertainty": 0.1,
                "uncertainty_type": null,
                "type": null,
                "method": "sec",
                "components": [],
                "components_relative": [],
                "structure": null,
                "sample_preparation": null,
                "set_id": null,
                "conditions": [],
                "data": "https://criptapp.org/api/data/6f66cba6-f6c3-421f-9384-07105cb540fa/",
                "computations": [],
                "citations": [],
                "notes": null
            },
            {
                "key": "mw_n",
                "value": 4.8,
                "unit": "kilogram / mole",
                "uncertainty": 0.4,
                "uncertainty_type": null,
                "type": null,
                "method": "nmr",
                "components": [],
                "components_relative": [],
                "structure": null,
                "sample_preparation": null,
                "set_id": null,
                "conditions": [],
                "data": "https://criptapp.org/api/data/293631b7-dad3-43ec-96b7-86f233f444c7/",
                "computations": [],
                "citations": [],
                "notes": null
            }
        ],
        "process": "https://criptapp.org/api/process/9f468e7a-7eb2-4796-b438-29fccfea4b4f/",
        "computational_forcefield": null,
        "public": true,
        "created_at": "2022-09-08T17:36:08.154333Z",
        "updated_at": "2022-10-06T14:17:21.817950Z"
    }
    ```
    """

    node_name = "Material"
    slug = "material"
    alt_names = ["materials", "components", "products", "waste"]

    @beartype
    def __init__(
        self,
        project: Union[Project, str],
        name: str,
        identifiers: list[Union[Identifier, dict]] = None,
        components: list[Union[BaseNode, str]] = None,
        keywords: Union[list[str], None] = None,
        properties: list[Union[Property, dict]] = None,
        process: Union[BaseNode, str, None] = None,
        computational_forcefield: Union[BaseSubobject, dict, None] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        group: Union[Group, str] = None,
        **kwargs,
    ):
        super().__init__(public=public, **kwargs)
        self.project = project
        self.name = name
        self.identifiers = identifiers if identifiers else []
        self.components = components if components else []
        self.keywords = keywords if keywords else []
        self.properties = properties if properties else []
        self.process = process
        self.computational_forcefield = computational_forcefield
        self.notes = notes
        self.group = auto_assign_group(group, project)

    @beartype
    def add_identifier(self, identifier: Union[Identifier, dict]):
        """Add an <a href="/../subobjects/identifier" target="_blank">`Identifier`</a>.

        Args:
            identifier (Union[Identifier, dict]): `Identifier` to add
        
        ``` py title="Example"
        material.add_identifier(identifier)
        ```
        """
        self._add_node(identifier, "identifiers")

    @beartype
    def remove_identifier(self, identifier: Union[Identifier, int]):
        """Remove an <a href="/../subobjects/identifier" target="_blank">`Identifier`</a>.

        Args:
            identifier (Union[Identifier, int]): `Identifier` to remove
        
        ``` py title="Example"
        material.remove_identifier(identifier)
        ```
        """
        self._remove_node(identifier, "identifiers")

    @beartype
    def add_component(self, component: Union[BaseNode, dict]):
        """Add a component.

        Args:
            component (Union[BaseNode, dict]): Component to add
        """
        self._add_node(component, "components")

    @beartype
    def remove_component(self, component: Union[BaseNode, int]):
        """Remove a component.

        Args:
            component (Union[BaseNode, int]): Component to remove
        """
        self._remove_node(component, "components")

    @beartype
    def add_property(self, property: Union[Property, dict]):
        """Add a <a href="/../subobjects/property" target="_blank">`Property`</a>.

        Args:
            property (Union[Identifier, dict]): `Property` to add
        
        ``` py title="Example"
        material.add_property(property)
        ```
        """
        self._add_node(property, "properties")

    @beartype
    def remove_property(self, property: Union[Property, int]):
        """Remove a <a href="/../subobjects/property" target="_blank">`Property`</a>.

        Args:
            property (Union[Identifier, int]): `Property` to remove
        
        ``` py title="Example"
        material.remove_property(property)
        ```
        """
        self._remove_node(property, "properties")
