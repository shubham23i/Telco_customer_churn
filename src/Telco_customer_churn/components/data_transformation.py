import os
from src.Telco_customer_churn.logger import logging
from src.Telco_customer_churn.exception import CustomException
from src.Telco_customer_churn.utils import save_object
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np
from dataclasses import dataclass
import sys

@dataclass
class DataTransformConfig:
    preprocess_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransform:
    def __init__(self):
        self.data_transform_config = DataTransformConfig()

    def get_data_transformation_obj(self):
        try:
            num_columns = ['tenure', 'MonthlyCharges', 'TotalCharges']

            cat_columns = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService',
                           'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
                           'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
                           'Contract', 'PaperlessBilling', 'PaymentMethod']

            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('onehotencoder', OneHotEncoder()),
                    ('scaler', StandardScaler(with_mean=False))
                ]
            )

            logging.info(f"categorical columns: {cat_columns}")
            logging.info(f"numerical columns: {num_columns}")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, num_columns),
                    ("cat_pipeline", cat_pipeline, cat_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def Initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("reading the train and test datasets")

            train_df['Churn'] = train_df['Churn'].map({'No': 0, 'Yes': 1})
            test_df['Churn'] = test_df['Churn'].map({'No': 0, 'Yes': 1})

            train_df = train_df.drop(columns=['customerID', 'Unnamed: 0'], errors='ignore')
            test_df = test_df.drop(columns=['customerID', 'Unnamed: 0'], errors='ignore')

            train_df['TotalCharges'] = pd.to_numeric(train_df['TotalCharges'], errors='coerce')
            test_df['TotalCharges'] = pd.to_numeric(test_df['TotalCharges'], errors='coerce')

            preprocessing_obj = self.get_data_transformation_obj()

            target_column_name = "Churn"

            input_features_train_df = train_df.drop(columns=target_column_name)
            target_feature_train_df = train_df[target_column_name]

            input_features_test_df = test_df.drop(columns=target_column_name)
            target_feature_test_df = test_df[target_column_name]

            logging.info('applying preprocessing on training and test datasets')

            input_features_train_arr = preprocessing_obj.fit_transform(input_features_train_df)
            input_features_test_arr = preprocessing_obj.transform(input_features_test_df)

            train_arr = np.c_[input_features_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_features_test_arr, np.array(target_feature_test_df)]

            logging.info(f"saved preprocessing obj")

            save_object(
                file_path=self.data_transform_config.preprocess_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transform_config.preprocess_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)