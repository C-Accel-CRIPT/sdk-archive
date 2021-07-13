#from .mongo_setup import global_init

from pymongo import MongoClient


if __name__ == '__main__':
    password = "YXMaoE1"
    database = "cript_testing"
    client = MongoClient(
        f"mongodb+srv://DW_cript:{password}@cluster0.ekf91.mongodb.net/{database}?retryWrites=true&w=majority")
    db = client["test"]
    collection = db["user"]

    print(client.list_database_names())
    print(db.list_collection_names())

   # post = {"_id":0, "name": "dylan", "chem": [1,2,3]}
  #  collection.insert_one(post)
