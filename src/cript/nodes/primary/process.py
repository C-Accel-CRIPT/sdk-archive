from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes import (
    Base,
    Group,
    Experiment,
    Ingredient,
    Material,
    Property,
    Condition,
    Citation,
)
from cript.validators import validate_required, validate_key
from cript.utils import auto_assign_group


logger = getLogger(__name__)


class Process(Base):
    """
    Object representing a process of creating or transforming
    a :class:`Material` object.
    """

    node_type = "primary"
    node_name = "Process"
    slug = "process"
    list_name = "processes"
    required = ["group", "experiment", "name"]
    unique_together = ["experiment", "name"]

    @beartype
    def __init__(
        self,
        group: Union[Group, str] = None,
        experiment: Union[Experiment, str] = None,
        name: str = None,
        keywords: Union[list[str], None] = None,
        description: Union[str, None] = None,
        prerequisite_processes: list[Union[Base, str]] = None,
        ingredients: list[Union[Ingredient, dict]] = None,
        equipment: list[Union[str, None]] = None,
        properties: list[Union[Property, dict]] = None,
        conditions: list[Union[Condition, dict]] = None,
        set_id: Union[int, None] = None,
        products: list[Union[Material, str]] = None,
        citations: list[Union[Citation, dict]] = None,
        notes: Union[str, None] = None,
        public: bool = False,
    ):
        super().__init__()
        self.url = None
        self.uid = None
        self.group = auto_assign_group(group, experiment)
        self.experiment = experiment
        self.name = name
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
        self.citations = citations if citations else []
        self.notes = notes
        self.public = public
        self.created_at = None
        self.updated_at = None
        validate_required(self)

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, value):
        if value:
            for i in range(len(value)):
                value[i] = validate_key("process-keyword", value[i])
        self._keywords = value

    @property
    def equipment(self):
        return self._equipment

    @equipment.setter
    def equipment(self, value):
        if value:
            for i in range(len(value)):
                value[i] = validate_key("equipment", value[i])
        self._equipment = value

    @beartype
    def add_prerequisite_process(self, process: Union[Base, dict]):
        self._add_node(process, "prerequisite_processes")

    @beartype
    def remove_prerequisite_process(self, process: Union[Base, int]):
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
