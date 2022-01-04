"""
Experiment Node

"""

from .. import CRIPTError
from ..utils import freeze_class, GetMaterial
from ..validator import type_check
from .base import BaseModel, ReferenceList


class ExperimentError(CRIPTError):
    """ Errors from the Experiment Node

    """
    pass


@freeze_class
class Experiment(BaseModel, _error=ExperimentError):
    """ Experiment Node

    Grouping of all associated material, process, simulation, data nodes

    Attributes
    ----------
    base_attributes:
        See CRIPT BaseModel
    c_material: Material node
        CRIPT Materials used in this experiment
    c_process: Process node
        CRIPT Process nodes associated with this experiment
    c_simulation: Simulation node
        CRIPT Simulation node associated with this experiment
    c_data: Data node
        CRIPT Data nodes associated with this experiment
    funding: str
        Funding source for experiment

    """

    class_ = "Experiment"

    def __init__(
        self,
        name: str,
        c_material=None,
        c_process=None,
        c_simulation=None,
        c_data=None,
        funding: str = None,
        notes: str = None,
        **kwargs
    ):
        super().__init__(name=name, class_=self.class_, notes=notes, **kwargs)

        self._funding = None
        self.funding = funding

        self._c_material = ReferenceList("Material", c_material, self._error)
        self._c_process = ReferenceList("Process", c_process, self._error)
        self._c_simulation = ReferenceList("Simulation", c_simulation, self._error)
        self._c_data = ReferenceList("Data", c_data, self._error)

    @property
    def funding(self):
        return self._funding

    @funding.setter
    @type_check(str)
    def funding(self, funding):
        self._funding = funding

    @property
    def c_material(self):
        return self._c_material

    @c_material.setter
    def c_material(self, *args):
        self._base_reference_block()

    @property
    def c_process(self):
        return self._c_process

    @c_process.setter
    def c_process(self, *args):
        self._base_reference_block()

    @property
    def c_simulation(self):
        return self._c_simulation

    @c_simulation.setter
    def c_simulation(self, *args):
        self._base_reference_block()

    @property
    def c_data(self):
        return self._c_data

    @c_data.setter
    def c_data(self, *args):
        self._base_reference_block()

    def get(self, target):
        """ Given a target (chemical name, cas number or some other identity) find material node."""
        return GetMaterial.get(target, self.c_material())
