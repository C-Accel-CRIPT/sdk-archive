from os import mkdir
from os.path import join
from json import dump
import time
from pathlib import Path

from .. import CRIPTError, Unit
from ..primary_nodes.base import CriptTypes
from ..validator import id_type_check_bool
from .load import load
from ..mongodb import GetObject, FilesInOut


class Export(CriptTypes):
    """ Export

    Export CRIPT nodes as JSON. I can export a single document, or it can traverse through references and
    download/export multiple files at once.

    """

    _error = CRIPTError

    def __init__(self):
        self.default_path = Path(join(Path.home(), "Downloads"))

    def __call__(self, obj, path: str = None, depth: int = 0, op_files: bool = False, export_limit: int = 100)\
            -> list[Path]:
        """ Export

        Does Export

        Parameters
        ----------
        obj: CRIPT node
            The node you want to export, or starting point of export traversal.
        path: str
            Path were files will be save to. Default is 'Downloads' folder.
        depth: int
            how many references to traverse
            0: export single CRIPT node, obj provided. (default)
            1: follow reference from obj one level
            2+: continue to respectively follow reference 'n' levels deep
                Warning!! increase this number by even +1 exponentially increase the files found. It can get large very
                fast!
                depth=4 from user node gets most of database
        op_files: bool
            True: download raw data files and CRIPT node JSON
            False: only download CRIPT node JSON
        export_limit: int
            Limit of files exported (default=100)
            This is mainly to prevent too many files from be download if too big depth entered.

        Returns
        -------
        paths: list[Path]
            List of all the files exported

        """
        if path is None:
            path = self.default_path

        # make new folder for exported data with time stamp
        time_ = time.strftime("%Y%m%d-%H%M%S")
        folder_path = Path(join(path, f"cript_export_{time_}"))
        mkdir(folder_path)

        if not isinstance(obj, list):
            obj = [obj]

        return_data = []  # data returned by method
        past_uids = set()  # keep track of what has been exported to avoid duplicates.
        export_count = 0
        for level in range(depth+1):
            uids = {}
            for ob in obj:

                # export counter to avoid exporting too many files.
                export_count += 1
                if export_count > export_limit:
                    raise self._error("Export Limit reached.")

                # load given object as CRIPT node
                if isinstance(ob, dict) and "created_date" in ob.keys():
                    ob = load(ob)
                if isinstance(ob, dict) and "class_" in ob.keys():
                    ob = GetObject.get_from_uid(ob["class_"], ob["uid"])[0]
                    ob = load(ob)
                if not hasattr(ob, "create_doc"):
                    mes = "Invalid object for export."
                    raise CRIPTError(mes)

                # save current object as JSON
                file_name = f"{ob.class_}_{ob.uid if ob.uid is not None else ob.created_date}_{ob.name}.txt"
                file_path = Path(join(folder_path, file_name))
                with open(file_path, 'w', encoding='utf-8') as f:
                    dump(ob.dict_remove_none(ob.dict_cleanup(ob.as_dict(save=False))),
                         f, indent=2, ensure_ascii=False, sort_keys=False)

                # save raw data
                if op_files and isinstance(ob, self.cript_types["Data"]):
                    FilesInOut.get_and_save(ob, folder_path)

                # update lists
                return_data.append(file_path)
                past_uids.update(set(ob.uid))

                # get uid that are referenced in document.
                if level < depth:
                    uids = uids | self.get_all_uid(ob)

            # remove already save uids
            uids = {k: v for k, v in uids.items() if k not in past_uids}

            # download from database all new objects to export
            obj = [GetObject.get_from_uid(class_, uid)[0] for uid, class_ in uids.items()]

        return return_data

    def get_all_uid(self, obj) -> dict[str:str]:
        """ Get all uid

        Given a object find all 'uids' and 'class_' so a database search can be done to find the object.
        Recursive function.

        Parameters
        ----------
        obj:
            Object that you want to extract 'uids' and 'class_' from.

        Returns
        -------
        out: dict[uid: class_]
            Both 'uid' and 'class_' are returned so a database search can be preformed.

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
