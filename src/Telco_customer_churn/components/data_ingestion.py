import os
import sys
from src.Telco_customer_churn.logger import logging
from src.Telco_customer_churn.exception import CustomException
from src.Telco_customer_churn.utils import read_sql_data
from dataclasses import dataclass
import pandas as pd
from sklearn.model_selection import train_test_split

@dataclass
class DataIngestionCnfig:
    train_data_path=os.path.join('artifacts','train.csv')
    test_data_path=os.path.join('artifacts','test.csv')
    raw_data_path=os.path.join('artifacts','raw.csv')

class DataIngestion:
    def __init__(self):
        self.ingestionconfig=DataIngestionCnfig()

    def initiatedataingestion(self):
        try:
            df=read_sql_data()
            logging.info('reading mysql database')
            os.makedirs(os.path.dirname(self.ingestionconfig.train_data_path),exist_ok=True)
            df.to_csv(self.ingestionconfig.raw_data_path,header=True)
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
            train_set.to_csv(self.ingestionconfig.train_data_path,header=True)
            test_set.to_csv(self.ingestionconfig.test_data_path,header=True)
            logging.info('data ingestion is completed')
            return(
                self.ingestionconfig.train_data_path,
                self.ingestionconfig.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)