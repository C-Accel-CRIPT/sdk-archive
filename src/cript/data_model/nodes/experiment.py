from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.collection import Collection
from cript.data_model.nodes.group import Group
from cript.data_model.paginator import Paginator
from cript.data_model.utils import auto_assign_group

logger = getLogger(__name__)


class Experiment(BaseNode):
    """The <a href="../experiment" target="_blank">`Experiment`</a> object
    represents a logical grouping of
    <a href="../process" target="_blank">`Process`</a>,
    <a href="../computation" target="_blank">`Computation`</a>,
    <a href="../computational_process" target="_blank">`ComputationalProcess`</a>, and
    <a href="../data" target="_blank">`Data`</a> objects. Each
    <a href="../experiment" target="_blank">`Experiment`</a> is nested inside of a
    <a href="../collection" target="_blank">`Collection`</a> object.

    Args:
        collection (Union[Collection, str]): The experiment's parent `Collection`
        name (str): Experiment name
        processes (str, optional): URL for list of processes inside the experiment
        computations (str, optional): URL for list of computations inside the experiment
        computational_processes (str, optional): URL for list of computational processes inside the experiment
        data (str, optional): _description_. URL for list of data objects inside the experiment
        funding (list[Union[str, None]], optional): List of funding sources for the experiment
        notes (Union[str, None], optional): Experiment notes
        public (bool, optional): Whether the experiment is publicly viewable
        group (Union[Group, str], optional): `Group` object that manages the experiment
    
    !!! warning "Experiment name uniqueness"
        Each <a href="../experiment" target="_blank">`Experiment`</a> name must be unique within a
        <a href="../collection" target="_blank">`Collection`</a> node.     

    !!! success "Experiment methods"
        Since the `Experiment` object inherits from the <a href="../base_node" target="_blank">`BaseNode`</a> object,
        all the <a href="../base_node" target="_blank">`BaseNode`</a> object methods can be used to manipulate an `Experiment`.
        These include `get()`, `create()`, `delete()`, `save()`, `search()`, `update()`, and `refresh()` methods.
        See the <a href="../base_node" target="_blank">`BaseNode`</a> documentation to learn more about these methods.

    ``` py title="Example"
    # get an existing collection
    my_collection = Collection.get(name="My collection")

    # create a new experiment in the existing collection
    my_exp = Experiment.create(
        collection=my_collection,
        name="My experiment name",
    )

    # get another experiment
    my_other_exp = Experiment.get(
        name="My other exp name",
        collection=my_collection,
    )
    ```

    !!! question "Why is `Collection` needed when getting an experiment?"
        <a href="../experiment" target="_blank">`Experiment`</a> names are only unique within a collection, not across all collections,
        so when getting a `Experiment` via name,
        the associated <a href="../collection" target="_blank">`Collection`</a> node must also be specified.


    ``` json title="Example of an experiment in JSON format"
    {
        "url": "https://criptapp.org/api/experiment/e8ab6e1d-fd39-44c3-ac34-4d0a32296327/",
        "uid": "e8ab6e1d-fd39-44c3-ac34-4d0a32296327",
        "group": "https://criptapp.org/api/group/deaa7088-2aac-4f30-a3f6-ad8a4439cafa/",
        "name": "Synthesis of Polymethylmethacrylate via ATRP",
        "funding": ["funding source 1", "funding source 2"],
        "notes": "using amide functionalized initiator",
        "collection": "https://criptapp.org/api/collection/a2cf64b4-5497-4ef4-a5af-521f641ac0fa/",
        "processes": "https://criptapp.org/api/experiment/e8ab6e1d-fd39-44c3-ac34-4d0a32296327/processes/",
        "computational_processes": "https://criptapp.org/api/experiment/e8ab6e1d-fd39-44c3-ac34-4d0a32296327/computational-processes/",
        "computations": "https://criptapp.org/api/experiment/e8ab6e1d-fd39-44c3-ac34-4d0a32296327/computations/",
        "data": "https://criptapp.org/api/experiment/e8ab6e1d-fd39-44c3-ac34-4d0a32296327/data/",
        "public": true,
        "created_at": "2022-05-24T19:14:29.119624Z",
        "updated_at": "2022-05-24T19:14:29.119644Z"
    }
    ```
    """

    node_name = "Experiment"
    slug = "experiment"
    alt_names = ["experiments"]

    @beartype
    def __init__(
        self,
        collection: Union[Collection, str],
        name: str,
        processes: str = None,
        computations: str = None,
        computational_processes: str = None,
        data: str = None,
        funding: list[Union[str, None]] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        group: Union[Group, str] = None,
        **kwargs,
    ):
        # pop materials if it is passed in as extra
        kwargs.pop("materials", None)
        super().__init__(public=public, **kwargs)
        self.collection = collection
        self.name = name
        self.funding = funding if funding else []
        self.processes = processes
        self.computations = computations
        self.computational_processes = computational_processes
        self.data = data
        self.notes = notes
        self.group = auto_assign_group(group, collection)

    @property
    def processes(self):
        return self._processes

    @processes.setter
    def processes(self, value):
        if value:
            self._processes = Paginator(url=value, node_name="Process")

    @property
    def computational_processes(self):
        return self._computational_processes

    @computational_processes.setter
    def computational_processes(self, value):
        if value:
            self._computational_processes = Paginator(
                url=value, node_name="ComputationalProcess"
            )

    @property
    def computations(self):
        return self._computations

    @computations.setter
    def computations(self, value):
        if value:
            self._computations = Paginator(url=value, node_name="Computation")

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if value:
            self._data = Paginator(url=value, node_name="Data")

    def save(self, get_level: int = 0, update_existing: bool = False):
        BaseNode.save(self, get_level=get_level, update_existing=update_existing)
