from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.file import File
from cript.data_model.nodes.group import Group
from cript.data_model.nodes.process import Process
from cript.data_model.nodes.experiment import Experiment
from cript.data_model.nodes.computation import Computation
from cript.data_model.nodes.computational_process import ComputationalProcess
from cript.data_model.subobjects.citation import Citation
from cript.data_model.utils import auto_assign_group

logger = getLogger(__name__)


class Data(BaseNode):
    """The <a href="../data" target="_blank">`Data`</a> object represents a
    logical grouping of <a href="../data" target="_blank">`File`</a> objects
    and their related metadata. For example, all the files asociated with
    optical characterization of a given polymer sample may be organized inside
    one <a href="../data" target="_blank">`Data`</a> object. Each
    <a href="../data" target="_blank">`Data`</a> object is nested inside a parent
    <a href="../experiment" target="_blank">`Experiment`</a> object.

    Args:
        experiment (Union[Experiment, str]): Parent `Experiment` object
        name (str): Data name
        type (str): Data type
        files (list[Union[File, str]], optional): List of `File` objects associated with the data
        sample_preparation (Union[Process, str, None], optional): `Process` object which describes sample preparation associated with the data
        computations (list[Union[Computation, str]], optional): List of `Computations` associated with the data
        computational_process (Union[ComputationalProcess, str, None], optional): `ComputationalProcess` object associated with the data
        materials (_type_, optional): List of `Material` objects associated with the data
        processes (_type_, optional): List of `Process` objects associated with the data
        notes (Union[str, None], optional): Data notes
        citations (list[Union[Citation, dict]], optional): List of `Citation` objects associated with the data
        public (bool, optional): Whether the data is publicly viewable
        group (Union[Group, str], optional): `Group` object which manages the data

    !!! warning "Data names must be unique"
        Each <a href="../data" target="_blank">`Data`</a> name must be unique within a given
        <a href="../experiment" target="_blank">`Experiment`</a> node.

    !!! success "Use <a href='../base_node' target='_blank'>`BaseNode`</a> methods to manipulate this object"
        Since this object inherits from the <a href="../base_node" target="_blank">`BaseNode`</a> object,
        all the <a href="../base_node" target="_blank">`BaseNode`</a> object methods can be used to manipulate it.
        These include `get()`, `create()`, `delete()`, `save()`, `search()`, `update()`, and `refresh()` methods.
        See the <a href="../base_node" target="_blank">`BaseNode`</a> documentation to learn more about these methods
        and see examples of their use.

    !!! note "Allowed `Data` types"
        The allowed `Data` types are listed in the
        <a href="https://criptapp.org/keys/data-type/" target="_blank">CRIPT controlled vocabulary</a>

    ``` py title="Example"
    # get an existing experiment
    my_experiment = Experiment.get(name="My experiment")

    # create a new data object in the existing experiment
    data = Data.create(
        experiment=my_experiment,
        name="My data",
        type="afm_amp",
        notes="AFM amplitude data measured in lab 210B",
        files=[file1, file2],
    )
    ```

    ``` json title="Example of a data object in JSON format"
    {
        "url": "https://criptapp.org/api/data/2180f4b8-77b1-418d-94e8-6cf49474eba5/",
        "uid": "2180f4b8-77b1-418d-94e8-6cf49474eba5",
        "experiment": "https://criptapp.org/api/experiment/d0441a13-ad6e-4e1d-9548-b4a4f86f508c/",
        "name": "expt_9_p4_torque_curve",
        "files": [
            "https://criptapp.org/api/file/6aca41248214-defe4902-a263-416f-96fc/",
            "https://criptapp.org/api/file/a263-416f-defe4902-96fc-6aca41248214/",
            "https://criptapp.org/api/file/defe4902-416f-6aca-41248-21496fca263/"
        ],
        "type": "rxn_conv",
        "sample_preparation": null,
        "computational_process": null,
        "computations": [],
        "citations": [],
        "notes": "My data notes",
        "public": true,
        "created_at": "2022-04-28T00:21:34.390165Z",
        "updated_at": "2022-05-04T20:09:59.512137Z",
        "group": "https://criptapp.org/api/group/fd3431b4-8011-4746-92c7-e8713a249c0c/"
    }
    """

    node_name = "Data"
    slug = "data"
    alt_names = ["data"]

    @beartype
    def __init__(
        self,
        experiment: Union[Experiment, str],
        name: str,
        type: str,
        files: list[Union[File, str]] = None,
        sample_preparation: Union[Process, str, None] = None,
        computations: list[Union[Computation, str]] = None,
        computational_process: Union[ComputationalProcess, str, None] = None,
        materials=None,
        processes=None,
        notes: Union[str, None] = None,
        citations: list[Union[Citation, dict]] = None,
        public: bool = False,
        group: Union[Group, str] = None,
        **kwargs,
    ):
        super().__init__(public=public, **kwargs)
        self.experiment = experiment
        self.name = name
        self.files = files if files else []
        self.type = type
        self.sample_preparation = sample_preparation
        self.computations = computations if computations else []
        self.computational_process = computational_process
        self.materials = materials if materials else []
        self.processes = processes if processes else []
        self.citations = citations if citations else []
        self.notes = notes
        self.group = auto_assign_group(group, experiment)

    def save(self, get_level: int = 0, update_existing: bool = False):
        BaseNode.save(self=self, get_level=get_level, update_existing=update_existing)

    @beartype
    def add_file(self, file: Union[File, dict]):
        """Add a <a href="../file" target="_blank">`File`</a> object.

        Args:
            file (Union[File, dict]): `File` object to add

        ``` py title="Example"
        my_data.add_file(my_file)
        ```
        """
        self._add_node(file, "files")

    @beartype
    def remove_file(self, file: Union[File, int]):
        """Remove a <a href="../file" target="_blank">`File`</a> object.

        Args:
            file (Union[File, int]): `File` object to remove

        ``` py title="Example"
        my_data.remove_file(my_file)
        ```
        """
        self._remove_node(file, "files")

    @beartype
    def add_computation(self, computation: Union[BaseNode, dict]):
        """Add a <a href="../computation" target="_blank">`Computation`</a> object.

        Args:
            computation (Union[Computation, dict]): `Computation` object to add

        ``` py title="Example"
        my_data.add_computation(my_computation)
        ```
        """
        self._add_node(computation, "computations")

    @beartype
    def remove_computation(self, computation: Union[BaseNode, int]):
        """Remove a <a href="../computation" target="_blank">`Computation`</a> object.

        Args:
            computation (Union[Computation, dict]): `Computation` object to remove

        ``` py title="Example"
        my_data.remove_computation(my_computation)
        ```
        """
        self._remove_node(computation, "computations")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        """Add a <a href="/../subobjects/citation" target="_blank">`Citation`</a> object.

        Args:
            citation (Union[Citation, dict]): `Citation` to add

        ``` py title="Example"
        data.add_citation(citation)
        ```
        """
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        """Remove a <a href="/../subobjects/citation" target="_blank">`Citation`</a> object.

        Args:
            citation (Union[Citation, int]): `Citation` to remove

        ``` py title="Example"
        data.remove_citation(citation)
        ```
        """
        self._remove_node(citation, "citations")
