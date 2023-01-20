from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.experiment import Experiment
from cript.data_model.nodes.group import Group
from cript.data_model.nodes.material import Material
from cript.data_model.subobjects.citation import Citation
from cript.data_model.subobjects.condition import Condition
from cript.data_model.subobjects.equipment import Equipment
from cript.data_model.subobjects.ingredient import Ingredient
from cript.data_model.subobjects.property import Property
from cript.data_model.utils import auto_assign_group

logger = getLogger(__name__)


class Process(BaseNode):
    """The <a href="../process" target="_blank">`Process`</a> object represents
    any process which creates or transforms a
    <a href="../material" target="_blank">`Material`</a> object. For example,
    the act of synthesizing, polymerizing, or annealing a material
    may be represented by a <a href="../process" target="_blank">`Process`</a> object.
    Each <a href="../process" target="_blank">`Process`</a> object is nested inside
    an <a href="../experiment" target="_blank">`Experiment`</a> object.

    Args:
        experiment (Union[Experiment, str]): The parent `Experiment` object
        name (str): Process name
        type (str): Process type
        keywords (Union[list[str], None], optional): List of process keywords
        description (Union[str, None], optional): Process description
        prerequisite_processes (list[Union[BaseNode, str]], optional): List of `Process` objects which must preceed the process
        ingredients (list[Union[Ingredient, dict]], optional): List `Ingredient` objects which are used in the process
        equipment (list[Union[Equipment, dict]], optional): List of `Equipment` objects which are used in the process
        properties (list[Union[Property, dict]], optional): List of `Property` objects associated with the process
        conditions (list[Union[Condition, dict]], optional): List of `Condition` objects associated with the process
        set_id (Union[int, None], optional): Set ID
        products (list[Union[Material, str]], optional): List of `Material` objects thaat the process produces
        waste (list[Union[Material, str]], optional): List of `Material` objects that the process produces as waste
        citations (list[Union[Citation, dict]], optional): List of `Citation` objects associated with the process
        public (bool, optional): Whether the process is publicly viewable
        group (Union[Group, str], optional): `Group` object which manages the process

    !!! warning "Process names must be unique"
        Each <a href="../process" target="_blank">`Process`</a> name must be unique within a given
        <a href="../experiment" target="_blank">`Experiment`</a> node.

    !!! success "Use <a href='../base_node' target='_blank'>`BaseNode`</a> methods to manipulate this object"
        Since this object inherits from the <a href="../base_node" target="_blank">`BaseNode`</a> object,
        all the <a href="../base_node" target="_blank">`BaseNode`</a> object methods can be used to manipulate it.
        These include `get()`, `create()`, `delete()`, `save()`, `search()`, `update()`, and `refresh()` methods.
        See the <a href="../base_node" target="_blank">`BaseNode`</a> documentation to learn more about these methods
        and see examples of their use.

    !!! note "Allowed `Process` keywords"
        The allowed `Process` keywords are listed in the
        <a href="https://criptapp.org/keys/process-keyword/" target="_blank">CRIPT controlled vocabulary</a>

    !!! note "Allowed `Process` types"
        The allowed `Process` types are listed in the
        <a href="https://criptapp.org/keys/process-type/" target="_blank">CRIPT controlled vocabulary</a>

    ``` py title="Example"
    # get an existing experiment
    my_experiment = Project.get(name="My experiment")

    # create a new material in the existing project
    process = Process.create(
        experiment=my_experiment,
        name="Initial polymerization",
        type="transform",
        keywords=["polymerization", "chain_growth"],
        description="the polymerization process took roughly 3 hours",
    )
    ```

    ``` json title="Example of a process in JSON format"
    {
        "url": "https://criptapp.org/api/process/ce7376a3-1349-43fa-9b19-f078241d7d86/",
        "uid": "ce7376a3-1349-43fa-9b19-f078241d7d86",
        "group": "https://criptapp.org/api/group/4f89a071-b84c-437b-a787-d03b6b7c844e/",
        "experiment": "https://criptapp.org/api/experiment/3280725b-d8eb-476b-92d0-bea9df847444/",
        "name": "DW13_1_P",
        "type": "multistep",
        "keywords": [],
        "description": "To a vial with a Teflon stir bar, diol (1 to 1.2 equiv) and dicarboxylic acid (1 equiv) were added. The vial is then fitted with a septum cap and purged with nitrogen. The vial is heated to 160 oC for 2 hours under 1 atm of nitrogen, before being placed under vacuum (~10 torr) for an additional 2 hours. Following that, the vial was refilled with nitrogen (1 atm) and titanium (IV) isopropoxide (0.001 equiv) was added. The reaction was allowed to stir for 30 min before being placed back under vacuum for 12 hours and increasing the temperature to 180 oC.",
        "prerequisite_processes": [],
        "ingredients": [
            {
                "material": "https://criptapp.org/api/material/bb306bc3-bb39-4821-9e10-54f5e4e1dbbd/",
                "keyword": "monomer",
                "quantities": [
                    {
                        "key": "mass",
                        "value": 0.001237531,
                        "unit": "kg",
                        "uncertainty": null,
                        "uncertainty_type": null
                    }
                ]
            },
            {
                "material": "https://criptapp.org/api/material/125c26ce-3406-410d-9cf8-33e1fd74e73e/",
                "keyword": "monomer",
                "quantities": [
                    {
                        "key": "mass",
                        "value": 0.001231434,
                        "unit": "kg",
                        "uncertainty": null,
                        "uncertainty_type": null
                    }
                ]
            },
            {
                "material": "https://criptapp.org/api/material/ba14b108-29f9-4702-88dd-848729a491de/",
                "keyword": "catalyst",
                "quantities": [
                    {
                        "key": "mass",
                        "value": 2.4e-06,
                        "unit": "kg",
                        "uncertainty": null,
                        "uncertainty_type": null
                    }
                ]
            }
        ],
        "equipment": [],
        "set_id": null,
        "properties": [],
        "conditions": [],
        "products": [
            "https://criptapp.org/api/material/19978b2e-86f4-40c0-bf11-8ee06064b4fa/"
        ],
        "waste": [],
        "citations": [],
        "public": true,
        "created_at": "2022-04-26T19:25:29.986239Z",
        "updated_at": "2022-07-06T21:12:52.155016Z"
    }
    ```
    """

    node_name = "Process"
    slug = "process"
    alt_names = ["processes", "prerequisite_processes", "sample_preparation"]

    @beartype
    def __init__(
        self,
        experiment: Union[Experiment, str],
        name: str,
        type: str,
        keywords: Union[list[str], None] = None,
        description: Union[str, None] = None,
        prerequisite_processes: list[Union[BaseNode, str]] = None,
        ingredients: list[Union[Ingredient, dict]] = None,
        equipment: list[Union[Equipment, dict]] = None,
        properties: list[Union[Property, dict]] = None,
        conditions: list[Union[Condition, dict]] = None,
        set_id: Union[int, None] = None,
        products: list[Union[Material, str]] = None,
        waste: list[Union[Material, str]] = None,
        citations: list[Union[Citation, dict]] = None,
        public: bool = False,
        group: Union[Group, str] = None,
        **kwargs,
    ):
        super().__init__(public=public, **kwargs)
        self.experiment = experiment
        self.name = name
        self.type = type
        self.keywords = keywords if keywords else []
        self.description = description
        self.prerequisite_processes = (
            prerequisite_processes if prerequisite_processes else []
        )
        self.ingredients = ingredients if ingredients else []
        self.equipment = equipment if equipment else []
        self.properties = properties if properties else []
        self.conditions = conditions if conditions else []
        self.set_id = set_id
        self.products = products if products else []
        self.waste = waste if waste else []
        self.citations = citations if citations else []
        self.group = auto_assign_group(group, experiment)

    @beartype
    def add_equipment(self, piece: Union[Equipment, dict]):
        """Add an <a href="/../subobjects/equipment" target="_blank">`Equipment`</a> object.

        Args:
            piece (Union[Equipment, dict]): `Equipment` object to add

        ``` py title="Example"
        process.add_equipment(equipment)
        ```
        """
        self._add_node(piece, "equipment")

    @beartype
    def remove_equipment(self, piece: Union[Equipment, int]):
        """Remove an <a href="/../subobjects/equipment" target="_blank">`Equipment`</a> object.

        Args:
            piece (Union[Equipment, int]): `Equipment` object to remove

        ``` py title="Example"
        process.remove_equipment(equipment)
        ```
        """
        self._remove_node(piece, "equipment")

    @beartype
    def add_prerequisite_process(self, process: Union[BaseNode, dict]):
        """Add a prerequisite <a href="../process" target="_blank">`Process`</a> object.

        Args:
            process (Union[Process, dict]): `Process` object to add

        ``` py title="Example"
        process.add_prerequisite_process(process)
        ```
        """
        self._add_node(process, "prerequisite_processes")

    @beartype
    def remove_prerequisite_process(self, process: Union[BaseNode, int]):
        """Remove a prerequisite <a href="../process" target="_blank">`Process`</a> object.

        Args:
            process (Union[Process, int]): `Process` object to remove

        ``` py title="Example"
        process.remove_prerequisite_process(process)
        ```
        """
        self._remove_node(process, "prerequisite_processes")

    @beartype
    def add_ingredient(self, ingredient: Union[Ingredient, dict]):
        """Add an <a href="/../subobjects/ingredient" target="_blank">`Ingredient`</a> object.

        Args:
            ingredient (Union[Ingredient, dict]): `Ingredient` object to add

        ``` py title="Example"
        process.add_ingredient(ingredient)
        ```
        """
        self._add_node(ingredient, "ingredients")

    @beartype
    def remove_ingredient(self, ingredient: Union[Ingredient, int]):
        """Remove an <a href="/../subobjects/ingredient" target="_blank">`Ingredient`</a> object.

        Args:
            ingredient (Union[Ingredient, int]): `Ingredient` object to remove

        ``` py title="Example"
        process.remove_ingredient(ingredient)
        ```
        """
        self._remove_node(ingredient, "ingredients")

    @beartype
    def add_product(self, material: Union[Material, dict]):
        """Add a <a href="../material" target="_blank">`Material`</a> object as a product.

        Args:
            material (Union[Material, dict]): `Material` object to add as a product

        ``` py title="Example"
        process.add_product(product)
        ```
        """
        self._add_node(material, "products")

    @beartype
    def remove_product(self, material: Union[Material, int]):
        """Remove a <a href="../material" target="_blank">`Material`</a> object as a product.

        Args:
            material (Union[Material, int]): `Material` object to remove as a product

        ``` py title="Example"
        process.remove_product(product)
        ```
        """
        self._remove_node(material, "products")

    @beartype
    def add_waste(self, material: Union[Material, dict]):
        """Add a <a href="../material" target="_blank">`Material`</a> object as waste.

        Args:
            material (Union[Material, dict]): `Material` object to add as waste

        ``` py title="Example"
        process.add_waste(waste)
        ```
        """
        self._add_node(material, "waste")

    @beartype
    def remove_waste(self, material: Union[Material, int]):
        """Remove a <a href="../material" target="_blank">`Material`</a> object as waste.

        Args:
            material (Union[Material, int]): `Material` object to remove as waste

        ``` py title="Example"
        process.remove_waste(waste)
        ```
        """
        self._remove_node(material, "waste")

    @beartype
    def add_condition(self, condition: Union[Condition, dict]):
        """Add a <a href="/../subobjects/condition" target="_blank">`Condition`</a> object.

        Args:
            condition (Union[Condition, dict]): `Condition` object to add

        ``` py title="Example"
        process.add_condition(condition)
        ```
        """
        self._add_node(condition, "conditions")

    @beartype
    def remove_condition(self, condition: Union[Condition, int]):
        """Remove a <a href="/../subobjects/condition" target="_blank">`Condition`</a> object.

        Args:
            condition (Union[Condition, int]): `Condition` object to remove

        ``` py title="Example"
        process.remove_condition(condition)
        ```
        """
        self._remove_node(condition, "conditions")

    @beartype
    def add_property(self, property: Union[Property, dict]):
        """Add a <a href="/../subobjects/property" target="_blank">`Property`</a> object.

        Args:
            property (Union[Property, dict]): `Property` object to add

        ``` py title="Example"
        process.add_property(property)
        ```
        """
        self._add_node(property, "properties")

    @beartype
    def remove_property(self, property: Union[Property, int]):
        """Remove a <a href="/../subobjects/property" target="_blank">`Property`</a> object.

        Args:
            property (Union[Property, int]): `Property` object to remove

        ``` py title="Example"
        process.remove_property(property)
        ```
        """
        self._remove_node(property, "properties")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        """Add a <a href="/../subobjects/citation" target="_blank">`Citation`</a> object.

        Args:
            citation (Union[Citation, dict]): `Citation` object to add

        ``` py title="Example"
        process.add_citation(citation)
        ```
        """
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        """Remove a <a href="/../subobjects/citation" target="_blank">`Citation`</a> object.

        Args:
            citation (Union[Citation, int]): `Citation` object to remove

        ``` py title="Example"
        process.remove_citation(citation)
        ```
        """
        self._remove_node(citation, "citations")
