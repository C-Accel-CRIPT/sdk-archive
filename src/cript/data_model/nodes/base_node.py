import abc
import copy
import json
from logging import getLogger
from typing import Union

from beartype import beartype

from cript.cache import cache_node, get_cached_api_session, get_cached_node
from cript.data_model.base import Base
from cript.data_model.exceptions import (
    AddNodeError,
    RemoveNodeError,
    UniqueNodeError,
    UnsavedNodeError,
)
from cript.data_model.paginator import Paginator
from cript.data_model.utils import create_node, set_node_attributes

logger = getLogger(__name__)


class BaseNode(Base, abc.ABC):
    """This is the base node that all other CRIPT primary nodes
    inherit from. The <a href="../base_node" target="_blank">`BaseNode`</a>
    is not called in the SDK directly, but its methods can be used from any of the
    other primary CRIPT nodes, including
    <a href="../collection" target="_blank">`Collection`</a>,
    <a href="../computation" target="_blank">`Computation`</a>,
    <a href="../computational_process" target="_blank">`ComputationalProcess`</a>,
    <a href="../data" target="_blank">`Data`</a>,
    <a href="../experiment" target="_blank">`Experiment`</a>,
    <a href="../file" target="_blank">`File`</a>,
    <a href="../group" target="_blank">`Group`</a>,
    <a href="../inventory" target="_blank">`Inventory`</a>,
    <a href="../material" target="_blank">`Material`</a>,
    <a href="../process" target="_blank">`Process`</a>,
    <a href="../project" target="_blank">`Project`</a>,
    <a href="../reference" target="_blank">`Reference`</a>, and
    <a href="../software" target="_blank">`Software`</a>.

    Args:
        url (str, optional): URL of the node
        uid (str, optional): UID of the node
        public (bool, optional): Whether the node is publicly viewable
        created_at (str, optional): Time at which the node was created
        updated_at (str, optional): Time at which the node was last updated
        can_edit (bool, optional): Whether the current user has permission to edit the node

    !!! warning "BaseNode Instantiation"
        Do not interact directly with the <a href="../base_node" target="_blank">`BaseNode`</a>.
        Instead, call its methods from other primary nodes. For example, instead of using
        `BaseNode().create()`, use the create method on a project,
        like this: `Project.create(name="My project")`.
    """

    slug = None

    def __init__(
        self,
        url: str = None,
        uid: str = None,
        public: bool = False,
        created_at: str = None,
        updated_at: str = None,
        can_edit: bool = False,
    ):
        super().__init__()
        self.url = url
        self.uid = uid
        self.public = public
        self.created_at = created_at
        self.updated_at = updated_at
        self.can_edit = can_edit

        # Add node to cache
        cache_node(self)

    @beartype
    def save(self, get_level: int = 1, update_existing: bool = False):
        """Create or update a node in the database.

        Args:
            get_level (int, optional): Level to recursively get nested nodes
            update_existing (bool, optional): Whether to update an existing node with the same unique fields

        Raises:
            UniqueNodeError: Arises when the node cannot be created because it is not unique

        ``` py title="Example"
        my_node = Project(
            name="My new project",
            notes="Project created using the Python SDK",
        )
        my_node.save()
        ```
        """

        api = get_cached_api_session(self.url)

        if self.url:
            # Update an existing object via PUT
            response = api.put(self.url, data=self._to_json(), valid_codes=[200, 400])
        else:
            # Create a new object via POST
            response = api.post(
                url=f"{api.url}/{self.slug}/",
                data=self._to_json(),
                valid_codes=[201, 400],
            )

            # Check if a unique error was returned
            if "unique" in response:
                unique_url = response.pop("unique")
                if unique_url and update_existing:
                    # Update existing unique node
                    self.url = unique_url
                    self.save(get_level=get_level)
                    return
                else:
                    raise UniqueNodeError(response["errors"][0])

        set_node_attributes(self, response)
        self._generate_nested_nodes(get_level=get_level)
        logger.info(f"{self.node_name} node has been saved to the database.")

    @beartype
    def delete(self):
        """Delete a node in the database and clear it locally."

        Raises:
            ValueError: The node does not exist in the database

        ``` py title="Example"
        my_project = Project.get(name="My project")
        my_project.delete()
        ```
        """
        if not self.url:
            raise ValueError(
                f"This {self.node_name} node does not exist in the database."
            )
        api = get_cached_api_session(self.url)
        api.delete(self.url)
        self.url = None
        self.uid = None
        self.created_at = None
        self.updated_at = None
        logger.info("The node has been deleted from the database.")

    @beartype
    def refresh(self, get_level: int = 1):
        """Overwrite a node's attributes with the latest values from the database.

        Args:
            get_level (int, optional): Level to recursively get nested nodes.

        Raises:
            ValueError: The node hasn't been saved to the database yet (it has no URL)

        ``` py title="Example"
        my_project = Project.get(name="My project")
        my_project.name = "New name"
        my_project.refresh()

        ```
        """
        if self.url is None:
            raise ValueError(
                "Before you can refresh a node, you must either save it or define its URL."
            )
        api = get_cached_api_session(self.url)
        response = api.get(self.url)
        set_node_attributes(self, response)
        self._generate_nested_nodes(get_level=get_level)

    @beartype
    def update(self, get_level: int = 1, **kwargs):
        """Updates and saves changes to a node.

        Args:
            get_level (int, optional): Level to recursively get nested nodes
            **kwargs (dict): Node attributes

        Raises:
            ValueError: The node hasn't been saved to the database yet (it has no URL)

        ``` py title="Example"
        # update project name
        proj = Project.get(name="My project")
        proj.update(name="My project with new name")

        # update project notes
        proj.update(notes="new notes")

        # update inventory to change its materials
        inventory = Inventory.get(name="My inventory")
        new_material_list = [material1, material2, material3]
        inventory.update(materials=new_material_list)
        ```
        """
        if self.url is None:
            raise ValueError(
                "Before you can update a node, you must either save it or define its URL."
            )

        set_node_attributes(self, kwargs)
        self.save(get_level=get_level)

    @classmethod
    @beartype
    def create(cls, get_level: int = 1, update_existing: bool = False, **kwargs):
        """Creates a node and saves it to the CRIPT database.

        Args:
            get_level (int, optional): Level to recursively get nested nodes
            update_existing (bool, optional): Whether to update an existing node with the same unique fields
            **kwargs (dict): Node attributes

        Returns:
            node (cript.data_model.nodes.BaseNode): _description_

        ``` py title="Example"
        import cript

        # create a project
        my_project = cript.Project.create(
            name="My project",
            notes="Project created from the Python SDK",
        )

        # create a collection
        my_collection = cript.Collection.create(
            name="My collection",
            project=my_project,
            notes="A new collection created from the Python SDK",
        )

        # create an experiment
        my_experiment = cript.Experiment.create(
            name="My experiment",
            collection=my_collection,
            notes="A new experiment created from the Python SDK",
        )
        ```
        """
        node = cls(**kwargs)
        node.save(get_level=get_level, update_existing=update_existing)
        return node

    @classmethod
    @beartype
    def get(cls, get_level: int = 1, **kwargs):
        """Get the JSON for a node and use it to generate a local node object.

        Args:
            get_level (int, optional): Level to recursively get nested nodes
            **kwargs (dict): Query parameters

        Raises:
            AttributeError: No query arguments were provided
            ValueError: No matches were found, or more than one match was found

        Returns:
            result (dict): The matching node object

        ``` py title="Example"
        # get a collection by name
        collection = Collection.get(name="My collection")

        # get a project by UID
        project = Project.get(uid="fa12b444-4931-427d-8f6e-475604e8404c")

        # get a material by URL
        url = "https://criptapp.org/material/015fc459-ea9f-4c37-80aa-f51d509095df/"
        material = styrene = cript.Material.get(url=url)
        ```
        """
        level = kwargs.pop("level", 0)

        if len(kwargs) == 0:
            raise AttributeError("Query arguments must be provided.")

        api = get_cached_api_session()

        if "url" in kwargs:
            obj_json = api.get(kwargs["url"])
        else:
            results = cls.search(**kwargs)
            count = results.count()
            if count < 1:
                raise ValueError("Your query did not match any existing nodes.")
            elif count > 1:
                raise ValueError("Your query matched more than one node.")
            else:
                obj_json = results.json()[0]

        # Return the local node object if it already exists
        # Otherwise, create a new node
        if "url" in obj_json:
            local_node = get_cached_node(obj_json["url"])

            if local_node:
                return local_node

        node = create_node(cls, obj_json)
        node._generate_nested_nodes(get_level=get_level, level=level)
        return node

    @classmethod
    @beartype
    def search(
        cls,
        limit: Union[int, None] = None,
        offset: Union[int, None] = None,
        get_level: int = 1,
        **kwargs,
    ):
        """Send a query to the API and display the results.

        Args:
            limit (Union[int, None], optional):  The maximum number of results to return
            offset (Union[int, None], optional): The starting position of the query
            get_level (int, optional): Level to recursively get nested nodes
            **kwargs (dict): Query parameters

        Raises:
            AttributeError: No query arguments were provided

        Returns:
            results (cript.data_model.paginator.Paginator): The paginated results

        ``` py title="Examples"
        # search for inventory with the name "My Inventory"
        results Inventory.search(name="My Inventory")

        # searches for collections inside "My project"
        results = Collection.search(project="My project")

        # search for materials with molar mass < 10 g/mol
        results =  cript.Material.search(
            properties = [
                {
                    "key": "molar_mass",
                    "value__lt": 10,
                    "unit": "g/mol"
                }
            ]
        )
        ```
        """
        if len(kwargs) == 0:
            raise AttributeError("Query arguments must be provided.")

        api = get_cached_api_session()
        url = f"{api.search_url}/{cls.slug}/"
        payload = json.dumps(kwargs)
        return Paginator(
            url=url,
            node_name=cls.node_name,
            limit=limit,
            offset=offset,
            get_level=get_level,
            payload=payload,
        )

    def _to_json(self):
        node_dict = copy.deepcopy(self._clean_dict())

        for key, value in node_dict.items():
            if isinstance(value, Paginator):
                node_dict[key] = value.url
            elif hasattr(value, "_prep_for_upload"):
                node_dict[key] = value._prep_for_upload()
            elif isinstance(value, list):
                for i in range(len(value)):
                    if hasattr(value[i], "_prep_for_upload"):
                        value[i] = value[i]._prep_for_upload()

        return json.dumps(node_dict, indent=4)

    def _prep_for_upload(self, first: bool = False):
        """
        Convert a node into a dict that can be sent to the API.

        :return: The converted dict.
        :rtype: dict
        """
        # Check if node has been saved
        if self.url is None:
            raise UnsavedNodeError(self.node_name)
        return self.url

    def _add_node(self, node: Base, attr_name: str):
        """
        Append a node to another node's list attribute.

        :param node: The node that will be appended.
        :param attr_name: The name of the list attribute (e.g., conditions).
        """
        if isinstance(node, BaseNode) and node.url is None:
            raise UnsavedNodeError(node.node_name)

        if hasattr(self, attr_name):
            getattr(self, attr_name).append(node)
        else:
            raise AddNodeError(node.node_name, self.node_name)

    def _remove_node(self, node: Base, attr: str):
        """
        Remove a node from another node's list attribute.

        :param node: The node that will be removed or it's position in the list.
        :param attr: The name of the list attribute (e.g., conditions).
        """
        if not hasattr(self, attr):
            raise RemoveNodeError(f"The node does not have attribute: {attr}")

        attribute = getattr(self, attr)

        if isinstance(node, int) and 0 < node <= len(attribute):
            attribute.pop(node)
        elif isinstance(node, BaseNode):
            if isinstance(attribute[0], str):
                # node attributes may be list[URL]
                attribute.remove(node.url)
            else:
                # node attributes may be list[BaseNode]
                attribute.remove(node)
        elif isinstance(node, Base):
            # for BaseSubobject
            attribute.remove(node)
        else:
            raise RemoveNodeError(
                f"{self.node_name} nodes do not contain {node.node_name} nodes."
            )
