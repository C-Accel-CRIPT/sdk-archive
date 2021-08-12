"""
Experiment Node

"""

import sys
from difflib import SequenceMatcher

from bson import ObjectId

from . import BaseModel, CRIPTError
import cript as C


class Experiment(BaseModel):

    _class = "Experiment"

    def __init__(
        self,
        name: str,
        c_material=None,
        c_process=None,
        c_data=None,
        notes: str = None,
    ):
        """

        :param name: The name of the user.

        :param notes: Any miscellaneous notes related to the user.
        """
        super().__init__(name=name, _class=self._class, notes=notes)

        self._c_material = None
        self.c_material = c_material

        self._c_process = None
        self.c_process = c_process

        self._c_data = None
        self.c_data = c_data

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

    def get(self, str_):
        mats = self._get_all_mat()
        if "poly" in str_:
            scores = []
            for mat in mats:
                best_match = 0
                for iden in mat["iden"].values():
                    for v in iden.values():
                        if isinstance(v, list):
                            for i in v:
                                if "poly" in v:
                                    best_match = max([best_match, SequenceMatcher(None, str_, v).ratio()])
                        else:
                            if "poly" in v:
                                best_match = max([best_match, SequenceMatcher(None, str_, v).ratio()])
                scores.append(best_match)
        else:
            scores = []
            for mat in mats:
                best_match = 0
                for iden in mat["iden"].values():
                    for v in iden.values():
                        if isinstance(v, list):
                            for i in v:
                                if "poly" not in v:
                                    best_match = max([best_match, SequenceMatcher(None, str_, v).ratio()])
                        else:
                            if "poly" not in v:
                                best_match = max([best_match, SequenceMatcher(None, str_, v).ratio()])
                scores.append(best_match)

        best_match_index = scores.index(max(scores))
        return mats[best_match_index]

    def _get_all_mat(self) -> list[dict]:
        try:  # Try to find a user node in the Python stack/globals
            for i in range(100):
                frames = sys._getframe(i)
                globals_ = frames.f_globals
                database = [globals_[k] for k, v in globals_.items() if isinstance(v, C.CriptDB) and k[0] != "_"]
                if database:
                    database = database[0]
                    break
            else:
                raise Exception
            coll = database.db["Material"]
            uids = [ObjectId(mat["uid"]) for mat in self.c_material]
            return list(coll.find({"_id" : {"$in" : uids}}))

        except Exception:
            mes = "Database not found in globals, so 'Material.get()' is not working."
            raise CRIPTError(mes)
