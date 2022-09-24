import sys
import pymongo
from backorder.exception import BackOrderException
from backorder.util.util import read_yaml_file
from backorder.constant import *
import os,sys
from backorder.logger import logging
import json
from backorder.credentials import Decrypt


class MangoDbconnection:
    def __init__(self,username=None,password=None):
        try:
            if username==None and password==None:
                config_path= CREDENTIAL_FILE_PATH
                self.config = read_yaml_file(file_path=config_path)
                
                self.username = Decrypt(self.config['mongodb']['user_name']).get_decrypted_massage()
                self.password = Decrypt(self.config['mongodb']['password']).get_decrypted_massage()

            else:
                self.username = username
                self.password = username
        except Exception as e:
            raise BackOrderException(e,sys) from e
    
    def get_database_client_object(self):
        """
        Return pymongoClient object
        """
        try:
            client = pymongo.MongoClient(f"mongodb+srv://{self.username}:{self.password}@cluster0.o1yzz.mongodb.net/?retryWrites=true&w=majority")
            return client
        except Exception as e:
            raise BackOrderException(e,sys) from e

    def is_database_present(self,client,db_name):
        try:
            if db_name in client.list_database_names():
                return True
            else:
                return False
        except Exception as e:
            raise BackOrderException(e,sys) from e

    def create_database(self,client,db_name):
        try:
            return client[db_name]
        except Exception as e:
            raise BackOrderException(e,sys) from e


    def is_collection_present(self,collection_name,database):
        try:
            """It verifies the existence of collection name in a database"""
            collection_list = database.list_collection_names()

            if collection_name in collection_list:
                logging.info(f"Collection:'{collection_name}' in Database:'{database}' exists")
                return True
            else:
                logging.info(f"{collection_name}' in Database:'{database}' does not exists OR \n        no documents are present in the collection")
                return False
        except Exception as e:
            raise BackOrderException(e,sys) from e

    
        
    def create_collection(self,database,collection_name):
        try:
            return database[collection_name]
        except Exception as e:
            raise BackOrderException(e,sys) from e

    def create_record(self,collection,data):
        try:
            collection.insert_many(data)
            return len(data)
        except Exception as e:
            raise BackOrderException(e,sys) from e
    
    def create_records(self, collection, data):

        try:
            collection.insert_many(data)
            return len(data)
        except Exception as e:
            raise BackOrderException(e,sys) from e

    def insert_dataframe_into_collection(self, db_name, collection_name, data_frame):
        """
        db_name:Database Name
        collection_name: collection name
        data_frame: dataframe which needs to be inserted
        return:

        """
        try:
            logging.info(f"{'=' * 20}Uploading logs to database.{'=' * 20}")
            data_frame.reset_index(drop=True, inplace=True)
            records = list(json.loads(data_frame.T.to_json()).values())
            client = self.get_database_client_object()
            database = self.create_database(client, db_name)
            collection = self.create_collection(collection_name=collection_name, database=database)
            collection.insert_many(records)
            logging.info(f"{'=' * 20}Logs uploaded successfully.{'=' * 20} ")
            return len(records)
        except Exception as e:
            raise BackOrderException(e,sys) from e

    def get_records_from_collection(self,database_name,collection_name):

        client=self.get_database_client_object()
        db_ = client[database_name]
        coll_ = db_[collection_name]
    
        return coll_.find()
