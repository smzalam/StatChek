from pymongo import MongoClient
from pymongo.server_api import ServerApi
import pymongo.errors as e
from pprint import pprint

class MongoDB:
    def __init__(self, password):
        self.uri = f"mongodb+srv://sighed:{password}@statchek.4ndej2y.mongodb.net/?retryWrites=true&w=majority"
        self.client = None
        self.db = None
        self.collection = None
        self.errors = [
            e.ConnectionFailure,
            e.DuplicateKeyError,
            e.InvalidOperation,
            e.InvalidURI,
            e.OperationFailure
        ]

    def print_states(self):
        instance_stats = {
            'client': self.client,
            'db': self.db,
            'collection': self.collection
        }
        pprint(instance_stats)

    def db_conn_test(self):
        """
        Send a ping to confirm a successful connection
        """
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def connect_client(self):
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.db_conn_test()

    def connect_db(self, database: str):
        self.db = self.client[database]
        print(f'Connected to database: {self.db.name}')

    def connect_collection(self, collection: str):
        self.collection = self.db[collection]
        print(f'Connected to database: {self.collection.name}')

    def insert_documents(self, many: bool, documents: dict | list):
        if many:
            try:
                result = self.collection.insert_many(documents)
                print(f'Inserted documents into {self.db.name}:{self.collection.name}')
                return result.inserted_ids
            except Exception as e:
                print(e)
        else:
            try:
                result = self.collection.insert_one(documents)
                print(f'Inserted document into {self.db.name}:{self.collection.name}')
                return result.inserted_id
            except Exception as e:
                print(e)

    def find_documents(self, many: bool, conditions: dict = None, projections: dict = None):
        if many:
            try:
                result = []
                for document in self.collection.find(conditions, projections):
                    result.append(document)
                print(f'Found documents from {self.db.name}:{self.collection.name}')
                return result
            except Exception as e:
                print(e)
        else:
            try:
                result = self.collection.find_one(conditions, projections)
                print(f'Found document from {self.db.name}:{self.collection.name}')
                return result
            except Exception as e:
                print(e)

    def delete_documents(self, many: bool, conditions: dict = {}):
        if many:
            try:
                result = self.collection.delete_many(conditions)
                print(f'Deleted documents from {self.db.name}:{self.collection.name}')
                return result
            except Exception as e:
                print(e)
        else:
            try:
                result = self.collection.delete_one(conditions)
                print(f'Deleted document from {self.db.name}:{self.collection.name}')
                return result
            except Exception as e:
                print(e)

    def count_documents(self, conditions: dict = {}):
        return self.collection.count_documents(conditions)

    def close_connection(self) -> None:
        self.client.close()
        print("Closed connection!")
