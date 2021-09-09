"""

"""
from os.path import join
from abc import ABC
import sys
from difflib import SequenceMatcher
from typing import Union
from warnings import warn

from gridfs import GridFS
from bson import ObjectId
from fuzzywuzzy import process, fuzz

from .. import CRIPTError, Path


class GetObject(ABC):
    _error = CRIPTError
    _cript_database = None
    _cript_type_db = None

    @classmethod
    def get_from_uid(cls, node: str, uid: Union[str, list[str], ObjectId, list[ObjectId]]) -> list[dict]:
        """
        Gets documents from database.
        :param node: Used to find collection on mongodb
        :param uid: document ids you want to find
        :return:
        """
        cls._get_database()
        coll = cls._cript_database.db[node]
        if isinstance(uid, str):
            uid = [ObjectId(uid)]
        elif isinstance(uid, list):
            uid = [ObjectId(u) for u in uid]

        obj = list(coll.find({"_id": {"$in": uid}}))
        if obj is not []:
            return obj
        else:
            mes = f"uid: {uid} not found in database (collection: {node})."
            raise cls._error(mes)

    @classmethod
    def _get_database(cls):
        """
        Checks if database has been grabbed from stack, if not it gets it
        """
        if cls._cript_type_db is None:
            cls._get_cript_type_db()
        if cls._cript_database is None:
            cls._cript_database = cls._get_from_stack(cls._cript_type_db)

    @classmethod
    def _get_cript_type_db(cls):
        from .. import CriptDB
        cls._cript_type_db = CriptDB

    @staticmethod
    def _get_from_stack(obj):
        """
        Gets object from Python stack/globals
        Stops at first object it finds

        Example:
        db = cls._get_from_stack(cript.CriptDB)
        user = cls._get_from_stack(cript.User)

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
            mes = f"{obj} not found in globals, so '.get()' is not working."
            raise Exception(mes)

        return found_obj


class GetMaterial(GetObject, ABC):
    """For Experiment and Inventory only."""

    @classmethod
    def get(cls, target: str, materials: list[dict]) -> dict:
        """
        Get material, if exact match found it will be returned otherwise best guess within limit.
        :param target: name of chemical, cas #, Chemical formula
        :param materials: c_material
        :return:
        """
        mats = cls._get_all_mat(materials)

        if "poly" in target:
            index = cls._find_closest_match(target, mats, require="poly")
        else:
            index = cls._find_closest_match(target, mats, reject="poly")

        return mats[index]

    @classmethod
    def _find_closest_match(cls,
                            target: str,
                            mats: list[dict],
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
            values = cls._get_set_of_values(mat)
            if require is not None:
                values = cls._str_check(values, require, cutoff=0.2, op=True)
            if reject is not None:
                values = cls._str_check(values, reject, cutoff=0.5, op=False)
            scores.append(cls._get_score(target, values)[1])

        best_match_index = scores.index(max(scores))
        if scores[best_match_index] < cutoff:
            mes = f"'{target}' not found."
            raise cls._error(mes)
        else:
            if scores[best_match_index] != 100:
                mes = f"Perfect match not found for '{target}', but close match found: " \
                      f"'{mats[best_match_index]['name']}' and used."
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
        if len(values) == 0:
            return "", 0

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

    @classmethod
    def _get_set_of_values(cls, mat: dict) -> set[str]:
        """ Returns a set of all idens """
        out = set()
        out.add(mat["name"])
        for iden in mat["iden"].values():
            out.update(cls._get_set_of_values_from_iden(iden))
        return out

    @staticmethod
    def _get_set_of_values_from_iden(iden: dict) -> set[str]:
        out = set()
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
        initial_length = len(values)
        if isinstance(require, str):
            require = [require]
        if isinstance(require, list):
            for i in require:
                remove = []
                for x in values:
                    if op:
                        if i not in x:  # requires i to stay in set
                            remove.append(x)
                    else:
                        if i in x:  # removes x from set if has i
                            remove.append(x)

                for ii in remove:
                    values.remove(ii)

        else:
            mes = f"Invalid type"
            raise TypeError(mes)

        if len(values)/initial_length > cutoff:
            return values
        else:
            return set()

    @classmethod
    def _get_all_mat(cls, materials) -> list[dict]:
        uids = [mat["uid"] for mat in materials]
        return cls.get_from_uid("Material", uids)

    @classmethod
    def _get_one_mat(cls, uid) -> dict:
        return cls.get_from_uid("Material", uid)[0]


class GetMaterialID(GetMaterial):
    """For Material."""

    @classmethod
    def get_id(cls, target, material):
        scores = []
        for _id, mat_ref in material.iden.items():
            mat = cls._get_one_mat(mat_ref["uid"])
            values = cls._get_set_of_values(mat)
            r = cls._get_score(target, values)[1]
            if r > 95:
                return _id
            else:
                scores.append([_id, r])

        if max_ := max([i[1] for i in scores]) > 0.75:
            return [i[0] for i in scores if i[1] == max_][0]
        else:
            mes = f"'{target}' not found or wasn't close enough to material name."
            raise cls._error(mes)


class FilesInOut(GetObject):
    _file_storage = None
    _cript_type_file = None

    @classmethod
    def put(cls, obj):
        """obj is Data node, will save to database and put uid for file in object."""
        cls._get_file_storage()

        keys_of_files = [k.lstrip("_") for k, v in vars(obj).items() if isinstance(v, cls._cript_type_file)]
        for key in keys_of_files:
            file = obj.__getattribute__(key)
            if file.uid is None:
                with open(file.path, 'rb') as f:
                    contents = f.read()
                file.uid = cls._file_storage.put(contents)
                file.path = None  # clear path - we don't need users personal file path
            else:
                mes = "update file not setup yet"
                raise cls._error(mes)

        return obj

    @classmethod
    def get(cls, obj):
        """
        Obj is Data node, return [[file_name.ext, file],...]
        """
        cls._get_file_storage()

        files = []
        ref_files = [v for v in vars(obj).values() if isinstance(v, cls._cript_type_file)]
        for ref in ref_files:
            if ref.uid is not None:
                files.append([Path(ref.file_name + ref.ext), cls._file_storage.get(ref.uid)])

        return files

    @classmethod
    def get_and_save(cls, obj, folder_path):
        files = cls.get(obj)
        for file in files:
            file_path = Path(join(folder_path, file[0]))
            with open(file_path, 'wb') as f:
                f.write(file[1].read())

    @classmethod
    def _get_file_storage(cls):
        """
        Checks for database and file storage
        """
        cls._get_database()
        if cls._file_storage is None:
            cls._file_storage = GridFS(cls._cript_database.db)
        if cls._cript_type_file is None:
            cls._get_cript_type_file()

    @classmethod
    def _get_cript_type_file(cls):
        from .. import File
        cls._cript_type_file = File
