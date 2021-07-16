from pymongo import MongoClient
from typing import Type
import cript

class criptdb:
    instances = 0

    def __init__(self, username: str, password: str, project: str, database: str, op_print = True):
        if self.instances > 0:
            raise UserError("Connection to CRIPT database already exists.")
        self.instances += 1


        self.client = MongoClient(
            f"mongodb+srv://{username}:{password}@cluster0.ekf91.mongodb.net/{project}?retryWrites=true&w=majority")
        self.db = self.client[database]
        self.collection = self.db.list_collection_names()

        self.op_print = op_print
        if self.op_print:
            print(f"Connection to database '{database}' successful.")

    def save(self, obj: type[cript.user]):
        doc = obj.as_dict()

        doc["_id"] = doc.pop("uid")  # need to happen recursively

        coll = self.db[obj.class_]
        coll.insert_one(doc).inserted_id
        if self.op_print:
            print(f"'{obj.name}' was saved to the database.")

    def update(self):
        pass