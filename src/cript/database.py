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
            print("Connection to database failed.\n\n")
            raise Exception(err)

        self.op_print = op_print
        if self.op_print:
            print(f"Connection to database '{db_database}' successful.")

        self.db = self.client[db_database]
        self.collections = self.db.list_collection_names()

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
            if len(user) == 24:  # uids are 24 charters long
                if self._user_exists(user):  # check database to make sure user exists
                    self._user = user
                else:
                    raise Exception(f"user({user}) not found.")
            else:
                raise Exception(f"User uids are 24 letters or numbers long. The provided uid is {len(user)}.")

    @login_check
    def save(self, obj):
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

    @login_check
    def update(self):
        pass

    def _create_doc(self, obj):
        # convert to dictionary
        doc = obj.as_dict()

        # remove empty id
        if doc["uid"] is None:
            doc.pop("uid")
        else:
            raise Exception("uid should not have an id already. If you are trying to update an existing doc, "
                            "don't use 'save', use 'update'.")

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
            raise Exception(f"{email} not found in database.")
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

    def view_all(self, obj):
        """
        View all items in a mongodb collection.
        :param obj:
        :return:
        """
        # make sure provided obj is a valid choice
        if obj not in self.collections:
            raise Exception(f"Invalid name provided. Valid names: {self.collections}")

        # Preform search
        coll = self.db[obj]
        result = list(coll.find({}))

        # Print to screen as nice table.
        row_format = "{:<6}" + "{:<30}" * 2
        print("")
        print(row_format.format("number", "name", "uid"))
        print("-" * 60)
        for i, doc in enumerate(result):
            print(row_format.format(str(i), doc["name"][:25], str(doc["_id"])))
        print("")

        return result

    # def list_documents_in_collection(
    #     database: Database = None, collection_name: str = None
    # ) -> List[dict]:
    #     """List all documents in a database collection."""
    #     return [c for c in database[collection_name].find({})]
    #
    # def get_document_by_id(
    #     database: Database = None, collection_name: str = None, uid: Union[str, ObjectId] = None
    # ) -> dict:
    #     """Get a document from a database collection using its uid."""
    #     uid = ObjectId(uid)
    #     return database[collection_name].find_one({"_id": uid})


# doc["_id"] = doc.pop("uid")  # need to happen recursively