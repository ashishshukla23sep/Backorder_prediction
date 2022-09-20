from inspect import trace
from backorder.entity.config_entity import DataIngestionConfig
import sys,os
from backorder.exception import BackOrderException
from backorder.logger import logging
from backorder.entity.artifact_entity import DataIngestionArtifact
from zipfile import ZipFile
import numpy as np
from six.moves import urllib
from urllib.request import urlopen
from io import BytesIO
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig ):
        try:
            logging.info(f"{'>>'*20}Data Ingestion log started.{'<<'*20} ")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise BackOrderException(e,sys)
    

    def download_housing_data(self,) -> str:
        try:
            #extraction remote url to download dataset
            download_url = self.data_ingestion_config.dataset_download_url

            #folder location to download file
            zip_download_dir = self.data_ingestion_config.zip_download_dir
            
            os.makedirs(zip_download_dir,exist_ok=True)

            backorder_file_name = os.path.basename(download_url)

            zip_file_path = os.path.join(zip_download_dir, backorder_file_name)

            logging.info(f"Downloading file from :[{download_url}] into :[{zip_file_path}]")
            urllib.request.urlretrieve(download_url, zip_file_path)
            logging.info(f"File :[{zip_file_path}] has been downloaded successfully.")
            return r'C:\Users\\1672040\Desktop\\project\\back_order_prediction\\dataset.zip'

        except Exception as e:
            raise BackOrderException(e,sys) from e

    def extract_zip_file(self,zip_file_path:str):
        try:
            

            os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
            os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok= True)

            logging.info(f"Extracting zip file: [{zip_file_path}] into train dir: [{self.data_ingestion_config.ingested_train_dir}] and test dir: [{self.data_ingestion_config.ingested_test_dir}]")


            with ZipFile(zip_file_path,'r') as backorder_tgz_file_obj:
                for info in backorder_tgz_file_obj.infolist():
                    if 'Test' in info.filename or 'test' in info.filename:
                        test_data_dir = os.path.join(self.data_ingestion_config.ingested_test_dir,str(info.filename).replace('/','\\'))
                        backorder_tgz_file_obj.extract(info.filename,path=self.data_ingestion_config.ingested_test_dir)
                    else:
                        train_data_dir = os.path.join(self.data_ingestion_config.ingested_train_dir,str(info.filename).replace('/','\\'))
                        backorder_tgz_file_obj.extract(info.filename,path=self.data_ingestion_config.ingested_train_dir)
            logging.info(f"Extraction completed")
            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_data_dir,
                                test_file_path=test_data_dir,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")

            return data_ingestion_artifact
        except Exception as e:
            raise BackOrderException(e,sys) from e
    
   

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            zip_file_path =  self.download_housing_data()
            
            return self.extract_zip_file(zip_file_path=zip_file_path)
        except Exception as e:
            raise BackOrderException(e,sys) from e
    


    # def __del__(self):
    #     logging.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")
