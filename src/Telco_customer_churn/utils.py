import os
import sys
import pymysql
import pandas as pd
from src.Telco_customer_churn.logger import logging
from src.Telco_customer_churn.exception import CustomException
from dotenv import load_dotenv

load_dotenv()
host = os.getenv('host')
user = os.getenv('user')
password = os.getenv('password')
database = os.getenv('database')


def read_sql_data():
    try:
        mydb=pymysql.connect(
            host=host,
            user=user,
            passwd=password,
            database=database
        )
        logging.info('connection established', mydb)
        df=pd.read_sql_query('select * from telco_customer',mydb)
    except Exception as e:
        raise CustomException(e,sys)