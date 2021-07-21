from pymongo import MongoClient
from datetime import datetime

#import cript


class criptdb:
    instances = 0

    def __init__(self, username: str, password: str, project: str, database: str, op_print = True):
        if self.instances > 0:
            raise Exception("Connection to CRIPT database already exists.")
        self.instances += 1

        self.client = MongoClient(
            f"mongodb+srv://{username}:{password}@cluster0.ekf91.mongodb.net/{project}?retryWrites=true&w=majority")
        self.db = self.client[database]
        self.collection = self.db.list_collection_names()

        self.op_print = op_print
        if self.op_print:
            print(f"Connection to database '{database}' successful.")

    def save(self, obj):
        doc = self._create_doc(obj)
        coll = self.db[obj.class_]

        # save generated uid back into object
        obj.uid = coll.insert_one(doc).inserted_id
        if self.op_print:
            print(f"'{obj.name}' was saved to the database.")

    def update(self):
        pass

    def _create_doc(self, obj):
        # convert to dictionary
        doc = obj.as_dict()

        # remove empty id
        if doc["uid"] == None:
            doc.pop("uid")
        else:
            raise Exception("uid should not have an id already. If you are trying to update an existing doc, don't use 'save', use 'update'.")

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