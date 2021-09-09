"""
Tools for loading and exporting mongodb documents
"""
from os import mkdir
from os.path import join
from json import dump
import time

from . import CRIPTError, Path, Unit
from .base import CriptTypes
from .utils.external_database_code import GetObject, FilesInOut
from .utils.validator.type_check import id_type_check_bool


class Load(CriptTypes):
    """Given a document directly from the database convert it into a CRIPT object."""

    def __call__(self, ddict: dict):
        if "_id" in ddict.keys():
            ddict["uid"] = str(ddict.pop("_id"))
        class_ = ddict.pop("class_")
        obj = self.cript_types[class_](**ddict)
        return obj


load = Load()


def loading_with_units(obj, type_):
    if isinstance(obj, list):
        for i, s in enumerate(obj):
            if isinstance(s, dict):
                obj[i] = type_(**s, _loading=True)
    elif isinstance(obj, type_):
        obj = [obj]

    return obj


class Export(CriptTypes):
    _error = CRIPTError
    """
    Given a document or node export it to txt file.
    """
    def __init__(self):
        self.default_path = Path(join(Path.home(), "Downloads"))

    def __call__(self, obj, path=None, depth: int = 0, op_files: bool = True) -> list[Path]:
        """
        depth=4 from user get most of database
        """
        if path is None:
            path = self.default_path

        time_ = time.strftime("%Y%m%d-%H%M%S")
        folder_path = Path(join(path, f"cript_export_{time_}"))
        mkdir(folder_path)

        if not isinstance(obj, list):
            obj = [obj]

        return_data = []
        past_uids = set()
        for level in range(depth+1):
            uids = {}
            for ob in obj:
                if isinstance(ob, dict) and "class_" in ob.keys():
                    ob = load(ob)
                if not hasattr(ob, "create_doc"):
                    mes = "Invalid object for export."
                    raise CRIPTError(mes)

                file_name = f"{ob.class_}_{ob.uid if ob.uid is not None else ob.created_date}_{ob.name}.txt"
                file_path = Path(join(folder_path, file_name))
                with open(file_path, 'w', encoding='utf-8') as f:
                    dump(ob.dict_remove_none(ob.dict_cleanup(ob.as_dict(save=False))),
                         f, indent=2, ensure_ascii=False, sort_keys=False)

                if op_files and isinstance(ob, self.cript_types["Data"]):
                    FilesInOut.get_and_save(ob, folder_path)

                return_data.append(file_path)
                past_uids.update(set(ob.uid))

                if level < depth:
                    uids = uids | self.get_all_uid(ob)

            uids = {k: v for k, v in uids.items() if k not in past_uids}  # remove already save uids
            obj = [GetObject.get_from_uid(class_, uid)[0] for uid, class_ in uids.items()]

        return return_data

    def get_all_uid(self, obj) -> dict[str:str]:
        """
        Gets uids recursively.
        :param obj:
        :return: dict[uid: class_]
        """
        out = {}

        if isinstance(obj, tuple(self.cript_types.values())):
            if isinstance(obj, self.cript_types["BaseReference"]):
                for i in obj:
                    out[i["uid"]] = i["class_"]
            else:
                keys = {k.lstrip("_") for k in vars(obj) if "__" not in k}
                for k in keys:
                    if isinstance(obj, Unit):
                        pass
                    else:
                        out.update(self.get_all_uid(obj.__getattribute__(k)))

        elif isinstance(obj, list):
            for i in obj:
                out.update(self.get_all_uid(i))

        elif isinstance(obj, dict):
            for k in obj.keys():
                if k == "uid":
                    if id_type_check_bool(obj["uid"]):
                        out[obj["uid"]] = obj["class_"]
                else:
                    out.update(self.get_all_uid(obj[k]))

        else:  # None, int, str
            pass

        return out


export = Export()
