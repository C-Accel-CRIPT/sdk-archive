import os
import json
import copy
from abc import ABCMeta
from typing import Union
from weakref import WeakSet
from logging import getLogger

from beartype import beartype

from cript.exceptions import AddNodeError, RemoveNodeError, UnsavedNodeError
from cript.validators import (
    validate_required,
    validate_key,
    validate_value,
    validate_unit,
)
from cript.utils import sha256_hash


logger = getLogger(__name__)


class Base(metaclass=ABCMeta):
    """
    The base abstract class for a CRIPT node.
    All nodes inherit from this class (note that this class cannot be directly
    instantiated).
    """

    __refs__ = WeakSet()  # Stores all node instances in memory

    def __init__(self):
        self.__refs__.add(self)  # Add instance to __refs__

    def __repr__(self):
        return self._to_json()

    def __str__(self):
        return self._to_json()

    def as_dict(self):
        """
        Convert a node object to a cleaned dictionary.

        :return: The cleaned dictionary.
        """
        return {k.lstrip("_"): self.__getattribute__(k) for k in vars(self)}

    def print_json(self):
        print(self._to_json())

    def _to_json(self):
        return json.dumps(self._prep_for_upload(), indent=4)

    def _prep_for_upload(self):
        """Convert a node into a dict that can be sent to the API."""
        node_dict = copy.deepcopy(self.as_dict())
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
    def __init__(
        self,
        username: str = None,
        email: str = None,
        orcid_id: str = None,
        public: bool = False,
        groups=None,
    ):
        super().__init__()
        self.url = None
        self.uid = None
        self.username = username
        self.email = email
        self.orcid_id = orcid_id
        self.groups = groups if groups else []
        self.public = public
        self.created_at = None
        self.updated_at = None


class Group(Base):
    node_type = "primary"
    node_name = "Group"
    slug = "group"
    required = ["name", "users"]
    unique_together = ["name"]

    @beartype
    def __init__(
        self,
        name: str = None,
        users: list[Union[User, str]] = None,
        public: bool = False,
    ):
        super().__init__()
        self.url = None
        self.uid = None
        self.name = name
        self.users = users
        self.public = public
        self.created_at = None
        self.updated_at = None
        validate_required(self)

    @beartype
    def add_user(self, user: Union[User, dict]):
        self._add_node(user, "users")

    @beartype
    def remove_user(self, user: Union[User, int]):
        self._remove_node(user, "users")


class Reference(Base):
    node_type = "primary"
    node_name = "Reference"
    slug = "reference"
    required = ["group", "title", "doi"]
    unique_together = ["doi"]

    @beartype
    def __init__(
        self,
        group: Union[Group, str] = None,
        title: str = None,
        doi: str = None,
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
    ):
        super().__init__()
        self.url = None
        self.uid = None
        self.group = group
        self.title = title
        self.doi = doi
        self.authors = authors if authors else []
        self.journal = journal
        self.publisher = publisher
        self.year = year
        self.volume = volume
        self.issue = issue
        self.pages = pages if pages else []
        self.issn = issn
        self.arxiv_id = arxiv_id
        self.pmid = pmid
        self.website = website
        self.notes = notes
        self.public = public
        self.created_at = None
        self.updated_at = None
        validate_required(self)


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
    required = ["group", "name"]
    unique_together = ["name", "created_by"]

    @beartype
    def __init__(
        self,
        group: Union[Group, str] = None,
        name: str = None,
        notes: Union[str, None] = None,
        citations: list[Union[Citation, dict]] = None,
        public: bool = False,
        experiments=None,
        inventories=None,
    ):
        super().__init__()
        self.url = None
        self.uid = None
        self.group = group
        self.name = name
        self.notes = notes
        self.experiments = experiments if experiments else []
        self.inventories = inventories if inventories else []
        self.citations = citations if citations else []
        self.public = public
        self.created_at = None
        self.updated_at = None
        validate_required(self)

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
    required = ["group", "collection", "name"]
    unique_together = ["collection", "name"]

    @beartype
    def __init__(
        self,
        group: Union[Group, str] = None,
        collection: Union[Collection, str] = None,
        name: str = None,
        funding: list[Union[str, None]] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        processes=None,
        data=None,
    ):
        super().__init__()
        self.url = None
        self.uid = None
        self.group = group
        self.collection = collection
        self.name = name
        self.funding = funding if funding else []
        self.notes = notes
        self.notes = notes
        self.processes = processes if processes else []
        self.data = data if data else []
        self.public = public
        self.created_at = None
        self.updated_at = None
        validate_required(self)


class Data(Base):
    node_type = "primary"
    node_name = "Data"
    slug = "data"
    list_name = "data"
    required = ["group", "experiment", "name", "type"]
    unique_together = ["experiment", "name"]

    @beartype
    def __init__(
        self,
        group: Union[Group, str] = None,
        experiment: Union[Base, str] = None,
        name: str = None,
        type: str = None,
        sample_prep: Union[str, None] = None,
        calibration: Union[str, None] = None,
        configuration: Union[str, None] = None,
        notes: Union[str, None] = None,
        citations: list[Union[Citation, dict]] = None,
        public: bool = False,
        files=None,
        materials=None,
        processes=None,
    ):
        super().__init__()
        self.url = None
        self.uid = None
        self.group = group
        self.name = name
        self.files = files
        self.type = type
        self.sample_prep = sample_prep
        self.calibration = calibration
        self.configuration = configuration
        self.notes = notes
        self.experiment = experiment
        self.materials = materials if materials else []
        self.processes = processes if processes else []
        self.citations = citations if citations else []
        self.public = public
        self.created_at = None
        self.updated_at = None
        validate_required(self)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = validate_key("data-type", value)

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
    required = ["group", "data", "source", "type"]
    unique_together = ["checksum", "created_by"]

    @beartype
    def __init__(
        self,
        group: Union[Group, str] = None,
        data: list[Union[Data, str]] = None,
        source: str = None,
        type: str = None,
        checksum: Union[str, None] = None,
        extension: Union[str, None] = None,
        external_source: Union[str, None] = None,
        public: bool = False,
        name=None,
    ):
        super().__init__()
        self.url = None
        self.uid = None
        self.group = group
        self.data = data
        self.checksum = checksum
        self.name = name
        self.source = source
        self.extension = extension
        self.external_source = external_source
        self.type = type
        self.public = public
        self.created_at = None
        self.updated_at = None
        validate_required(self)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = validate_key("file-type", value)

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        value = value.replace("\\", "/")
        if os.path.exists(value):
            print("Generating checksum ...")
            self.checksum = sha256_hash(value)
            print("Complete.")
            self.name = os.path.basename(value)
        elif value.startswith(("http", "https")) or not value:
            pass
        else:
            raise FileNotFoundError(
                "The file could not be found on the local filesystem."
            )
        self._source = value

    @beartype
    def add_data(self, data: Union[Data, dict]):
        self._add_node(data, "data")

    @beartype
    def remove_data(self, data: Union[Data, int]):
        self._remove_node(data, "data")


class Condition(Base):
    node_type = "secondary"
    node_name = "Condition"
    list_name = "conditions"
    required = ["key"]

    @beartype
    def __init__(
        self,
        key: str = None,
        value: Union[str, int, float, list, None] = None,
        unit: Union[str, None] = None,
        type: Union[str, None] = None,
        uncertainty: Union[float, None] = None,
        uncertainty_type: Union[str, None] = None,
        set_id: Union[int, None] = None,
        measurement_id: Union[int, None] = None,
        data: list[Union[Data, str]] = None,
    ):
        super().__init__()
        self.key = key
        self.unit = unit
        self.value = value
        self.type = type
        self.uncertainty = uncertainty
        self.uncertainty_type = uncertainty_type
        self.set_id = set_id
        self.measurement_id = measurement_id
        self.data = data if data else []
        validate_required(self)

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = validate_key("condition-key", value)

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        self._unit = validate_unit("condition-key", self.key, value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = validate_value("condition-key", self.key, value, self.unit)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = validate_key("set-type", value)

    @property
    def uncertainty_type(self):
        return self._uncertainty_type

    @uncertainty_type.setter
    def uncertainty_type(self, value):
        self._uncertainty_type = validate_key("uncertainty-type", value)

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
    required = ["key", "value"]

    @beartype
    def __init__(
        self,
        key: str = None,
        value: Union[str, int, float, list, None] = None,
        unit: Union[str, None] = None,
        type: Union[str, None] = None,
        method: Union[str, None] = None,
        method_description: Union[str, None] = None,
        uncertainty: Union[float, None] = None,
        uncertainty_type: Union[str, None] = None,
        component_id: Union[int, None] = None,
        structure: Union[str, None] = None,
        set_id: Union[int, None] = None,
        data: list[Union[Data, str]] = None,
        conditions: list[Union[Condition, dict]] = None,
    ):
        super().__init__()
        self.key = key
        self.unit = unit
        self.value = value
        self.type = type
        self.method = method
        self.method_description = method_description
        self.uncertainty = uncertainty
        self.uncertainty_type = uncertainty_type
        self.component_id = component_id
        self.structure = structure
        self.set_id = set_id
        self.data = data if data else []
        self.conditions = conditions if conditions else []
        validate_required(self)

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = validate_key("property-key", value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = validate_value("property-key", self.key, value, self.unit)

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        self._unit = validate_unit("property-key", self.key, value)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = validate_key("set-type", value)

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        self._method = validate_key("property-method", value)

    @property
    def uncertainty_type(self):
        return self._uncertainty_type

    @uncertainty_type.setter
    def uncertainty_type(self, value):
        self._uncertainty_type = validate_key("uncertainty-type", value)

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


class Identifier(Base):
    node_type = "secondary"
    node_name = "Identifier"
    list_name = "identifiers"
    required = ["key", "value"]

    @beartype
    def __init__(self, key: str = None, value: Union[str, int, float, list] = None):
        super().__init__()
        self.key = key
        self.value = value
        validate_required(self)

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = validate_key("material-identifier-key", value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = validate_value("material-identifier-key", self.key, value)


class Quantity(Base):
    node_type = "secondary"
    node_name = "Quantity"
    list_name = "quantities"
    required = ["key", "value"]

    @beartype
    def __init__(
        self,
        key: str = None,
        value: Union[int, float] = None,
        unit: Union[str, None] = None,
    ):
        super().__init__()
        self.key = key
        self.unit = unit
        self.value = value
        validate_required(self)

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = validate_key("quantity-key", value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = validate_value("quantity-key", self.key, value, self.unit)

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        self._unit = validate_unit("quantity-key", self.key, value)


class Component(Base):
    node_type = "secondary"
    node_name = "Component"
    list_name = "components"
    required = ["component"]

    @beartype
    def __init__(self, component_uid: int = 1, component: Union[Base, str] = None):
        super().__init__()
        self.component_uid = component_uid
        self.component = component
        validate_required(self)


class Material(Base):
    node_type = "primary"
    node_name = "Material"
    slug = "material"
    list_name = "materials"
    required = ["group", "name"]
    unique_together = ["name", "created_by"]

    @beartype
    def __init__(
        self,
        group: Union[Group, str] = None,
        name: str = None,
        identifiers: list[Union[Identifier, dict]] = None,
        names: Union[list[str], None] = None,
        components: list[Union[Component, dict]] = None,
        vendor: Union[str, None] = None,
        lot_number: Union[str, None] = None,
        keywords: Union[list[str], None] = None,
        process: Union[Base, str, None] = None,  # Needs more specific type check
        properties: list[Union[Property, dict]] = None,
        citations: list[Union[Citation, dict]] = None,
        notes: Union[str, None] = None,
        public: bool = False,
    ):
        super().__init__()
        self.url = None
        self.uid = None
        self.group = group
        self.name = name
        self.names = names if names else []
        self.identifiers = identifiers
        self.components = components if components else []
        self.vendor = vendor
        self.lot_number = lot_number
        self.keywords = keywords if keywords else []
        self.process = process
        self.properties = properties if properties else []
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
                value[i] = validate_key("material-keyword", value[i])
        self._keywords = value

    @beartype
    def add_identifier(self, identifier: Union[Identifier, dict]):
        self._add_node(identifier, "identifiers")

    @beartype
    def remove_identifier(self, identifier: Union[Identifier, int]):
        self._remove_node(identifier, "identifiers")

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
    required = ["group", "collection", "name"]
    unique_together = ["collection", "name"]

    @beartype
    def __init__(
        self,
        group: Union[Group, str] = None,
        collection: Union[Collection, str] = None,
        name: str = None,
        materials: list[Union[Material, str]] = None,
        description: Union[str, None] = None,
        public: bool = False,
    ):
        super().__init__()
        self.url = None
        self.uid = None
        self.group = group
        self.collection = collection
        self.name = name
        self.description = description
        self.materials = materials
        self.public = public
        self.created_at = None
        self.updated_at = None
        validate_required(self)

    @beartype
    def add_material(self, material: Union[Material, dict]):
        self._add_node(material, "materials")

    @beartype
    def remove_material(self, material: Union[Material, int]):
        self._remove_node(material, "materials")


class Ingredient(Base):
    node_type = "secondary"
    node_name = "Ingredient"
    list_name = "ingredients"
    required = ["ingredient"]

    @beartype
    def __init__(
        self,
        ingredient: Union[Material, str],
        keyword: str = None,
        quantities: list[Union[Quantity, dict]] = None,
    ):
        super().__init__()
        self.ingredient = ingredient
        self.keyword = keyword
        self.quantities = quantities if quantities else []
        validate_required(self)

    @property
    def keyword(self):
        return self._keyword

    @keyword.setter
    def keyword(self, value):
        self._keyword = validate_key("ingredient-keyword", value)

    @beartype
    def add_quantity(self, quantity: Union[Quantity, dict]):
        self._add_node(quantity, "quantities")

    @beartype
    def remove_quantity(self, quantity: Union[Quantity, int]):
        self._remove_node(quantity, "quantities")


class Process(Base):
    node_type = "primary"
    node_name = "Process"
    slug = "process"
    list_name = "processes"
    required = ["group", "experiment", "name"]
    unique_together = ["experiment", "name"]

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        experiment: Union[Experiment, str],
        name: str,
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
        self.group = group
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
