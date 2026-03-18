import sys
from src.Telco_customer_churn.logger import logging
from src.Telco_customer_churn.exception import CustomException
if __name__=='__main__':
    logging.info('hi')
    try:
        a=10/0
    except Exception as e:
        raise CustomException(e,sys)