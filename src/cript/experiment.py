"""
Experiment Node

"""

from . import BaseModel, CRIPTError
from .utils.external_database_code import GetMaterial


class ExperimentError(CRIPTError):
    def __init__(self, *msg):
        super().__init__(*msg)


class Experiment(BaseModel, GetMaterial):

    _error = ExperimentError
    _class = "Experiment"

    def __init__(
        self,
        name: str,
        c_material=None,
        c_process=None,
        c_data=None,
        funding: list[str]=None,
        notes: str = None,
        **kwargs
    ):
        """

        :param name: The name of the user.

        :param notes: Any miscellaneous notes related to the user.
        """
        super().__init__(name=name, _class=self._class, notes=notes, **kwargs)

        self._c_material = None
        self.c_material = c_material

        self._c_process = None
        self.c_process = c_process

        self._c_data = None
        self.c_data = c_data

        self._funding = None
        self.funding = funding

    @property
    def c_material(self):
        return self._c_material

    @c_material.setter
    def c_material(self, c_material):
        self._setter_CRIPT_prop(c_material, "c_material")

    @property
    def c_process(self):
        return self._c_process

    @c_process.setter
    def c_process(self, c_process):
        self._setter_CRIPT_prop(c_process, "c_process")

    @property
    def c_data(self):
        return self._c_data

    @c_data.setter
    def c_data(self, c_data):
        self._setter_CRIPT_prop(c_data, "c_data")

    @property
    def funding(self):
        return self._funding

    @funding.setter
    def funding(self, funding):
        self._funding = funding
