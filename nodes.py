import json
import copy
from typing import Union

from beartype import beartype
from weakref import WeakSet

from .errors import AddNodeError, RemoveNodeError, UnsavedNodeError


class Base:
    """
    The base CRIPT class node.
    All nodes inherit from this class.
    """

    __refs__ = WeakSet()  # Set() of all node instances

    def __init__(self):
        self.__refs__.add(self)  # Add instance to __refs__

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


class User(Base):
    node_type = "primary"
    node_name = "User"
    slug = "user"
    list_name = "users"

    @beartype
    def __init__(self, email: str, url: Union[str, None] = None):
        super().__init__()
        self.url = url
        self.email = email


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


class Reference(Base):
    node_type = "primary"
    node_name = "Reference"
    slug = "reference"

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        title: str,
        doi: str,
        authors: Union[list[str], None] = None,
        journal: Union[str, None] = None,
        publisher: Union[str, None] = None,
        year: Union[int, None] = None,
        volume: Union[int, None] = None,
        issue: Union[int, None] = None,
        pages: Union[list[int], None] = None,
        issn: Union[str, None] = None,
        arxiv_id: Union[str, None] = None,
        pmid: Union[int, None] = None,
        website: Union[str, None] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        url: Union[str, None] = None,
    ):
        super().__init__()
        self.url = url
        self.group = group
        self.title = title
        self.doi = doi
        self.authors = authors
        self.journal = journal
        self.publisher = publisher
        self.year = year
        self.volume = volume
        self.issue = issue
        self.pages = pages
        self.issn = issn
        self.arxiv_id = arxiv_id
        self.pmid = pmid
        self.website = website
        self.notes = notes
        self.created_at = None
        self.updated_at = None
        self.public = public


class Citation(Base):
    node_type = "secondary"
    node_name = "Citation"
    list_name = "citations"

    @beartype
    def __init__(
        self, reference: Union[Reference, str], method: Union[str, None] = None
    ):
        super().__init__()
        self.method = method
        self.reference = reference


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
        citations: list[Union[Citation, dict]] = None,
        public: bool = False,
        url: Union[str, None] = None,
        experiments=None,
        inventories=None,
    ):
        super().__init__()
        self.url = url
        self.group = group
        self.name = name
        self.notes = notes
        self.experiments = experiments if experiments else []
        self.inventories = inventories if inventories else []
        self.citations = citations if citations else []
        self.created_at = None
        self.updated_at = None
        self.public = public

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        self._remove_node(citation, "citations")


class Experiment(Base):
    node_type = "primary"
    node_name = "Experiment"
    slug = "experiment"
    list_name = "experiments"

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        collection: Union[Collection, str],
        name: str,
        funding: Union[str, None] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        url: Union[str, None] = None,
        processes=None,
        data=None,
    ):
        super().__init__()
        self.url = url
        self.group = group
        self.collection = collection
        self.name = name
        self.funding = funding
        self.notes = notes
        self.notes = notes
        self.processes = processes if processes else []
        self.data = data if data else []
        self.created_at = None
        self.updated_at = None
        self.public = public


class Data(Base):
    node_type = "primary"
    node_name = "Data"
    slug = "data"
    list_name = "data"

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        experiment: Union[Base, str],
        name: str,
        type: str,
        files: list[Union[Base, str]] = None,
        sample_prep: Union[str, None] = None,
        calibration: Union[str, None] = None,
        configuration: Union[str, None] = None,
        notes: Union[str, None] = None,
        citations: list[Union[Citation, dict]] = None,
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
        self.calibration = calibration
        self.configuration = configuration
        self.notes = notes
        self.experiment = experiment
        self.citations = citations if citations else []
        self.created_at = None
        self.updated_at = None
        self.public = public

    @beartype
    def add_file(self, citation: Union[Base, dict]):
        self._add_node(citation, "files")

    @beartype
    def remove_file(self, citation: Union[Base, int]):
        self._remove_node(citation, "files")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        self._remove_node(citation, "citations")


class File(Base):
    node_type = "primary"
    node_name = "File"
    slug = "file"
    list_name = "files"

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
        self.created_at = None
        self.updated_at = None
        self.public = public


class Condition(Base):
    node_type = "secondary"
    node_name = "Condition"
    list_name = "conditions"

    @beartype
    def __init__(
        self,
        key: str,
        value: Union[str, int, float],
        unit: Union[str, None] = None,
        uncertainty: Union[float, None] = None,
        uncertainty_type: Union[str, None] = None,
        set_id: Union[int, None] = None,
        measurement_id: Union[int, None] = None,
        data: list[Union[Data, str]] = None,
    ):
        super().__init__()
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
    list_name = "properties"

    @beartype
    def __init__(
        self,
        key: str,
        value: Union[str, int, float],
        unit: Union[str, None] = None,
        method: Union[str, None] = None,
        method_description: Union[str, None] = None,
        uncertainty: Union[float, None] = None,
        uncertainty_type: Union[str, None] = None,
        set_id: Union[int, None] = None,
        data: list[Union[Data, str]] = None,
        conditions: list[Union[Condition, dict]] = None,
    ):
        super().__init__()
        self.key = key
        self.value = value
        self.unit = unit
        self.method = method
        self.method_description = method_description
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
        self.created_at = None
        self.updated_at = None
        self.public = public


class Component(Base):
    node_type = "secondary"
    node_name = "Component"
    list_name = "components"

    @beartype
    def __init__(self, identity: Union[Identity, str], component_id: int = 0):
        super().__init__()
        self.component_id = component_id
        self.identity = identity


class Quantity(Base):
    node_type = "secondary"
    node_name = "Quantity"
    list_name = "quantity"

    @beartype
    def __init__(
        self,
        key: str,
        value: Union[int, float],
        unit: Union[str, None] = None,
    ):
        super().__init__()
        self.key = key
        self.value = value
        self.unit = unit


class Material(Base):
    node_type = "primary"
    node_name = "Material"
    slug = "material"
    list_name = "materials"

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        name: str,
        components: list[Union[Component, dict]] = None,
        vendor: Union[str, None] = None,
        lot_number: Union[str, None] = None,
        keywords: Union[list[str], None] = None,
        notes: Union[str, None] = None,
        step: Union[Base, str, None] = None,  # Needs more specific type check
        properties: list[Union[Property, dict]] = None,
        citations: list[Union[Citation, dict]] = None,
        public: bool = False,
        url: Union[str, None] = None,
    ):
        super().__init__()
        self.url = url
        self.group = group
        self.name = name
        self.components = components if components else []
        self.vendor = vendor
        self.lot_number = lot_number
        self.keywords = keywords
        self.notes = notes
        self.step = step
        self.properties = properties if properties else []
        self.citations = citations if citations else []
        self.created_at = None
        self.updated_at = None
        self.public = public

    def add_experiment(self, experiment):
        self._add_node(experiment, "experiments")

    def remove_experiment(self, experiment):
        self._remove_node(experiment, "experiments")

    @beartype
    def add_component(self, component: Union[Component, dict]):
        self._add_node(component, "components")

    @beartype
    def remove_component(self, component: Union[Component, int]):
        self._remove_node(component, "components")

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


class Inventory(Base):
    node_type = "primary"
    node_name = "Inventory"
    slug = "inventory"

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        collection: Union[Collection, str],
        name: str,
        materials: list[Union[Material, str]],
        description: str = None,
        public: bool = False,
        url: Union[str, None] = None,
    ):
        super().__init__()
        self.url = url
        self.group = group
        self.collection = collection
        self.name = name
        self.description = description
        self.materials = materials
        self.created_at = None
        self.updated_at = None
        self.public = public

    @beartype
    def add_material(self, material: Union[Material, dict]):
        self._add_node(material, "materials")

    @beartype
    def remove_material(self, material: Union[Material, int]):
        self._remove_node(material, "materials")


class IntermediateIngredient(Base):
    node_type = "secondary"
    node_name = "IntermediateIngredient"
    list_name = "intermediate_ingredients"

    @beartype
    def __init__(
        self,
        ingredient: Union[Base, str],  # Needs more specific type check
        keyword: str = None,
        quantity: list[Union[Quantity, dict]] = None,
        method: Union[str, None] = None,
    ):
        super().__init__()
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
    list_name = "material_ingredients"

    @beartype
    def __init__(
        self,
        ingredient: Union[Material, str],
        keyword: str = None,
        quantity: list[Union[Quantity, dict]] = None,
        method: Union[str, None] = None,
    ):
        super().__init__()
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


class Process(Base):
    node_type = "primary"
    node_name = "Process"
    slug = "process"
    list_name = "processes"

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        experiment: Union[Experiment, str],
        name: str,
        keywords: Union[list[str], None] = None,
        notes: Union[str, None] = None,
        citations: list[Union[Citation, dict]] = None,
        public: bool = False,
        url: Union[str, None] = None,
        steps=None,
    ):
        super().__init__()
        self.url = url
        self.group = group
        self.experiment = experiment
        self.name = name
        self.keywords = keywords
        self.notes = notes
        self.steps = steps if steps else []
        self.created_at = None
        self.updated_at = None
        self.citations = citations if citations else []
        self.public = public

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        self._remove_node(citation, "citations")


class Step(Base):
    node_type = "primary"
    node_name = "Step"
    slug = "step"
    list_name = "steps"

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        process: Union[Process, str],
        type: str,
        description: Union[str, None] = None,
        intermediate_ingredients: list[Union[IntermediateIngredient, dict]] = None,
        material_ingredients: list[Union[MaterialIngredient, dict]] = None,
        equipment: Union[list[str], None] = None,
        duration: Union[Quantity, dict, None] = None,
        time_position: Union[Quantity, dict, None] = None,
        properties: list[Union[Property, dict]] = None,
        conditions: list[Union[Condition, dict]] = None,
        set_id: Union[int, None] = None,
        material_products: list[Union[Material, str]] = None,
        public: bool = False,
        url: Union[str, None] = None,
    ):
        super().__init__()
        self.url = url
        self.group = group
        self.process = process
        self.type = type
        self.description = description
        self.intermediate_ingredients = (
            intermediate_ingredients if intermediate_ingredients else []
        )
        self.material_ingredients = material_ingredients if material_ingredients else []
        self.equipment = equipment
        self.duration = duration
        self.time_position = time_position
        self.properties = properties if properties else []
        self.conditions = conditions if conditions else []
        self.set_id = set_id
        self.material_products = material_products if material_products else []
        self.created_at = None
        self.updated_at = None
        self.public = public

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
    def add_product(self, material: Union[Material, dict]):
        self._add_node(material, "material_products")

    @beartype
    def remove_product(self, material: Union[Material, int]):
        self._remove_node(material, "material_products")

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
