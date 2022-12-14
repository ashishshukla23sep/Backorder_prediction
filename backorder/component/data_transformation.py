from cgi import test
from sklearn import preprocessing
from backorder.exception import BackOrderException
from backorder.logger import logging
from backorder.entity.config_entity import DataTransformationConfig 
from backorder.entity.artifact_entity import DataIngestionArtifact,\
DataValidationArtifact,DataTransformationArtifact
import sys,os
import numpy as np
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.preprocessing import StandardScaler,OneHotEncoder,LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import pandas as pd
from backorder.constant import *
from backorder.util.util import read_yaml_file,save_object,save_numpy_array_data,load_data




class ManualFeatureEditor(BaseEstimator, TransformerMixin):

    def __init__(self):
        """
        ManualFeatureEditor Initialization
        Replacing -99.0 to np.nan
        and then filling it with median
        """
        try:
            pass
        except Exception as e:
            raise BackOrderException(e, sys) from e

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        try:
            nn = []
            for i in X.columns:
                d = np.array(X[i])
                d[d==-99.0]=np.nan
                nn.append(d)
            genrated_feature = np.c_[nn[0],nn[1]]
            
            return genrated_feature
        except Exception as e:
            raise BackOrderException(e, sys) from e





class DataTransformation:

    def __init__(self, data_transformation_config: DataTransformationConfig,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_artifact: DataValidationArtifact
                 ):
        try:
            logging.info(f"{'>>' * 30}Data Transformation log started.{'<<' * 30} ")
            self.data_transformation_config= data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact

        except Exception as e:
            raise BackOrderException(e,sys) from e

    

    def get_data_transformer_object(self)->ColumnTransformer:
        try:
            schema_file_path = self.data_validation_artifact.schema_file_path

            dataset_schema = read_yaml_file(file_path=schema_file_path)

            numerical_columns = dataset_schema[NUMERICAL_COLUMN_KEY]
            categorical_columns = dataset_schema[CATEGORICAL_COLUMN_KEY]
            replace_99_nan_columns = dataset_schema[REPLACE_99_NAN]
            # target_column = dataset_schema[TARGET_COLUMN_KEY]


            replace_99_nan_pipeline = Pipeline(steps=[('feature_generator', ManualFeatureEditor()),
                                                    ('imputer', SimpleImputer(missing_values=np.nan,strategy="median")),
                                                    ('scaler', StandardScaler())])

            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(missing_values=np.nan,strategy="median")),
                ('scaler', StandardScaler())
            ]
            )

            # target_pipeline = Pipeline(steps=[('label_encoder',LabelEncoder())])

            cat_pipeline = Pipeline(steps=[
                ('impute', SimpleImputer(missing_values=np.nan,strategy="most_frequent")),
                ('one_hot_encoder', OneHotEncoder(drop='first'))
                 
            ]
            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")


            preprocessing = ColumnTransformer([
                # ('target_column',target_pipeline,target_column),
                ('replace_nan',replace_99_nan_pipeline,replace_99_nan_columns),
                ('num_pipeline', num_pipeline, numerical_columns),
                ('cat_pipeline', cat_pipeline, categorical_columns),
            ])
            return preprocessing

        except Exception as e:
            raise BackOrderException(e,sys) from e   


    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info(f"Obtaining preprocessing object.")
            preprocessing_obj = self.get_data_transformer_object()


            logging.info(f"Obtaining training and test file path.")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            

            schema_file_path = self.data_validation_artifact.schema_file_path
            
            logging.info(f"Loading training and test data as pandas dataframe.")
            train_df = load_data(file_path=train_file_path, schema_file_path=schema_file_path)
            test_df = load_data(file_path=test_file_path, schema_file_path=schema_file_path)

            

            schema = read_yaml_file(file_path=schema_file_path)

            target_column_name = schema[TARGET_COLUMN_KEY]


            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe")
            # print('Train_df_shape \n',train_df.shape,'\n',train_df.columns)

            preprocess_data_train = preprocessing_obj.fit_transform(train_df)
            preprocess_data_test = preprocessing_obj.transform(test_df)



            
            

            train_df = pd.DataFrame(preprocess_data_train,columns=schema[REPLACE_99_NAN]+schema[NUMERICAL_COLUMN_KEY]+schema[CATEGORICAL_COLUMN_KEY])
            test_df = pd.DataFrame(preprocess_data_test,columns=test_df.columns)

            

            logging.info(f"Splitting input and target feature from training and testing dataframe.")
            input_feature_train_df = train_df.drop(columns=target_column_name)
            target_feature_train_df = train_df[target_column_name]
        
            input_feature_test_df = test_df.drop(columns=target_column_name)
            target_feature_test_df = test_df[target_column_name]
            

            
            input_feature_train_arr = np.array(input_feature_train_df)
            input_feature_test_arr = np.array(input_feature_test_df)


            train_arr = np.c_[ input_feature_train_arr, np.array(target_feature_train_df)]

            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            
            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            train_file_name = os.path.basename(train_file_path).replace(".csv",".npz")
            test_file_name = os.path.basename(test_file_path).replace(".csv",".npz")

            transformed_train_file_path = os.path.join(transformed_train_dir, train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir, test_file_name)

            logging.info(f"Saving transformed training and testing array.")
            
            save_numpy_array_data(file_path=transformed_train_file_path,array=train_arr)
            save_numpy_array_data(file_path=transformed_test_file_path,array=test_arr)

            preprocessing_obj_file_path = self.data_transformation_config.preprocessed_object_file_path

            logging.info(f"Saving preprocessing object.")
            save_object(file_path=preprocessing_obj_file_path,obj=preprocessing_obj)

            data_transformation_artifact = DataTransformationArtifact(is_transformed=True,
            message="Data transformation successfull.",
            transformed_train_file_path=transformed_train_file_path,
            transformed_test_file_path=transformed_test_file_path,
            preprocessed_object_file_path=preprocessing_obj_file_path

            )
            logging.info(f"Data transformationa artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise BackOrderException(e,sys) from e

    # def __del__(self):
    #     logging.info(f"{'>>'*30}Data Transformation log completed.{'<<'*30} \n\n")
