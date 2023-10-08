from database_class import MongoDB
from dotenv import load_dotenv, find_dotenv
import os, pprint

load_dotenv(find_dotenv())
password = os.environ.get('MONGODB_PW')

mongodb = MongoDB(password)
mongodb.connect_client()
