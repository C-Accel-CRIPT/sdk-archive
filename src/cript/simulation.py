"""
Simulation Node

"""


from .base import BaseModel


class Simulation(BaseModel):
    _class = "Simulation"

    def __init__(
            self,
            name: str,
            notes: str = None):
        super().__init__(name=name, _class=self._class, notes=notes)


