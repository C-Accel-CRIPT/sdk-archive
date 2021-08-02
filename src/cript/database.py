"""
Database Connection

"""
from datetime import datetime
from typing import Union

from pymongo import MongoClient, errors
from bson import ObjectId
from jsonpatch import JsonPatch

from .utils.type_check import *
from .utils.database_tools import *


class CriptDB:
    instances = 0

    def __init__(self,
                 db_username: str,
                 db_password: str,
                 db_project: str,
                 db_database: str,
                 user: str = None,
                 op_print: bool = True):
        """
        This class handles all communication with MongoDB.
        :param db_username: mongoDB username
        :param db_password: mongoDB password
        :param db_project: mongoDB project
        :param db_database: name of database on mongoDB
        :param user: provide email or uid for user you want to login with
        :param op_print: True to get printouts from database commands
        """

        if self.instances > 0:
            raise Exception("Connection to CRIPT database already exists.")
        self.instances += 1

        self.db_username = db_username
        self.db_password = db_password
        self.db_project = db_project
        self.db_database = db_database

        try:
            self.client = MongoClient(
                f"mongodb+srv://{db_username}:{db_password}@cluster0.ekf91.mongodb.net/{db_project}?retryWrites=true&w=majority")
            self.client.server_info()  # test database connection
        except errors.ServerSelectionTimeoutError as err:
            msg = "Connection to database failed.\n\n"
            raise cript.CRIPTError(msg)

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

    @property
    def user(self):
        return self._user

    @user.setter
    @type_check_property
    def user(self, user):
        if user is None:
            self._user = user
        elif "@" in user:
            # if user provides email address find their id for them.
            self._user = self._user_find_by_email(user)
        else:
            if id_type_check(user):
                if self._user_exists(user):  # check database to make sure user exists
                    self._user = user
                else:
                    msg = f"user('{user}') not found."
                    raise cript.CRIPTError(msg)

    def _user_find_by_email(self, email: str) -> str:
        """
        Find User by email address
        :param email:
        :return: id as string
        """
        coll = self.db["User"]
        doc = coll.find_one({"email": email})
        if doc is None:
            msg = f"{email} not found in database."
            raise cript.CRIPTError(msg)

        return str(doc["_id"])

    def _user_exists(self, uid: str) -> bool:
        """
        Given the uid check if user exists
        :param uid:
        :return:
        """
        coll = self.db["User"]
        doc = coll.find_one({"_id": ObjectId(uid)})
        if doc is not None:
            return True
        else:
            return False


    @login_check
    def save(self, obj):
        """
        Saves item to database

        Example:
        save('user node')
        save('group node')

        :param obj: The object to be saved.
        :return:
        """
        # checks
        self._save_checks(obj)

        # create document from python object
        doc = self._create_doc(obj)

        # select collection based on class type
        coll = self.db[obj.class_]

        # save document and put generated uid back into object
        obj.uid = str(coll.insert_one(doc).inserted_id)

        # output to user
        if self.op_print:
            print(f"'{obj.name}' was saved to the database.")

        return obj.uid

    def _create_doc(self, obj):
        """
        Converts a CRIPT node into document for upload to mongoDB
        """
        # add time stamps
        self._set_time_stamps(obj)

        # convert to dictionary
        doc = obj.as_dict()

        # remove empty id
        doc["_id"] = doc.pop("uid")

        # check for incomplete object references
        doc = self._doc_reference_check(doc)

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
                            node = cript.load(result)
                            new_value.append(node._create_reference())
                        else:
                            msg = f"'{item}' in '{key}' not found in database."
                            raise CRIPTError(msg)
                    else:
                        msg = f"'{item}' in '{key}' is an invalid object type."
                        raise CRIPTError(msg)

                doc[key] = new_value

        return doc

    def _save_checks(self, obj):
        """
        This function checks the database for conflicts.
        """
        coll = self.db[obj.class_]

        if obj.uid is not None:
            msg = "uid should not have an id already. If you are trying to update an existing doc, "\
                            "don't use 'save', use 'update'."
            raise cript.CRIPTError(msg)

        if obj.class_ == "User":
            # must have unique email address
            if coll.find_one({"email": obj.email}) is not None:
                msg = f"{obj.email} is already registered in the database."
                raise CRIPTError(msg)

        elif obj.class_ == "Group":
            pass

        elif obj.class_ == "Collection":
            pass

        elif obj.class_ == "Experiment":
            pass

        elif obj.class_ == "Material":
            pass

    @login_check
    def view(self, obj, sort_by: str = None, num_results: int = 50):
        """
        View/search based on node.

        Examples:
            shows all in database
        view(cript.Group)                           shows all groups
        view(cript.Material)                        shows all materials
        view(cript.Publication)                     shows all publications

            shows all in your groups
        view(cript.Collection)                      shows all collections from all groups you are apart of
        view(cript.Inventory)                       shows all inventories from all groups you are apart of
        view(cript.Experiment)                      shows all experiments from all groups and collections
        view(cript.Process)                         shows all processes from all groups and collections
        view(cript.Simulation)                      shows all simulation from all groups and collections
        view(cript.Data)                            shows all data from all groups and collections

            shows one file
        view('uid')                                 shows just that object (can be group, collection, etc.)

        :param obj: The node type you want or uid of node you want
        :param sort_by:
        :param num_results:
        :return:
        """
        if obj in cript.cript_types.values():
            result = self._search(obj)
            self._print_table(result)
            return result

        elif id_type_check(obj):   #################### This search should be improved, for loop bad idea _> probably change from random to user defined _id with class embedded
            result = None
            for coll in self.db_collections:
                coll = self.db[coll]
                result = coll.find_one({"_id": ObjectId(obj)})
                if result is not None:
                    break

            if result is None:
                mes = f"{obj} not found."
                raise cript.CRIPTError(mes)

            print(result)
            return result

        else:
            msg = "Invalid input."
            raise cript.CRIPTError(msg)

    def _search(self, obj, sort_by: str = None, num_results: int = 50):
        """

        """
        if obj in [cript.Group, cript.Publication, cript.Material]:
            result = self._search_full_collection(obj, sort_by, num_results)
        elif obj in [cript.Collection, cript.Inventory, cript.Experiment, cript.Process, cript.Simulation, cript.Data]:
            result = self._search_with_groups(obj, sort_by, num_results)
        else:
            mes = f"{obj} is not a valid object for viewing."
            raise cript.CRIPTError(mes)

        return result

    def _search_full_collection(self, obj, sort_by: str = None, num_results: int = 50):
        """
        Search the full collection
        """
        coll = self.db[obj._class]
        if sort_by is None:
            result = list(coll.find({}, limit=num_results))
        else:
            result = list(coll.find({}, limit=num_results, sort=[(sort_by, -1)]))
        return result

    def _search_with_groups(self, obj, sort_by: str = None, num_results: int = 50):
        """
        Get groups user is apart of and search those.
        """
        coll = self.db[obj._class]
        if sort_by is None:
            result = list(coll.find({}, limit=num_results))
        else:
            result = list(coll.find({}, limit=num_results, sort=[(sort_by, -1)]))
        return result

    @staticmethod
    def _print_table(result: list[dict]):
        """
        Print to screen as nice table from
        :param result:
        :return:
        """
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

    @login_check
    def update(self, obj):
        # get current document
        coll = self.db[obj.class_]
        old_doc = coll.find_one({"_id": ObjectId(obj.uid)})
        if old_doc is None:
            mes = f"Previous document not found in database. ('{obj.name}', '{obj.uid}')"
            raise cript.CRIPTError(mes)

        # create new doc
        new_doc = self._create_doc(obj)

        # get differences
        patch = self._create_json_patch(old_doc, new_doc)

        # Do update
        self._update_from_patch(obj, patch, new_doc)

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
            raise CRIPTError(msg)
        else:
            print(f"Update of '{obj.name}' successful!")

    @login_check
    def delete(self, obj):
        pass

    @login_check
    def search(self, quary: Union[str, dict], node=None):
        """
        View/search based on a key or value in a node.

        Example:
        .search("styrene", cript.Material)                      searches for the word styrene anywhere in all material nodes
        .search({"preferred_name": "styrene"}, cript.Material)  search for the styrene in only preferred_name in Material node
        .search(
            {"preferred_name": "styrene", "mw": ">1000"},
            cript.Material)

        :param quary:
        :param node:
        :return:
        """
        pass