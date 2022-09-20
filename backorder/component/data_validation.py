

from backorder.logger import logging
from backorder.exception import BackOrderException
from backorder.entity.config_entity import DataValidationConfig
from backorder.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
import os,sys
import pandas  as pd
# from evidently.model_profile import Profile
# from evidently.model_profile.sections import DataDriftProfileSection
# from evidently.dashboard import Dashboard
# from evidently.dashboard.tabs import DataDriftTab
from backorder.util.util import read_yaml_file
import json
from backorder.constant import *
class DataValidation:
    

    def __init__(self, data_validation_config:DataValidationConfig,
        data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*30}Data Valdaition log started.{'<<'*30} \n\n")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise BackOrderException(e,sys) from e


    def get_train_and_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df,test_df
        except Exception as e:
            raise BackOrderException(e,sys) from e


    def is_train_test_file_exists(self)->bool:
        try:
            logging.info("Checking if training and test file is available")
            is_train_file_exist = False
            is_test_file_exist = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)

            is_available =  is_train_file_exist and is_test_file_exist

            logging.info(f"Is train and test file exists?-> {is_available}")
            
            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path
                testing_file = self.data_ingestion_artifact.test_file_path
                message=f"Training file: {training_file} or Testing file: {testing_file}" \
                    "is not present"
                raise Exception(message)

            return is_available
        except Exception as e:
            raise BackOrderException(e,sys) from e

    
    def validate_dataset_schema(self)->bool:
        try:
            validation_status = False
            train_df,test_df=self.get_train_and_test_df()
            schema_info  = read_yaml_file(file_path=SCHEMA_FILE_PATH)

            train_column_dtype_dict=dict(zip(train_df.columns,list(map(lambda x:str(x).replace("dtype('","").replace("')","") ,train_df.dtypes.values))))
            test_column_dtype_dict=dict(zip(test_df.columns,list(map(lambda x:str(x).replace("dtype('","").replace("')","") ,test_df.dtypes.values))))

            is_train_data_validated=schema_info['columns']==train_column_dtype_dict
            is_test_data_validated=schema_info['columns']==test_column_dtype_dict

            if is_train_data_validated and is_test_data_validated:
                logging.info(f"Data column and dtypes matches successfully")
                validation_status=True
                return validation_status
            else:
                logging.info(f"Data column and dtypes doesn\'t matches Train data:\n{train_column_dtype_dict}\n Test data\n{test_column_dtype_dict}\n Schema yaml file\n{schema_info['columns']}")
                validation_status=False
                return validation_status

        except Exception as e:
            raise BackOrderException(e,sys) from e

    # def get_and_save_data_drift_report(self):
    #     try:
    #         profile = Profile(sections=[DataDriftProfileSection()])

    #         train_df,test_df = self.get_train_and_test_df()

    #         profile.calculate(train_df,test_df)

    #         report = json.loads(profile.json())

    #         report_file_path = self.data_validation_config.report_file_path
    #         report_dir = os.path.dirname(report_file_path)
    #         os.makedirs(report_dir,exist_ok=True)

    #         with open(report_file_path,"w") as report_file:
    #             json.dump(report, report_file, indent=6)
    #         return report
    #     except Exception as e:
    #         raise BackOrderException(e,sys) from e

    # def save_data_drift_report_page(self):
    #     try:
    #         dashboard = Dashboard(tabs=[DataDriftTab()])
    #         train_df,test_df = self.get_train_and_test_df()
    #         dashboard.calculate(train_df,test_df)

    #         report_page_file_path = self.data_validation_config.report_page_file_path
    #         report_page_dir = os.path.dirname(report_page_file_path)
    #         os.makedirs(report_page_dir,exist_ok=True)

    #         dashboard.save(report_page_file_path)
    #     except Exception as e:
    #         raise BackOrderException(e,sys) from e

    # def is_data_drift_found(self)->bool:
    #     try:
    #         report = self.get_and_save_data_drift_report()
    #         self.save_data_drift_report_page()
    #         return True
    #     except Exception as e:
    #         raise BackOrderException(e,sys) from e

    def initiate_data_validation(self)->DataValidationArtifact :
        try:
            self.is_train_test_file_exists()
            is_validated = self.validate_dataset_schema()
            # self.is_data_drift_found()

            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                is_validated=is_validated,
                message="Data Validation performed successully."
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise BackOrderException(e,sys) from e


    # def __del__(self):
    #     logging.info(f"{'>>'*30}Data Valdaition log completed.{'<<'*30} \n\n")
        



