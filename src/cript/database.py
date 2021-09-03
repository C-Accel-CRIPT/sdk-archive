"""
Database Connection

"""
import sys
from datetime import datetime
from typing import Union

from pymongo import MongoClient, errors
from bson import ObjectId
from jsonpatch import JsonPatch
from gridfs import GridFS

from cript.utils.validator.type_check import *
from .utils.database_tools import *
from . import load, CRIPTError, User, File


class CriptDBError(CRIPTError):
    def __init__(self, *msg):
        super().__init__(*msg)


class CriptDB:
    cript_types = None
    instances = 0
    user_update = 0
    _error = CriptDBError

    def __init__(self,
                 db_username: str,
                 db_password: str,
                 db_project: str,
                 db_database: str,
                 user: Union[str, User] = None,
                 op_print: bool = True):
        """
        This class handles all communication with MongoDB.
        :param db_username: mongoDB username
        :param db_password: mongoDB password
        :param db_project: mongoDB project
        :param db_database: name of database on mongoDB
        :param user: user node
        :param op_print: True to get printouts from database commands
        """

        if CriptDB.instances > 0:
            raise Exception("Connection to CRIPT database already exists. Can't start a second one.")
        CriptDB.instances += 1

        self.db_username = db_username
        self.db_password = db_password
        self.db_project = db_project
        self.db_database = db_database

        try:
            self.client = MongoClient(
                f"mongodb+srv://{db_username}:{db_password}@cluster0.ekf91.mongodb.net/{db_project}?retryWrites=true&w=majority")
            self.client.server_info()  # test database connection
        except errors.ServerSelectionTimeoutError:
            msg = "Connection to database failed.\n\n"
            raise self._error(msg)

        self.op_print = op_print
        if self.op_print:
            print(f"Connection to database '{db_database}' successful.")

        self.db = self.client[db_database]
        self.db_collections = self.db.list_collection_names()

        self._user = None
        self.user = user

    def __repr__(self):
        return f"\nYou are connected to: {self.db_database}" \
               f"\n\tLogged in as: {self.user}"

    def __str__(self):
        return f"\nYou are connected to: {self.db_database}" \
               f"\n\tLogged in as: {self.user}"

    @classmethod
    def _init_(cls):
        from . import cript_types
        cls.cript_types = cript_types

    @property
    def user(self):
        return self._user

    @user.setter
    @type_check_property
    def user(self, user):
        """
        Takes str(email or uid) and will find User node, or you can provide user node
        :param user: email, or uid or User node
        :return:
        """
        if user is None:
            self._user = user
            if self.op_print:
                print(f"Not yet logged in.")
            return

        elif isinstance(user, str) and "@" in user:
            self._user = self._user_find_by_email(user)
        elif isinstance(user, str) and id_type_check(user):
            self._user = self._user_find_by_id(user)
        elif isinstance(user, User) and user.uid is not None:
            self._user = user
            CriptDB.user_update += 1
            if CriptDB.user_update > 1:
                return
        else:
            msg = f"User login failed due to invalid object ({user}) passed to user. " \
                  f"(accepted values: email or uid or user node 'after being saved')\n\n"
            raise self._error(msg)

        if self.op_print:
            print(f"Login as '{self.user.name}' was successful.")

    def _user_find_by_email(self, email: str) -> User:
        """
        Find User by email address
        :param email:
        :return: id as string
        """
        coll = self.db["User"]
        doc = coll.find_one({"email": email})
        if doc is None:
            msg = f"{email} not found in database."
            raise self._error(msg)

        return load(doc)

    def _user_find_by_id(self, uid: str) -> User:
        """
        Given the uid check if user exists
        :param uid:
        :return:
        """
        coll = self.db["User"]
        doc = coll.find_one({"_id": ObjectId(uid)})
        if doc is None:
            msg = f"{uid} not found in database."
            raise self._error(msg)

        return load(doc)

    @login_check
    def save(self, obj, parent_obj=None):
        """
        Saves item to database

        Example:
            Solo saves (user, group)
        save('user node')   automatically logs you in
        save('group node')  automatically add user as owner, and adds the group to user node
        save('publication')
        save('material')

            pair saves (collection, experiment, inventory, material, process, data)
        save('collection node', 'group node')
        save('collection node','publication node')
        save('experiment node', 'collection node')
        save('inventory node', 'group node')
        save('material', 'inventory')
        save('material', ['inventory node', 'inventory node', 'experiment node'])
        save('process', 'experiment node')
        save('data', ['experiment node', 'process node'])


        :param obj: The object to be saved.
        :param parent_obj: The object you want it to be added to, or dict of that node.
        :return:
        """
        # pre - checks
        if isinstance(parent_obj, dict):
            parent_obj = load(parent_obj)
        self._pre_save_checks(obj, parent_obj)

        # save to database
        self._do_save(obj)

        # output to user
        if self.op_print:
            print(f"Save of '{obj.name}' was successful.")

        # post - checks
        self._post_save_checks(obj, parent_obj)

        return obj.uid

    def _do_save(self, obj):
        # create document from python object
        doc = self._create_doc(obj)

        # select collection based on class type
        coll = self.db[obj.class_]

        # save document and put generated uid back into object
        obj.uid = str(coll.insert_one(doc).inserted_id)

    def _create_doc(self, obj):
        """
        Converts a CRIPT node into document for upload to mongoDB
        """
        # add time stamps
        self._set_time_stamps(obj)

        # check for incomplete object references
        self._obj_reference_check(obj)

        # convert to dictionary
        doc = obj.as_dict(save=True)

        # remove empty id
        doc["_id"] = doc.pop("uid")

        # remove any unused attributes
        doc = obj.dict_remove_none(doc)
        return doc

    @staticmethod
    def _set_time_stamps(obj):
        """
        Adds time stamps to CRIPT node.
        """
        now = datetime.utcnow()
        if obj.created_date is None:
            obj.created_date = now

        obj.last_modified_date = now

    def _obj_reference_check(self, obj):
        """
        a reference my not have both uid and name, so this will find the document and add it.
        """
        ref_keys = [k.strip("_") for k in vars(obj) if k[:3] == "_c_"]

        for key in ref_keys:
            value = getattr(obj, key)
            if value is None:
                continue
            elif isinstance(value, list):
                new_value = []
                for item in value:
                    if isinstance(item, dict):
                        new_value.append(item)
                    elif isinstance(item, str):  # if string look up and get the extra details
                        coll = self.db[key[2:].capitalize()]
                        result = coll.find_one({"_id": ObjectId(item)})
                        if result:
                            node = load(result)
                            new_value.append(node._reference())
                        else:
                            msg = f"'{item}' in '{key}' not found in database."
                            raise self._error(msg)
                    else:
                        msg = f"'{item}' in '{key}' is an invalid object type."
                        raise self._error(msg)

                setattr(obj, key, "_clear")
                setattr(obj, key, new_value)

    def _doc_reference_check(self, doc: dict) -> dict:
        """
        a reference my not have both uid and name, so this will find the document and add it.
        """
        ref_keys = [k for k in doc.keys() if k[:2] == "c_"]

        for key in ref_keys:
            value = doc[key]
            if value is None:
                continue
            elif isinstance(value, list):
                new_value = []
                for item in value:
                    if isinstance(item, dict):
                        new_value.append(item)
                    elif isinstance(item, str):  # if string look up and get the extra details
                        coll_name = key[2:].capitalize()
                        coll = self.db[coll_name]
                        result = coll.find_one({"_id": ObjectId(item)})
                        if result:
                            node = load(result)
                            new_value.append(node._reference())
                        else:
                            msg = f"'{item}' in '{key}' not found in database."
                            raise self._error(msg)
                    else:
                        msg = f"'{item}' in '{key}' is an invalid object type."
                        raise self._error(msg)

                doc[key] = new_value

        return doc

    def _pre_save_checks(self, obj, parent_obj):
        """
        This function checks the database for conflicts.
        """
        # General checks
        if not isinstance(obj, tuple(self.cript_types.values())):
            msg = f"{obj} is not a valid CRIPT node."
            raise self._error(msg)

        if isinstance(parent_obj, tuple(self.cript_types.values())) or parent_obj is None:
            pass
        elif isinstance(parent_obj, list):
            for i in parent_obj:
                if isinstance(i, tuple(self.cript_types.values())):
                    pass
                else:
                    msg = f"{i} is not a valid CRIPT node for {obj.name}."
                    raise self._error(msg)
        else:
            msg = f"{parent_obj} is not a valid CRIPT node."
            raise self._error(msg)

        if obj.uid is not None:
            msg = "uid should not have an id already. If you are trying to update an existing doc, "\
                            "don't use 'save', use 'update'."
            raise self._error(msg)

        if parent_obj is not None:
            if isinstance(parent_obj, list):
                for i in parent_obj:
                    if i.uid is None:
                        msg = f"{i.name} needs to be saved first."
                        raise self._error(msg)
            else:
                if parent_obj.uid is None:
                    msg = f"{parent_obj.name} needs to be saved first."
                    raise self._error(msg)

        # Class specific checks.
        if obj.class_ == "User":
            coll = self.db[obj.class_]
            # must have unique email address
            if coll.find_one({"email": obj.email}) is not None:
                msg = f"{obj.email} is already registered in the database."
                raise self._error(msg)

        elif obj.class_ == "Group":
            obj.c_owner = self.user._reference()

        elif obj.class_ == "Collection":
            parent_obj_types = ["Group", "Publication"]
            self._parent_obj_check(obj, parent_obj, parent_obj_types)

        elif obj.class_ == "Experiment":
            parent_obj_types = ["Collection"]
            self._parent_obj_check(obj, parent_obj, parent_obj_types)

        elif obj.class_ == "Material":
            parent_obj_types = ["Experiment", "Inventory", None]
            self._parent_obj_check(obj, parent_obj, parent_obj_types)

        elif obj.class_ == "Process":
            parent_obj_types = ["Experiment"]
            self._parent_obj_check(obj, parent_obj, parent_obj_types)

        elif obj.class_ == "Data":
            parent_obj_types = ["Experiment", "Material", "Process"]
            self._parent_obj_check(obj, parent_obj, parent_obj_types)
            obj = self._save_file(obj)

        elif obj.class_ == "Inventory":
            parent_obj_types = ["Group", "Collection"]
            self._parent_obj_check(obj, parent_obj, parent_obj_types)

        elif obj.class_ == "Publication":
            pass

        else:
            msg = f"{obj.class_} cannot be saved by itself."
            raise self._error(msg)

    def _parent_obj_check(self, obj, parent_obj, parent_obj_types):
        if parent_obj is None:
            if None in parent_obj_types:
                return
            else:
                pass

        if isinstance(parent_obj, list):
            for i in parent_obj:
                if i.class_ not in parent_obj_types:
                    break
            else:
                return

        if hasattr(parent_obj, "class_") and parent_obj.class_ in parent_obj_types:
            return
        else:
            pass

        msg = f"Saving a {obj.class_} requires a parent_obj to be {parent_obj_types}."
        raise self._error(msg)

    def _save_file(self, obj):
        file_storage = GridFS(self.db)

        keys_of_files = [k.lstrip("_") for k, v in vars(obj).items() if isinstance(v, File)]
        for key in keys_of_files:
            file = obj.__getattribute__(key)
            if file.uid is None:
                with open(file.path, 'rb') as f:
                    contents = f.read()
                file.uid = file_storage.put(contents)
                file.path = None  # clear path - we don't need users personal file path
            else:
                mes = "update file not setup yet"
                raise self._error(mes)

    def _post_save_checks(self, obj, parent_obj):
        """
        This function checks the database for conflicts.
        """
        if obj.class_ == "User":
            pass

        elif obj.class_ == "Group":
            # adding new group to current user logged in
            try:  # Try to find a user node in the Python stack/globals
                for i in range(100):
                    frames = sys._getframe(i)
                    globals_ = frames.f_globals
                    user_node = [globals_[k] for k, v in globals_.items() if isinstance(v, User) and k[0] != "_"]
                    if user_node:
                        user_node = user_node[0]
                        user_node.c_group = obj.uid
                        break

            except AttributeError:  # if no User node found, just load it in and update it
                coll = self.db["User"]
                doc = coll.find_one({"_id": ObjectId(self.user)})
                user_node = load(doc)
                user_node.c_group = obj.uid

            self.update(user_node)

        elif obj.class_ == "Collection":
            attr = "c_" + obj.class_.lower()
            if isinstance(parent_obj, list):
                for i in parent_obj:
                    setattr(i, attr, obj)
                    self.update(i)
            else:
                setattr(parent_obj, attr, obj)
                self.update(parent_obj)

        elif obj.class_ == "Experiment":
            attr = "c_" + obj.class_.lower()
            if isinstance(parent_obj, list):
                for i in parent_obj:
                    setattr(i, attr, obj)
                    self.update(i)
            else:
                setattr(parent_obj, attr, obj)
                self.update(parent_obj)

        elif obj.class_ == "Inventory":
            attr = "c_" + obj.class_.lower()
            if isinstance(parent_obj, list):
                for i in parent_obj:
                    setattr(i, attr, obj)
                    self.update(i)
            else:
                setattr(parent_obj, attr, obj)
                self.update(parent_obj)

        elif obj.class_ == "Material":
            attr = "c_" + obj.class_.lower()
            if isinstance(parent_obj, list):
                for i in parent_obj:
                    setattr(i, attr, obj)
                    self.update(i)
            elif parent_obj is None:
                pass
            else:
                setattr(parent_obj, attr, obj)
                self.update(parent_obj)

        elif obj.class_ == "Process":
            attr = "c_" + obj.class_.lower()
            if isinstance(parent_obj, list):
                for i in parent_obj:
                    setattr(i, attr, obj)
                    self.update(i)
            else:
                setattr(parent_obj, attr, obj)
                self.update(parent_obj)

        elif obj.class_ == "Data":
            attr = "c_" + obj.class_.lower()
            if isinstance(parent_obj, list):
                for i in parent_obj:
                    setattr(i, attr, obj)
                    self.update(i)
            else:
                setattr(parent_obj, attr, obj)
                self.update(parent_obj)

    @login_check
    def view(self, obj, query: dict = None, num_results: int = 50):
        """
        View/search based on node.

        Examples:
            shows all in *your* groups
        view(C.Collection)                      shows all collections from all groups you are apart of
        view(C.Inventory)                       shows all inventories from all groups you are apart of
        view(C.Experiment)                      shows all experiments from all groups and collections
        view(C.Data)                            shows all data from all groups and collections

            shows one file
        view('uid')                                 shows just that object (can be group, collection, etc.)

            shows all in database
        view(C.Group, {"scope": "all"})                    shows all groups in database
        view(C.Material, {"scope": "all"})                 shows all materials in database



        :param obj: The node type you want or uid of node you want
        :param query:
        :param num_results:
        :return:
        """
        # if obj is cript node
        if obj in tuple(self.cript_types.values()):
            result, key = self._search(obj, query, num_results)
            self._print_table(result, key)

        # if obj is uid
        elif id_type_check_bool(obj):   ### This search should be improved, for loop bad idea _> probably change from random to user defined _id with class embedded
            result = None
            for coll in self.db_collections:
                coll = self.db[coll]
                result = coll.find_one({"_id": ObjectId(obj)})
                if result is not None:
                    break

            if result is None:
                mes = f"{obj} not found."
                raise self._error(mes)
            else:
                print(result)

        else:
            msg = "Invalid input."
            raise self._error(msg)

        return result

    def _search(self, obj, query: dict = None, num_results: int = 50):
        """

        """
        key = None
        if isinstance(query, dict):
            if "scope" in query and query["scope"] == "all":
                # search whole database
                result = self._search_full_collection(obj, query, num_results)
            else:
                # search your nodes with query
                print("your query not currently supported.")
                result = None

        elif query is None:
            result, key = self._search_local(obj, num_results)
        else:
            mes = f"{query} is not a valid object for viewing."
            raise self._error(mes)

        return result, key

    def _search_full_collection(self, obj, query: dict = None, num_results: int = 50):
        """
        Search the full collection
        """
        coll = self.db[obj._class]
        if len(query.keys()) == 1:
            # search whole collection
            result = list(coll.find({}, limit=num_results))
        else:
            try:
                result = list(coll.find(query["key"], limit=num_results))
            except Exception:
                mes = f"Not a valid query."
                raise self._error(mes)

        return result

    def _search_local(self, obj, num_results: int = 50):   ######## Could be refactored.
        """
        Get everything the user is associated with.
        """
        result = []
        key = []

        if obj is self.cript_types["User"]:
            result = self.user
            key = None
        elif obj is self.cript_types["Group"]:
            for group in self.user.c_group:
                group_dict = self.db["Group"].find_one({"_id": ObjectId(group["uid"])})
                if group_dict is not None:
                    result.append(group_dict)
            key = None
        elif obj is self.cript_types["Collection"]:
            for group in self.user.c_group:
                group_dict = self.db["Group"].find_one({"_id": ObjectId(group["uid"])})
                if group_dict is not None:
                    if "c_collection" in group_dict.keys():
                        for collection in group_dict["c_collection"]:
                            coll_dict = self.db["Collection"].find_one({"_id": ObjectId(collection["uid"])})
                            if coll_dict is not None:
                                result.append(coll_dict)
                                key.append(f".{group['name']}")
        elif obj is self.cript_types["Experiment"]:
            for group in self.user.c_group:
                group_dict = self.db["Group"].find_one({"_id": ObjectId(group["uid"])})
                if group_dict is not None:
                    if "c_collection" in group_dict.keys():
                        for collection in group_dict["c_collection"]:
                            coll_dict = self.db["Collection"].find_one({"_id": ObjectId(collection["uid"])})
                            if coll_dict is not None:
                                if "c_experiment" in coll_dict.keys():
                                    for expt in coll_dict["c_experiment"]:
                                        expt_dict = self.db["Experiment"].find_one({"_id": ObjectId(expt["uid"])})
                                        if expt_dict is not None:
                                            result.append(expt_dict)
                                            key.append(f".{group['name']}.{collection['name']}")
        elif obj is self.cript_types["Inventory"]:
            for group in self.user.c_group:
                group_dict = self.db["Group"].find_one({"_id": ObjectId(group["uid"])})
                if group_dict is not None:

                    if "c_inventory" in group_dict.keys():
                        for inventory in group_dict["c_inventory"]:
                            inventory_dict = self.db["Inventory"].find_one({"_id": ObjectId(inventory["uid"])})
                            if inventory_dict is not None:
                                result.append(inventory_dict)
                                key.append(f".{group['name']}")

                    if "c_collection" in group_dict.keys():
                        for collection in group_dict["c_collection"]:
                            coll_dict = self.db["Collection"].find_one({"_id": ObjectId(collection["uid"])})
                            if coll_dict is not None:
                                if "c_inventory" in coll_dict.keys():
                                    for inventory in coll_dict["c_inventory"]:
                                        inventory_dict = self.db["Inventory"].find_one({"_id": ObjectId(inventory["uid"])})
                                        if inventory_dict is not None:
                                            result.append(inventory_dict)
                                            key.append(f".{group['name']}.{collection['name']}")

        elif obj is self.cript_types["Material"]:
            for group in self.user.c_group:
                group_dict = self.db["Group"].find_one({"_id": ObjectId(group["uid"])})
                if group_dict is not None:

                    if "c_inventory" in group_dict.keys():
                        for inventory in group_dict["c_inventory"]:
                            inventory_dict = self.db["Inventory"].find_one({"_id": ObjectId(inventory["uid"])})
                            if inventory_dict is not None:
                                for mat in inventory_dict["c_material"]:
                                    mat_dict = self.db["Material"].find_one({"_id": ObjectId(mat["uid"])})
                                    if mat_dict is not None:
                                        result.append(mat_dict)
                                        key.append(f".{group['name']}.{inventory['name']}")

                    if "c_collection" in group_dict.keys():
                        for collection in group_dict["c_collection"]:
                            coll_dict = self.db["Collection"].find_one({"_id": ObjectId(collection["uid"])})
                            if coll_dict is not None:

                                if "c_inventory" in coll_dict.keys():
                                    for inventory in coll_dict["c_inventory"]:
                                        inventory_dict = self.db["Inventory"].find_one({"_id": ObjectId(inventory["uid"])})
                                        if inventory_dict is not None:
                                            for mat in inventory_dict["c_material"]:
                                                mat_dict = self.db["Material"].find_one({"_id": ObjectId(mat["uid"])})
                                                if mat_dict is not None:
                                                    result.append(mat_dict)
                                                    key.append(f".{group['name']}.{inventory['name']}")

                                if "c_experiment" in coll_dict.keys():
                                    for expt in coll_dict["c_experiment"]:
                                        expt_dict = self.db["Experiment"].find_one({"_id": ObjectId(expt["uid"])})
                                        if expt_dict is not None:
                                            for mat in expt_dict["c_material"]:
                                                mat_dict = self.db["Material"].find_one({"_id": ObjectId(mat["uid"])})
                                                if mat_dict is not None:
                                                    result.append(mat_dict)
                                                    key.append(f".{group['name']}.{expt['name']}")

        elif obj is self.cript_types["Process"]:
            for group in self.user.c_group:
                group_dict = self.db["Group"].find_one({"_id": ObjectId(group["uid"])})
                if group_dict is not None:
                    if "c_collection" in group_dict.keys():
                        for collection in group_dict["c_collection"]:
                            coll_dict = self.db["Collection"].find_one({"_id": ObjectId(collection["uid"])})
                            if coll_dict is not None:
                                if "c_experiment" in coll_dict.keys():
                                    for expt in coll_dict["c_experiment"]:
                                        expt_dict = self.db["Experiment"].find_one({"_id": ObjectId(expt["uid"])})
                                        if expt_dict is not None:
                                            for proc in expt_dict["c_process"]:
                                                proc_dict = self.db["Process"].find_one({"_id": ObjectId(proc["uid"])})
                                                if proc_dict is not None:
                                                    result.append(proc_dict)
                                                    key.append(f".{group['name']}.{expt['name']}")

        elif obj is self.cript_types["Data"]:
            for group in self.user.c_group:
                group_dict = self.db["Group"].find_one({"_id": ObjectId(group["uid"])})
                if group_dict is not None:
                    if "c_collection" in group_dict.keys():
                        for collection in group_dict["c_collection"]:
                            coll_dict = self.db["Collection"].find_one({"_id": ObjectId(collection["uid"])})
                            if coll_dict is not None:
                                if "c_experiment" in coll_dict.keys():
                                    for expt in coll_dict["c_experiment"]:
                                        expt_dict = self.db["Experiment"].find_one({"_id": ObjectId(expt["uid"])})
                                        if expt_dict is not None:
                                            for data in expt_dict["c_data"]:
                                                data_dict = self.db["Data"].find_one({"_id": ObjectId(data["uid"])})
                                                if data_dict is not None:
                                                    result.append(data_dict)
                                                    key.append(f".{group['name']}.{expt['name']}")

        return result, key

    @staticmethod
    def _print_table(result: list[dict], key: list[str]):
        """
        Print to screen as nice table from
        :param result:
        :return:
        """
        if key is None:
            row_format = "{:<8}" + "{:<30}" * 2
            print("")
            print(row_format.format("number", "name", "uid"))
            print("-" * 60)
            if result:
                for i, doc in enumerate(result):
                    print(row_format.format(str(i), doc["name"][:25], str(doc["_id"])))
                print("")
            else:
                print("No results.")
        else:
            row_format = "{:<8}" + "{:<30}" * 3
            print("")
            print(row_format.format("number", "key", "name", "uid"))
            print("-" * 60)
            if result:
                for i, (doc, k) in enumerate(zip(result, key)):
                    print(row_format.format(str(i), k, doc["name"][:25], str(doc["_id"])))
                print("")
            else:
                print("No results.")

    @login_check
    def update(self, obj):

        # pre - checks
        self._pre_update_checks(obj)

        # get current doc from database
        old_doc = self._get_doc_from_obj(obj)

        # create new doc
        new_doc = self._create_doc(obj)

        # get differences
        patch = self._create_json_patch(old_doc, new_doc)

        # Do update
        self._update_from_patch(obj, patch, new_doc)

        # post - checks
        self._post_update_checks(obj)

    def _get_doc_from_obj(self, obj) -> dict:
        """Get document from database given a node"""
        coll = self.db[obj.class_]
        doc = coll.find_one({"_id": ObjectId(obj.uid)})
        if doc is None:
            mes = f"Previous document not found in database. ('{obj.name}', '{obj.uid}')"
            raise self._error(mes)
        return doc

    @staticmethod
    def _create_json_patch(doc_old, doc_new):
        """
        Creates patch from old and new document
        :param doc_old:
        :param doc_new:
        :return:
        """
        # cleaning up non-JSON dump-able objects
        doc_old["_id"] = str(doc_old["_id"])

        remove_keys = ["created_date", "last_modified_date"]
        for key in remove_keys:
            doc_old.pop(key)
            doc_new.pop(key)

        return JsonPatch.from_diff(src=doc_old, dst=doc_new)

    def _update_from_patch(self, obj, patch, doc_new):
        """

        """
        coll = self.db[obj.class_]
        changes = {}
        for p in patch:
            key = p["path"].split("/")[1]
            if key not in changes.keys():
                changes[key] = doc_new[key]

        result = coll.update_one({"_id": ObjectId(obj.uid)}, {"$set": changes})
        if not result.acknowledged:
            msg = f"Error in updating {obj.name}."
            raise self._error(msg)
        else:
            print(f"Update of '{obj.name}' successful!")

    def _pre_update_checks(self, obj):
        pass

    def _post_update_checks(self, obj):

        if obj.class_ == "User":
            if obj is not self.user:
                self.user = obj

    @login_check
    def delete(self, obj):
        pass
