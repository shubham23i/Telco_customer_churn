import os
import sys
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import pymysql
import pandas as pd
from src.Telco_customer_churn.logger import logging
from src.Telco_customer_churn.exception import CustomException
from dotenv import load_dotenv
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score

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
        logging.info(f'connection established, {mydb}')
        df = pd.read_sql_query('select * from telco_customer', mydb)
        
        return df
    except Exception as e:
        raise CustomException(e,sys)
    

def save_object(file_path,obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e,sys)


def evaluate_model(X_train, y_train, X_test, y_test, models, params):
    report = {}

    for model_name, model in models.items():
        param = params.get(model_name, {})

        gs = GridSearchCV(
            model,
            param,
            cv=3,
            scoring='f1',
            n_jobs=-1,
            verbose=0
        )

        gs.fit(X_train, y_train)

        best_model = gs.best_estimator_

        y_train_pred = best_model.predict(X_train)
        y_test_pred = best_model.predict(X_test)

        train_f1 = f1_score(y_train, y_train_pred)
        test_f1 = f1_score(y_test, y_test_pred)

        print(f"\nModel: {model_name}")
        print(f"Train F1: {train_f1}")
        print(f"Test F1: {test_f1}")

        report[model_name] = test_f1

    return report