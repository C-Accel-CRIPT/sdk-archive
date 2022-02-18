import json
import copy
from typing import Union

from beartype import beartype

from .errors import AddNodeError, RemoveNodeError, UnsavedNodeError


class Base:
    """
    The base CRIPT class node.
    All nodes inherit from this class.
    """

    def __init__(self):
        self.created_at = None
        self.updated_at = None

    def __repr__(self):
        return self._to_json()

    def __str__(self):
        return self._to_json()

    def print_json(self):
        print(self._to_json())

    def _to_json(self):
        return json.dumps(self._prep_for_upload(), indent=4)

    def _prep_for_upload(self):
        """Convert a node into a dict that can be sent to the API."""
        node_dict = copy.deepcopy(self.__dict__)
        for key, value in node_dict.items():
            # Check if the value is a node
            if isinstance(value, Base):
                if value.node_type == "primary":
                    # Check if primary node has been saved
                    if value.url is None:
                        raise UnsavedNodeError(value.node_name)
                    node_dict[key] = value.url
                elif value.node_type == "secondary":
                    node_dict[key] = value._prep_for_upload()
            elif isinstance(value, list):
                for i in range(len(value)):
                    if isinstance(value[i], Base):
                        if value[i].node_type == "primary":
                            # Check if primary node has been saved
                            if value[i].url is None:
                                raise UnsavedNodeError(value[i].node_name)
                            value[i] = value[i].url
                        elif value[i].node_type == "secondary":
                            value[i] = value[i]._prep_for_upload()
        return node_dict

    def _add_node(self, node, attr_name):
        """
        Append a node to another node's list attribute.

        :param node: The node that will be appended.
        :param attr: The name of the list attribute (e.g., conditions).
        """
        if node.node_type == "primary" and node.url is None:
            raise UnsavedNodeError(node.node_name)
        elif hasattr(self, attr_name):
            getattr(self, attr_name).append(node)
        else:
            raise AddNodeError(node.node_name, self.node_name)

    def _remove_node(self, node, attr):
        """
        Remove a node from another node's list attribute.

        :param node: The node that will be removed or it's position in the list.
        :param attr: The name of the list attribute (e.g., conditions).
        """
        if isinstance(node, int):
            getattr(self, attr).pop(node)
        elif hasattr(self, attr):
            if node.node_type == "primary":
                getattr(self, attr).remove(node.url)
            elif node.node_type == "secondary":
                getattr(self, attr).remove(node)
        else:
            raise RemoveNodeError(node.node_name, self.node_name)


class Group(Base):
    node_type = "primary"
    node_name = "Group"
    slug = "group"

    @beartype
    def __init__(self, name: str, users: list[str], url: Union[str, None] = None):
        super().__init__()
        self.url = url
        self.name = name
        self.users = users


class Data(Base):
    node_type = "primary"
    node_name = "Data"
    slug = "data"

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        name: str,
        type: str,
        files: list[str] = None,
        sample_prep: Union[str, None] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        url: Union[str, None] = None,
    ):
        super().__init__()
        self.url = url
        self.group = group
        self.name = name
        self.files = files
        self.type = type
        self.sample_prep = sample_prep
        self.notes = notes
        self.public = public


class File(Base):
    node_type = "primary"
    node_name = "File"
    slug = "file"

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        data: Union[Data, str],
        source: Union[str, None],
        name: Union[str, None] = None,
        extension: Union[str, None] = None,
        public: bool = False,
        url: Union[str, None] = None,
    ):
        super().__init__()
        self.url = url
        self.group = group
        self.data = data
        self.source = source
        self.name = name
        self.extension = extension
        self.public = public


class Condition(Base):
    node_type = "secondary"
    node_name = "Condition"

    @beartype
    def __init__(
        self,
        key: str,
        value: Union[str, int, float],
        unit: Union[str, None] = None,
        uncertainty: float = None,
        uncertainty_type: str = None,
        set_id: int = None,
        measurement_id: int = None,
        data: list[Union[Data, str]] = None,
    ):
        self.key = key
        self.value = value
        self.unit = unit
        self.uncertainty = uncertainty
        self.uncertainty_type = uncertainty_type
        self.set_id = set_id
        self.measurement_id = measurement_id
        self.data = data if data else []

    @beartype
    def add_data(self, data: Union[Data, dict]):
        self._add_node(data, "data")

    @beartype
    def remove_data(self, data: Union[Data, int]):
        self._remove_node(data, "data")


class Property(Base):
    node_type = "secondary"
    node_name = "Property"

    @beartype
    def __init__(
        self,
        key: str,
        value: Union[str, int, float],
        unit: Union[str, None] = None,
        method: Union[str, None] = None,
        reference_material: Union[str, None] = None,
        uncertainty: float = None,
        uncertainty_type: str = None,
        set_id: int = None,
        data: list[Union[Data, str]] = None,
        conditions: list[Union[Condition, dict]] = None,
    ):
        self.key = key
        self.value = value
        self.unit = unit
        self.method = method
        self.reference_material = reference_material
        self.uncertainty = uncertainty
        self.uncertainty_type = uncertainty_type
        self.set_id = set_id
        self.data = data if data else []
        self.conditions = conditions if conditions else []

    @beartype
    def add_data(self, data: Union[Data, dict]):
        self._add_node(data, "data")

    @beartype
    def remove_data(self, data: Union[Data, int]):
        self._remove_node(data, "data")

    @beartype
    def add_condition(self, condition: Union[Condition, dict]):
        self._add_node(condition, "conditions")

    @beartype
    def remove_condition(self, condition: Union[Condition, int]):
        self._remove_node(condition, "conditions")


class Collection(Base):
    node_type = "primary"
    node_name = "Collection"
    slug = "collection"

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        name: str,
        notes: Union[str, None] = None,
        experiments: list[Union[Base, str]] = None,  # Needs more specific type check
        public: bool = False,
        url: Union[str, None] = None,
    ):
        super().__init__()
        self.url = url
        self.group = group
        self.name = name
        self.notes = notes
        self.experiments = experiments if experiments else []
        self.public = public

    def add_experiment(self, experiment):
        self._add_node(experiment, "experiments")

    def remove_experiment(self, experiment):
        self._remove_node(experiment, "experiments")


class Identity(Base):
    node_type = "primary"
    node_name = "Identity"
    slug = "identity"

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        name: str,
        names: Union[list[str], None] = None,
        cas: Union[str, None] = None,
        smiles: Union[str, None] = None,
        bigsmiles: Union[str, None] = None,
        chem_formula: Union[str, None] = None,
        chem_repeat: Union[str, None] = None,
        pubchem_cid: Union[str, None] = None,
        inchi: Union[str, None] = None,
        inchi_key: Union[str, None] = None,
        public: bool = False,
        url: Union[str, None] = None,
    ):
        super().__init__()
        self.url = url
        self.group = group
        self.name = name
        self.names = names
        self.cas = cas
        self.smiles = smiles
        self.bigsmiles = bigsmiles
        self.chem_formula = chem_formula
        self.chem_repeat = chem_repeat
        self.pubchem_cid = pubchem_cid
        self.inchi = inchi
        self.inchi_key = inchi_key
        self.public = public


class MaterialComponent(Base):
    node_type = "secondary"
    node_name = "MaterialComponent"

    @beartype
    def __init__(self, identity: Union[Identity, str], component_id: int = 0):
        self.component_id = component_id
        self.identity = identity


class Quantity(Base):
    node_type = "secondary"
    node_name = "Quantity"

    @beartype
    def __init__(
        self,
        key: str,
        value: Union[int, float],
        unit: Union[str, None] = None,
    ):
        self.key = key
        self.value = value
        self.unit = unit


class Specification(Base):
    node_type = "secondary"
    node_name = "Specification"

    @beartype
    def __init__(
        self,
        vendor: str = None,
        lot_number: str = None,
        storage_location: str = None,
        quantity: Quantity = None,
        initial_quantity: Quantity = None,
        container: str = None,
    ):
        self.vendor = vendor
        self.lot_number = lot_number
        self.storage_location = storage_location
        self.quantity = quantity
        self.initial_quantity = initial_quantity
        self.container = container


class Material(Base):
    node_type = "primary"
    node_name = "Material"
    slug = "material"

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        name: str,
        components: list[Union[MaterialComponent, dict]] = None,
        source: Union[str, None] = None,
        keywords: Union[list[str], None] = None,
        notes: Union[str, None] = None,
        experiments: list[Union[Base, str]] = None,  # Needs more specific type check
        step: Union[Base, str] = None,  # Needs more specific type check
        properties: list[Union[Property, dict]] = None,
        public: bool = False,
        url: Union[str, None] = None,
    ):
        super().__init__()
        self.url = url
        self.group = group
        self.name = name
        self.components = components if components else []
        self.source = source
        self.keywords = keywords
        self.notes = notes
        self.experiments = experiments if experiments else []
        self.step = step
        self.properties = properties if properties else []
        self.public = public

    def add_experiment(self, experiment):
        self._add_node(experiment, "experiments")

    def remove_experiment(self, experiment):
        self._remove_node(experiment, "experiments")

    @beartype
    def add_component(self, component: Union[MaterialComponent, dict]):
        self._add_node(component, "components")

    @beartype
    def remove_component(self, component: Union[MaterialComponent, int]):
        self._remove_node(component, "components")

    @beartype
    def add_property(self, property: Union[Property, dict]):
        self._add_node(property, "properties")

    @beartype
    def remove_property(self, property: Union[Property, int]):
        self._remove_node(property, "properties")


class IntermediateIngredient(Base):
    node_type = "secondary"
    node_name = "IntermediateIngredient"

    @beartype
    def __init__(
        self,
        ingredient: Union[Base, str],  # Needs more specific type check
        keyword: str = None,
        quantity: list[Union[Quantity, dict]] = None,
        method: Union[str, None] = None,
    ):
        self.ingredient = ingredient
        self.keyword = keyword
        self.quantity = quantity if quantity else []
        self.method = method

    @beartype
    def add_quantity(self, quantity: Union[Quantity, dict]):
        self._add_node(quantity, "quantity")

    @beartype
    def remove_quantity(self, quantity: Union[Quantity, int]):
        self._remove_node(quantity, "quantity")


class MaterialIngredient(Base):
    node_type = "secondary"
    node_name = "MaterialIngredient"

    @beartype
    def __init__(
        self,
        ingredient: Union[Material, str],
        keyword: str = None,
        quantity: list[Union[Quantity, dict]] = None,
        method: Union[str, None] = None,
    ):
        self.ingredient = ingredient
        self.keyword = keyword
        self.quantity = quantity if quantity else []
        self.method = method

    @beartype
    def add_quantity(self, quantity: Union[Quantity, dict]):
        self._add_node(quantity, "quantity")

    @beartype
    def remove_quantity(self, quantity: Union[Quantity, int]):
        self._remove_node(quantity, "quantity")


class Step(Base):
    node_type = "primary"
    node_name = "Step"

    @beartype
    def __init__(
        self,
        description: Union[str, None] = None,
        product_ingredients: list[Union[IntermediateIngredient, dict]] = None,
        material_ingredients: list[Union[MaterialIngredient, dict]] = None,
        properties: list[Union[Property, dict]] = None,
        conditions: list[Union[Condition, dict]] = None,
        url: Union[str, None] = None,
    ):
        self.url = url
        self.description = description
        self.product_ingredients = product_ingredients if product_ingredients else []
        self.material_ingredients = material_ingredients if material_ingredients else []
        self.properties = properties if properties else []
        self.conditions = conditions if conditions else []

    @beartype
    def add_ingredient(
        self, ingredient: Union[IntermediateIngredient, MaterialIngredient, dict]
    ):
        if isinstance(ingredient, IntermediateIngredient):
            self._add_node(ingredient, "product_ingredients")
        elif isinstance(ingredient, MaterialIngredient):
            self._add_node(ingredient, "material_ingredients")

    @beartype
    def remove_ingredient(
        self, ingredient: Union[IntermediateIngredient, MaterialIngredient, int]
    ):
        if isinstance(ingredient, IntermediateIngredient):
            self._remove_node(ingredient, "product_ingredients")
        elif isinstance(ingredient, MaterialIngredient):
            self._remove_node(ingredient, "material_ingredients")

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


class Process(Base):
    node_type = "primary"
    node_name = "Process"
    slug = "process"

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        name: str,
        keywords: Union[list[str], None] = None,
        notes: Union[str, None] = None,
        experiments: list[Union[Base, str]] = None,  # Needs more specific type check
        steps: list[Union[Step, dict]] = None,
        public: bool = False,
        url: Union[str, None] = None,
    ):
        super().__init__()
        self.url = url
        self.group = group
        self.name = name
        self.keywords = keywords
        self.notes = notes
        self.experiments = experiments if experiments else []
        self.steps = steps if steps else []
        self.public = public

    def add_experiment(self, experiment):
        self._add_node(experiment, "experiments")

    def remove_experiment(self, experiment):
        self._remove_node(experiment, "experiments")

    @beartype
    def add_step(self, step: Union[Step, dict]):
        self._add_node(step, "steps")

    @beartype
    def remove_step(self, step: Union[Step, int]):
        self._remove_node(step, "steps")


class Experiment(Base):
    node_type = "primary"
    node_name = "Experiment"
    slug = "experiment"

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        collection: Union[Collection, str],
        name: str,
        funding: Union[str, None] = None,
        notes: Union[str, None] = None,
        materials: list[Union[Material, str]] = None,
        processes: list[Union[Process, str]] = None,
        data: list[Union[Data, str]] = None,
        public: bool = False,
        url: Union[str, None] = None,
    ):
        super().__init__()
        self.url = url
        self.group = group
        self.collection = collection
        self.name = name
        self.funding = funding
        self.notes = notes
        self.notes = notes
        self.materials = materials if materials else []
        self.processes = processes if processes else []
        self.data = data if data else []
        self.public = public
