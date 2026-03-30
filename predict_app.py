from flask import Flask,render_template,request
import pickle
import pandas as pd
from src.Telco_customer_churn.exception import CustomException
import sys

app=Flask(__name__)

model=pickle.load(open("artifacts/model.pkl","rb"))
preprocessor=pickle.load(open("artifacts/preprocessor.pkl","rb"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data=request.form
        input_dict = {
            'gender': data['gender'],
            'SeniorCitizen': int(data['SeniorCitizen']),
            'Partner': data['Partner'],
            'Dependents': data['Dependents'],
            'tenure': int(data['tenure']),
            'PhoneService': data['PhoneService'],
            'MultipleLines': data['MultipleLines'],
            'InternetService': data['InternetService'],
            'OnlineSecurity': data['OnlineSecurity'],
            'OnlineBackup': data['OnlineBackup'],
            'DeviceProtection': data['DeviceProtection'],
            'TechSupport': data['TechSupport'],
            'StreamingTV': data['StreamingTV'],
            'StreamingMovies': data['StreamingMovies'],
            'Contract': data['Contract'],
            'PaperlessBilling': data['PaperlessBilling'],
            'PaymentMethod': data['PaymentMethod'],
            'MonthlyCharges': float(data['MonthlyCharges']),
            'TotalCharges': float(data['TotalCharges'])
        }
        input_df=pd.DataFrame([input_dict])
        transformed=preprocessor.transform(input_df)
        prediction=model.predict(transformed)[0]
        result="Churn" if prediction==1 or prediction=="Yes" else "No Churn"

        return render_template('index.html',prediction_text=result)
    
    except Exception as e:
        raise CustomException(e,sys)

if __name__=="__main__":
   app.run(host="0.0.0.0",port=10000)