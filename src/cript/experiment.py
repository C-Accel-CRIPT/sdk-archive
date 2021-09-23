"""
Experiment Node

"""

from . import CRIPTError
from .base import BaseModel, BaseSlot
from .utils.external_database_code import GetMaterial
from .utils.class_tools import freeze_class


class ExperimentError(CRIPTError):
    pass


@freeze_class
class Experiment(BaseModel, _error=ExperimentError):
    class_ = "Experiment"

    def __init__(
        self,
        name: str,
        c_material=None,
        c_process=None,
        c_data=None,
        funding=None,
        notes: str = None,
        **kwargs
    ):
        """

        :param name: The name of the user.

        :param notes: Any miscellaneous notes related to the user.
        """
        super().__init__(name=name, class_=self.class_, notes=notes, **kwargs)

        self._funding = None
        self.funding = funding

        self._c_material = BaseSlot("Material", c_material, self._error)
        self._c_process = BaseSlot("Process", c_process, self._error)
        self._c_data = BaseSlot("Data", c_data, self._error)

    @property
    def funding(self):
        return self._funding

    @funding.setter
    def funding(self, funding):
        self._funding = funding

    @property
    def c_material(self):
        return self._c_material

    @c_material.setter
    def c_material(self, *args):
        self._base_slot_block()

    @property
    def c_process(self):
        return self._c_process

    @c_process.setter
    def c_process(self, *args):
        self._base_slot_block()

    @property
    def c_data(self):
        return self._c_data

    @c_data.setter
    def c_data(self, *args):
        self._base_slot_block()

    def get(self, target):
        """ Given a target (chemical name, cas number or some other identity find material."""
        return GetMaterial.get(target, self.c_material())
