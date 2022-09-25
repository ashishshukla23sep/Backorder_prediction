import boto3
from backorder.constant import *
from backorder.database.mangodb import MangoDbconnection
from backorder.exception import BackOrderException
import sys
import dill
from io import BytesIO
from backorder.constant import *

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

    def upload_file(self,file,key:str):
        
        access_key ,secret_key = self.get_cloud_key()
        try:
            with BytesIO() as f:
                dill.dump(file, f)
                f.seek(0)
                boto3.client("s3",aws_access_key_id=access_key,aws_secret_access_key=secret_key).upload_fileobj(Bucket=BUCKET_NAME, Key=key, Fileobj=f)
        except Exception as e:
            raise BackOrderException(e,sys) from e

    def download_file(self,key:str):
        try:
            access_key ,secret_key = self.get_cloud_key()
            with BytesIO() as f:
                boto3.client("s3",aws_access_key_id=access_key,aws_secret_access_key=secret_key).download_fileobj(Bucket=BUCKET_NAME, Key=key, Fileobj=f)
                f.seek(0)
                file = dill.load(f)
            return file
        except Exception as e:
            raise BackOrderException(e,sys) from e