"""
Data node

"""

from pathlib import Path

from . import BaseModel, Cond, Prop
from .utils.serializable import Serializable
from .keys.data import *

class File(Serializable):
    def __init__(
            self,
            path: Path,
            descr: str = None,
    ):
        """

        :param path: file path
        :param descr: description

        :param ext: file extension
        """

        self._path = None
        self.path = path

        self._descr = None
        self.descr = descr

        # self._ext = None
        # self.ext = ext


class Data(BaseModel):
    op_keywords = []
    _class = "Data"

    def __init__(
            self,
            name: str,
            _type: list[str],
            source: str,
            file = None,

            notes: str = None
    ):
        super().__init__(name=name, _class=self._class, notes=notes)

