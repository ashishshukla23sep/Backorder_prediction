from backorder.component.data_ingestion import DataIngestion
from backorder.component.data_validation import DataValidation
from backorder.component.model_trainer import ModelTrainer
from backorder.component.data_transformation import DataTransformation
from backorder.config.configuration import Configuartion
import os,sys

config_path = os.path.join("yaml_files","config.yaml")
config = Configuartion(config_file_path=config_path)
data_ingestion = DataIngestion(data_ingestion_config=config.get_data_ingestion_config())
data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
data_validation = DataValidation(data_validation_config=config.get_data_validation_config(),data_ingestion_artifact=data_ingestion_artifact)
data_validation_artifact = data_validation.initiate_data_validation()
print(sys.getsizeof(data_validation_artifact))
data_tranformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,data_validation_artifact=data_validation_artifact,data_transformation_config=config.get_data_transformation_config())
data_tranformation_artifact = data_tranformation.initiate_data_transformation()
model_trainer = ModelTrainer(model_trainer_config=config.get_model_trainer_config(),data_transformation_artifact=data_tranformation_artifact)
model_trainer_artifact = model_trainer.initiate_model_trainer()
