"""

"""

from abc import ABC
import sys
from difflib import SequenceMatcher
from typing import Union
from warnings import warn

from bson import ObjectId
from fuzzywuzzy import process, fuzz

from .. import CRIPTError, CRIPTWarning


class GetObject(ABC):
    _error = CRIPTError

    @staticmethod
    def _get_from_stack(obj):
        """
        Gets object from Python stack/globals
        Stops at first object it finds

        Example:
        db = self._get_from_stack(cript.CriptDB)
        user = self._get_from_stack(cript.User)

        :param obj:
        :return: returns the object looking for
        """
        for i in range(100):  # 100 is to limit the depth it looks
            frames = sys._getframe(i)
            globals_ = frames.f_globals
            found_obj = [globals_[k] for k, v in globals_.items() if isinstance(v, obj) and k[0] != "_"]
            if found_obj:
                found_obj = found_obj[0]
                break
        else:
            mes = "Database not found in globals, so 'Material.get()' is not working."
            raise Exception

        return found_obj


class GetMaterial(GetObject, ABC):
    """For Experiment and Inventory only."""

    _error = CRIPTError
    _cript_type_db = None
    _cript_database = None

    def get(self, target: str):
        """
        Get material, if exact match found it will be returned otherwise best guess within limit.
        :param target: name of chemical, cas #, Chemical formula
        :return:
        """
        mats = self._get_all_mat()

        if "poly" in target:
            index = self._find_closest_match(target, mats, require="poly")
        else:
            index = self._find_closest_match(target, mats, reject="poly")

        return mats[index]

    def _find_closest_match(self,
                            target: str,
                            mats,
                            require: Union[str, list[str]] = None,
                            reject: Union[str, list[str]] = None,
                            cutoff: int = 75,
                            ) -> int:
        """

        :param target:
        :param mats:
        :param require:
        :param reject:
        :param cutoff: 0-100
        :return: best match index
        """
        scores = []
        for mat in mats:
            values = self._get_set_of_values(mat)
            if require is not None:
                values = self._str_check(values, require, cutoff=0.2, op=True)
            if reject is not None:
                values = self._str_check(values, reject, cutoff=0.5, op=False)
            scores.append(self._get_score(target, values)[1])

        best_match_index = scores.index(max(scores))
        if scores[best_match_index] < cutoff:
            mes = f"'{target}' not found in '{self.name}'."
            raise self._error(mes)
        else:
            if scores[best_match_index] != 100:
                mes = f"Perfect match not found for '{target}', but close match found and used " \
                      f"'{mats[best_match_index]['name']}'."
                warn(mes)

            return best_match_index

    @staticmethod
    def _get_score(target: str, values: set[str], op: int = 5) -> tuple[str, int]:
        """

        :param target:
        :param values:
        :param op:
        :return: scores are from 0 - 100
        """
        if op == 0:
            text, score = process.extractOne(target, values)
        elif op == 1:
            scores = {v: fuzz.ratio(target, v) for v in values}
            text = max(scores, key=scores.get)
            score = scores[text]
        elif op == 2:
            scores = {v: fuzz.partial_ratio(target, v)for v in values}
            text = max(scores, key=scores.get)
            score = scores[text]
        elif op == 3:
            scores = {v: fuzz.token_set_ratio(target, v) for v in values}
            text = max(scores, key=scores.get)
            score = scores[text]
        elif op == 4:
            scores = {v: fuzz.token_sort_ratio(target, v) for v in values}
            text = max(scores, key=scores.get)
            score = scores[text]
        elif op == 5:
            scores = {v: SequenceMatcher(None, target, v).ratio() * 100 for v in values}
            text = max(scores, key=scores.get)
            score = scores[text]
        else:
            mes = "Invalid matching option('op')."
            raise GetMaterial._error(mes)

        return text, score

    @staticmethod
    def _get_set_of_values(mat) -> set[str]:
        """ Returns a set of all idens """
        out = set()
        out.add(mat["name"])
        for iden in mat["iden"].values():
            for v in iden.values():
                if isinstance(v, list):
                    for i in v:
                        out.add(i)
                else:
                    out.add(v)
        return out

    @staticmethod
    def _str_check(values: set[str], require: Union[str, list[str]], cutoff: float = 0.2, op=False) -> set:
        """

        :param values:
        :param require:
        :param cutoff:
        :param op:  True for require, False for reject
        :return:
        """
        removed = 0
        initial_length = len(values)
        if isinstance(require, str):
            require = [require]
        if isinstance(require, list):
            for i in require:
                for x in values:
                    if op:
                        if i not in x:  # requires i to stay in set
                            values.remove(x)
                            removed += 1
                    else:
                        if i in x:  # removes x from set if has i
                            values.remove(x)
                            removed += 1
        else:
            mes = f"Invalid type"
            raise TypeError(mes)

        if len(values)/initial_length > cutoff:
            return values
        else:
            return set()

    def _get_all_mat(self) -> list[dict]:
        if self._cript_type_db is None:
            self._get_cript_type_db()
        if self._cript_database is None:
            self._cript_database = self._get_from_stack(self._get_cript_db)

        database = self._get_from_stack(self._get_cript_db)
        coll = database.db["Material"]
        uids = [ObjectId(mat["uid"]) for mat in self.c_material]
        return list(coll.find({"_id": {"$in": uids}}))

    def _get_one_mat(self, uid) -> dict:
        if self._cript_type_db is None:
            self._get_cript_type_db()
        if self._cript_database is None:
            self._cript_database = self._get_from_stack(self._get_cript_db)

        coll = self._cript_database.db["Material"]
        uid = ObjectId(uid)
        return coll.find_one({"_id": {"$in": uid}})

    def _get_cript_type_db(self):
        try:
            self._get_cript_db = self.cript_types["CriptDB"]
        except Exception:
            from ..import CriptDB
            self._get_cript_db = CriptDB
