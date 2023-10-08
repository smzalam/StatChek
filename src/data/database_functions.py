from dotenv import load_dotenv, find_dotenv
import os, pprint
from pymongo import MongoClient
from pymongo.server_api import ServerApi


def db_connect(password):
    """ 
    Create a new client and connect to the server
    """
    
    uri = f"mongodb+srv://sighed:{password}@statchek.4ndej2y.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))

    return client

def db_conn_test(client):
    """
    Send a ping to confirm a successful connection
    """
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

