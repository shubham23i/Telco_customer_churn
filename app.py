import sys
from src.Telco_customer_churn.logger import logging
from src.Telco_customer_churn.exception import CustomException
from src.Telco_customer_churn.components.data_ingestion import DataIngestion,DataIngestionCnfig
if __name__=='__main__':
    logging.info('hi')
    try:
        #data_ingestion_config=DataIngestionCnfig()
        data_ingestion=DataIngestion()
        data_ingestion.initiatedataingestion()
    except Exception as e:
        raise CustomException(e,sys)