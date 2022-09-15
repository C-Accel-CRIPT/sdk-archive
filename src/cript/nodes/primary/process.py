from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes.primary.group import Group
from cript.nodes.primary.experiment import Experiment
from cript.nodes.primary.material import Material
from cript.nodes.secondary.ingredient import Ingredient
from cript.nodes.secondary.equipment import Equipment
from cript.nodes.secondary.property import Property
from cript.nodes.secondary.condition import Condition
from cript.nodes.secondary.citation import Citation
from cript.validators import validate_key
from cript.utils import auto_assign_group


logger = getLogger(__name__)


class Process(BasePrimary):
    """
    Object representing a process of creating or transforming
    a `Material` object.
    """

    node_name = "Process"
    slug = "process"
    list_name = "processes"

    @beartype
    def __init__(
        self,
        experiment: Union[Experiment, str],
        name: str,
        type: str,
        keywords: Union[list[str], None] = None,
        description: Union[str, None] = None,
        prerequisite_processes: list[Union[BasePrimary, str]] = None,
        ingredients: list[Union[Ingredient, dict]] = None,
        equipment: list[Union[Equipment, dict]] = None,
        properties: list[Union[Property, dict]] = None,
        conditions: list[Union[Condition, dict]] = None,
        set_id: Union[int, None] = None,
        products: list[Union[Material, str]] = None,
        waste: list[Union[Material, str]] = None,
        citations: list[Union[Citation, dict]] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        group: Union[Group, str] = None,
    ):
        super().__init__(public=public)
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
        self.notes = notes
        self.group = auto_assign_group(group, experiment)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = validate_key("process-type", value)

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, value):
        if value:
            for i in range(len(value)):
                value[i] = validate_key("process-keyword", value[i])
        self._keywords = value

    @beartype
    def add_equipment(self, piece: Union[Equipment, dict]):
        self._add_node(piece, "equipment")

    @beartype
    def remove_equipment(self, piece: Union[Equipment, int]):
        self._remove_node(piece, "equipment")

    @beartype
    def add_prerequisite_process(self, process: Union[BasePrimary, dict]):
        self._add_node(process, "prerequisite_processes")

    @beartype
    def remove_prerequisite_process(self, process: Union[BasePrimary, int]):
        self._remove_node(process, "prerequisite_processes")

    @beartype
    def add_ingredient(self, ingredient: Union[Ingredient, dict]):
        self._add_node(ingredient, "ingredients")

    @beartype
    def remove_ingredient(self, ingredient: Union[Ingredient, int]):
        self._remove_node(ingredient, "ingredients")

    @beartype
    def add_product(self, material: Union[Material, dict]):
        self._add_node(material, "products")

    @beartype
    def remove_product(self, material: Union[Material, int]):
        self._remove_node(material, "products")

    @beartype
    def add_waste(self, material: Union[Material, dict]):
        self._add_node(material, "waste")

    @beartype
    def remove_waste(self, material: Union[Material, int]):
        self._remove_node(material, "waste")

    @beartype
    def add_condition(self, condition: Union[Condition, dict]):
        self._add_node(condition, "conditions")

    @beartype
    def remove_condition(self, condition: Union[Condition, int]):
        self._remove_node(condition, "conditions")

    @beartype
    def add_property(self, property: Union[Property, dict]):
        self._add_node(property, "properties")

    @beartype
    def remove_property(self, property: Union[Property, int]):
        self._remove_node(property, "properties")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        self._remove_node(citation, "citations")
