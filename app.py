import sys
from src.Telco_customer_churn.logger import logging
from src.Telco_customer_churn.exception import CustomException
from src.Telco_customer_churn.components.data_ingestion import DataIngestion,DataIngestionCnfig
from src.Telco_customer_churn.components.data_transformation import DataTransform,DataTransformConfig
from src.Telco_customer_churn.components.model_trainer import ModelTrainerConfig,ModelTrainer
if __name__=='__main__':
    logging.info('hi')
    try:
        #data_ingestion_config=DataIngestionCnfig()
        data_ingestion=DataIngestion()
        train_data_path,test_data_path=data_ingestion.initiatedataingestion()

        data_transform=DataTransform()
        data_transform_config=DataTransformConfig()
        train_array,test_array,_=data_transform.Initiate_data_transformation(train_data_path,test_data_path)

        Model_trainer=ModelTrainer()
        print(Model_trainer.InitiateModelTrainer(train_array,test_array))
    except Exception as e:
        raise CustomException(e,sys)