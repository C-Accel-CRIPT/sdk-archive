"""
Database Connection

"""
from datetime import datetime

from pymongo import MongoClient, errors
from bson import ObjectId

from .validation_tools import *
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
            if self._id_type_check(user):  # uids are 24 charters long
                if self._user_exists(user):  # check database to make sure user exists
                    self._user = user
                else:
                    msg = f"user({user}) not found."
                    raise cript.CRIPTError(msg)

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
        # create document from python object
        doc = self._create_doc(obj)

        # select collection based on class type
        coll = self.db[obj.class_]

        # save document and put generated uid back into object
        obj.uid = coll.insert_one(doc).inserted_id

        # output to user
        if self.op_print:
            print(f"'{obj.name}' was saved to the database.")

        return obj.uid

    def _create_doc(self, obj):
        # convert to dictionary
        doc = obj.as_dict()

        # remove empty id
        if doc["uid"] is None:
            doc.pop("uid")
        else:
            msg = "uid should not have an id already. If you are trying to update an existing doc, "\
                            "don't use 'save', use 'update'."
            raise cript.CRIPTError(msg)

        # add time stamps
        doc = self._set_time_stamps(doc)

        # remove any unused attributes
        doc = obj.dict_remove_none(doc)
        return doc

    @staticmethod
    def _set_time_stamps(doc):
        now = datetime.utcnow()
        if "created_date" in doc.keys() and doc["created_date"] is None:
            doc["created_date"] = now
        if "last_modified_date" in doc.keys():
            doc["last_modified_date"] = now
        return doc

    def _user_find_by_email(self, email: str) -> str:
        """
        Find User by email address
        :param email:
        :return: id as string
        """
        coll = self.db["user"]
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
        coll = self.db["user"]
        doc = coll.find_one({"_id": ObjectId(uid)})
        if doc is not None:
            return True
        else:
            return False

    @staticmethod
    def _id_type_check(uid: str) -> bool:
        if type(uid) != str:
            msg = f"uids should be type 'str'. The provided uid is {type(uid)}."
            raise cript.CRIPTError(msg)
        if len(uid) != 24:
            msg = f"uids are 24 letters or numbers long. The provided uid is {len(uid)} long."
            raise cript.CRIPTError(msg)

        return True

    @login_check
    def view(self, obj, sort_by: str = None, num_results: int = 50):
        """
        View  items in a mongodb collection.

        Examples:
        view(cript.Group)                           shows all groups
        view(cript.Collection)                      shows all collections from all groups you are apart of
        view(cript.Experiment)                      shows all experiments from all groups and collections
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

        elif self._id_type_check(obj):   #################### This search should be improved, for loop bad idea _> probably change from random to user defined _id with class embedded
            for coll in self.db_collections:
                coll = self.db[coll]
                result = coll.find_one({"_id": ObjectId(obj)})
                if result is not None:
                    break
            print(result)
            return result

        else:
            msg = "Invalid input."
            raise cript.CRIPTError(msg)

    def _search(self, obj, sort_by: str = None, num_results: int = 50):
        """
        Preform search of db_collection

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
        for i, doc in enumerate(result):
            print(row_format.format(str(i), doc["name"][:25], str(doc["_id"])))
        print("")

    @login_check
    def load(self, obj):
        pass

    @login_check
    def delete(self, obj):
        pass

    @login_check
    def update(self, obj):
        pass