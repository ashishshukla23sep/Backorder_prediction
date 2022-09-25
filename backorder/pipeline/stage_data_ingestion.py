from backorder.component.data_ingestion import DataIngestion
from backorder.config.configuration import Configuartion
from backorder.logger import logging
import os

STAGE_NAME = "DATA_INGESTION"
def data_ingestion():
    logging.info(f">>>>>> stage DATA_INGESTION  started <<<<<<")
    config_path = os.path.join("yaml_files","config.yaml")
    config = Configuartion(config_file_path=config_path)
    data_ingestion = DataIngestion(data_ingestion_config=config.get_data_ingestion_config())
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
    logging.info(f">>>>>> stage DATA_INGESTION  Ended <<<<<<")

    return config,data_ingestion_artifact