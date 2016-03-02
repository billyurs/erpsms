import pymongo
from pymongo import MongoClient


class MongoWrapper(object):
    def __init__(self):
        pass

    def mongo_db_connect(self, server_key='', database='erpmongodb'):
        mongo_conn = MongoClient('mongodb://localhost:27017/')
        mongowithdb = mongo_conn[database]
        return mongowithdb

    def get_mongo_collection(self, database='erpmongodb', collection=''):
        # Returns the Collection as specified at parameter
        # In SQL terms return the table
        mongo_db = self.mongo_db_connect(database= database)
        return mongo_db[collection]
