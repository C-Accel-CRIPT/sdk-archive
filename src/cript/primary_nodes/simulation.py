"""
Simulation Node

"""


from .base import BaseModel


class Simulation(BaseModel):
    class_ = "Simulation"

    def __init__(
            self,
            name: str,
            notes: str = None,
            **kwargs
    ):
        super().__init__(name=name, class_=self.class_, notes=notes, **kwargs)
