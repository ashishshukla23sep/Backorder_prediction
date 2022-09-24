import boto3
from backorder.constant import *
from backorder.database.mangodb import MangoDbconnection
from backorder.exception import BackOrderException
import sys

class CloudKey:
    def __init__(self) -> None:
        pass
    def get_cloud_key(self):
        try:
            records = MangoDbconnection().get_records_from_collection(database_name=DATABASE_NAME,collection_name=COLLOCTION_NAME)
            records = [i for i in records]
            access_key = records[1]['access_key']
            secret_access_key = records[1]['secret_access_key']

            return access_key,secret_access_key
        except Exception as e:
            raise BackOrderException(e,sys) from e