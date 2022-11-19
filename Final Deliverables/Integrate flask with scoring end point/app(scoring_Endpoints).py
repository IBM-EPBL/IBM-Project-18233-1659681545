import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle as p
app=Flask(__name__)

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "kmIiSq9J3IdSfiF09LKp5cwYnO_yyp1uIhlmc16UOiGm"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

@app.route('/')
def HOME():
    return render_template('index.html')

@app.route('/Predictions')
def index():
    return render_template('Predictions.html')

@app.route('/predict',methods=['POST'])
def prediction():    
    form_value=request.form.values()    
    data=[]
    for x in form_value:
        data.append(pd.to_numeric(x).astype(float))
      
    features_name=['age','blood_urea','coronary_artery_disease',
                   'anemia','pus_cell','red_blood_cells','diabetes_melitus','peda_edema']
    
    
    payload_scoring = {"input_data": [{"fields": features_name, "values": [data]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/0e3a6faa-9f65-423f-870e-e1ad69727110/predictions?version=2022-11-17', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    prediction=response_scoring.json()
    print(prediction)
    output=prediction['predictions'][0]['values'][0][0]

    
    if(output==0):
        return render_template('Predictions.html' , pred='Oops!! You have Kidney Chronic Disease. So, please concern a Doctor')
    else:
        return render_template('Predictions.html' , pred='you are not affected by Chronic kidney Disease')

if __name__=='__main__':
    app.run(debug=True)


