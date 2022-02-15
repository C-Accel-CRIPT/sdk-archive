import json
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

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def print_json(self):
        print(json.dumps(self.to_dict(), indent=4))

    def to_dict(self):
        """Convert a node into a dict that can be sent to the API."""
        node_dict = self.__dict__
        for key, obj in node_dict.items():
            # Check if the obj is a node
            if hasattr(obj, "node_type"):
                if obj.node_type == "primary":
                    # Check if primary node has been saved
                    if obj.url is None:
                        raise UnsavedNodeError(obj.node_name)
                    node_dict[key] = obj.url
                elif obj.node_type == "secondary":
                    node_dict[key] = obj.to_dict()
            elif isinstance(obj, list):
                for i in range(len(obj)):
                    if hasattr(obj[i], "node_type"):
                        if obj[i].node_type == "primary":
                            # Check if primary node has been saved
                            if obj[i].url is None:
                                raise UnsavedNodeError(obj[i].node_name)
                            obj[i] = obj[i].url
                        elif obj[i].node_type == "secondary":
                            obj[i] = obj[i].to_dict()
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
        self.print_json()

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
                getattr(self, attr).remove(node.to_dict())
        else:
            raise RemoveNodeError(node.node_name, self.node_name)
        self.print_json()


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

        self.print_json()


class File(Base):
    node_type = "primary"
    name = "File"
    slug = "file"

    @beartype
    def __init__(
        self,
        group: Union[Group, str],
        source: Union[str, None],
        name: Union[str, None] = None,
        extension: Union[str, None] = None,
        public: bool = False,
        url: Union[str, None] = None,
    ):
        super().__init__()
        self.url = url
        self.group = group
        self.source = source
        self.name = name
        self.extension = extension
        self.public = public


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
        files: list[Union[File, str]] = None,
        sample_prep: Union[str, None] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        url: Union[str, None] = None,
    ):
        super().__init__()
        self.url = url
        self.group = group
        self.name = name
        self.files = files if files else []
        self.type = type
        self.sample_prep = sample_prep
        self.notes = notes
        self.public = public

        self.print_json()

    @beartype
    def add_file(self, file: Union[File, dict]):
        self._add_node(file, "files")

    @beartype
    def remove_file(self, file: Union[File, int]):
        self._remove_node(file, "files")


class Condition(Base):
    node_type = "secondary"
    node_name = "Condition"

    @beartype
    def __init__(
        self,
        key: str,
        value: Union[str, int, float],
        unit: Union[str, None] = None,
        data: list[Union[Data, str]] = None,
    ):
        self.key = key
        self.value = value
        self.unit = unit
        self.data = data if data else []

        self.print_json()

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
        uncertainty: Union[int, float, None] = None,
        reference_material: Union[str, None] = None,
        data: list[Union[Data, str]] = None,
        conditions: list[Union[Condition, dict]] = None,
    ):
        self.key = key
        self.value = value
        self.unit = unit
        self.method = method
        self.uncertainty = uncertainty
        self.reference_material = reference_material
        self.data = data if data else []
        self.conditions = conditions if conditions else []

        self.print_json()

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
        experiments: list = None,
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

        self.print_json()

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

        self.print_json()


class MaterialComponent(Base):
    node_type = "secondary"
    node_name = "MaterialComponent"

    @beartype
    def __init__(self, identity: Union[Identity, str], component_id: int = 0):
        self.component_id = component_id
        self.identity = identity

        self.print_json()


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
        lot_number: Union[str, None] = None,
        keywords: Union[list[str], None] = None,
        notes: Union[str, None] = None,
        experiments: list = None,
        properties: list[Union[Property, dict]] = None,
        conditions: list[Union[Condition, dict]] = None,
        public: bool = False,
        url: Union[str, None] = None,
    ):
        super().__init__()
        self.url = url
        self.group = group
        self.name = name
        self.components = components if components else []
        self.source = source
        self.lot_number = lot_number
        self.keywords = keywords
        self.notes = notes
        self.experiments = experiments if experiments else []
        self.properties = properties if properties else []
        self.conditions = conditions if conditions else []
        self.public = public

        self.print_json()

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

        self.print_json()


class ProductIngredient(Base):
    node_type = "secondary"
    node_name = "ProductIngredient"

    @beartype
    def __init__(
        self,
        procedure_id: int,
        keyword: str,
        quantity: list[Union[Quantity, dict]] = None,
        method: Union[str, None] = None,
    ):
        self.procedure_id = procedure_id
        self.keyword = keyword
        self.quantity = quantity if quantity else []
        self.method = method

        self.print_json()

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
        keyword: str,
        quantity: list[Union[Quantity, dict]] = None,
        method: Union[str, None] = None,
    ):
        self.ingredient = ingredient
        self.keyword = keyword
        self.quantity = quantity if quantity else []
        self.method = method

        self.print_json()

    @beartype
    def add_quantity(self, quantity: Union[Quantity, dict]):
        self._add_node(quantity, "quantity")

    @beartype
    def remove_quantity(self, quantity: Union[Quantity, int]):
        self._remove_node(quantity, "quantity")


class Procedure(Base):
    node_type = "secondary"
    node_name = "Procedure"

    @beartype
    def __init__(
        self,
        procedure_id: int,
        description: Union[str, None] = None,
        product_ingredients: list[Union[ProductIngredient, dict]] = None,
        material_ingredients: list[Union[MaterialIngredient, dict]] = None,
        properties: list[Union[Property, dict]] = None,
        conditions: list[Union[Condition, dict]] = None,
    ):
        self.procedure_id = procedure_id
        self.description = description
        self.product_ingredients = product_ingredients if product_ingredients else []
        self.material_ingredients = material_ingredients if material_ingredients else []
        self.properties = properties if properties else []
        self.conditions = conditions if conditions else []

        self.print_json()

    @beartype
    def add_ingredient(
        self, ingredient: Union[ProductIngredient, MaterialIngredient, dict]
    ):
        if isinstance(ingredient, ProductIngredient):
            self._add_node(ingredient, "product_ingredients")
        elif isinstance(ingredient, MaterialIngredient):
            self._add_node(ingredient, "material_ingredients")

    @beartype
    def remove_ingredient(
        self, ingredient: Union[ProductIngredient, MaterialIngredient, int]
    ):
        if isinstance(ingredient, ProductIngredient):
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
        experiments: list = None,
        procedures: list[Union[Procedure, dict]] = None,
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
        self.procedures = procedures if procedures else []
        self.public = public

        self.print_json()

    def add_experiment(self, experiment):
        self._add_node(experiment, "experiments")

    def remove_experiment(self, experiment):
        self._remove_node(experiment, "experiments")

    @beartype
    def add_procedure(self, procedure: Union[Procedure, dict]):
        self._add_node(procedure, "procedures")

    @beartype
    def remove_procedure(self, procedure: Union[Procedure, int]):
        self._remove_node(procedure, "procedures")


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
        process: Union[Process, str] = None,
        product: Union[Material, str] = None,
        public: bool = False,
        url: Union[str, None] = None,
    ):
        super().__init__()
        self.url = url
        self.group = group
        self.name = name
        self.funding = funding
        self.notes = notes
        self.notes = notes
        self.collection = collection
        self.process = process
        self.product = product
        self.public = public

        self.print_json()
