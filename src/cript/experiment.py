"""
Experiment Node

"""

from .base import BaseModel


class Experiment(BaseModel):

    _class = "experiment"

    def __init__(
        self,
        name: str,
        notes: str = None,
    ):
        """

        :param name: The name of the user.

        :param notes: Any miscellaneous notes related to the user.
        """
        super().__init__(name=name, _class=self._class, notes=notes)


        #materials
        #process
        # sample
        # data