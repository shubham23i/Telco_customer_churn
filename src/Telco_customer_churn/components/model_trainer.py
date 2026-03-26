from src.Telco_customer_churn.exception import CustomException
from src.Telco_customer_churn.logger import logging
from src.Telco_customer_churn.utils import save_object,evaluate_model
from dataclasses import dataclass
import os
import sys
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.modeltrainerconfig=ModelTrainerConfig()

    def InitiateModelTrainer(self,train_array,test_array):
        try:
            logging.info("splitting training and test input data")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            models = {
                "Logistic Regression": LogisticRegression(),
                "KNN": KNeighborsClassifier(),
                "Decision Tree": DecisionTreeClassifier(),
                "Random Forest": RandomForestClassifier(),
                "AdaBoost": AdaBoostClassifier(),
                "SVM": SVC(probability=True),
                "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
                "CatBoost": CatBoostClassifier(verbose=False)
            }
            params = {
                "Decision Tree": {
                    'criterion': ['gini', 'entropy'],
                    'max_depth': [5, 10, 20],
                    'min_samples_split': [5, 10, 20],
                    'min_samples_leaf': [2, 5, 10],
                    'class_weight': ['balanced']
                },

                "Random Forest": {
                    'n_estimators': [200, 300, 500],
                    'max_depth': [10, 20, None],
                    'min_samples_split': [5, 10],
                    'min_samples_leaf': [2, 4],
                    'max_features': ['sqrt'],
                    'class_weight': ['balanced']
                },

                "Logistic Regression": {
                    'penalty': ['l2'],
                    'C': [0.1, 1, 10],
                    'solver': ['liblinear'],
                    'class_weight': ['balanced']
                },

                "AdaBoost": {
                    'n_estimators': [100, 200, 300],
                    'learning_rate': [0.05, 0.1, 0.5]
                },

                "KNN": {
                    'n_neighbors': [5, 7, 11, 15],
                    'weights': ['distance'],
                    'metric': ['manhattan']
                },

                "SVM": {
                    'C': [1, 10],
                    'kernel': ['rbf'],
                    'gamma': ['scale'],
                    'class_weight': ['balanced']
                },

                "XGBoost": {
                    'n_estimators': [200, 300],
                    'learning_rate': [0.05, 0.1],
                    'max_depth': [4, 6],
                    'subsample': [0.8],
                    'colsample_bytree': [0.8],
                    'scale_pos_weight': [2, 3]
                },

                "CatBoost": {
                    'iterations': [200, 300],
                    'learning_rate': [0.05, 0.1],
                    'depth': [4, 6],
                    'l2_leaf_reg': [3, 5]
                }
            }
            model_report:dict=evaluate_model(X_train,y_train,X_test,y_test,models,params)
            print(model_report)

            best_model_name = max(model_report, key=model_report.get)
            best_model_score = model_report[best_model_name]

            best_model = models[best_model_name]
            best_model.fit(X_train, y_train)
            if best_model_score<0.55:
                raise Exception('no best model found')
            logging.info('best model in both training and test dataset')
            save_object(
                file_path=self.modeltrainerconfig.trained_model_file_path,
                obj=best_model
            )

            return best_model_score,best_model_name
        except Exception as e:
            raise CustomException(e,sys)