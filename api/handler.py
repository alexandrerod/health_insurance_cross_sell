import pickle
import pandas as pd
from flask import Flask, request, Response
from health.HealthInsurance import HealthInsurance


#load model 


model = pickle.load(open('/home/alexandrerod/Documentos/repos/health_insurance_cross_sell/models/xgb_tunned.pkl', 'rb'))

#start api
app = Flask(__name__)

@app.route('/predict', methods=['POST'])

def health_insurance_predict():
    test_json = request.get_json()

    if test_json:
        if isinstance(test_json,dict):
            test_raw = pd.DataFrame( test_json, index=[0] )
        else:
            test_raw = pd.DataFrame( test_json, columns=test_json[0].keys() )

        #start class
        pipeline = HealthInsurance()

        #cleaning
        df1 = pipeline.cleanind_data(test_raw)

        #feature engineering
        df2 = pipeline.feature_engineering(df1)

        #data preparation
        df3 = pipeline.data_preparation(df2)

        #predict
        df_response = pipeline.get_prediction(model, test_raw, df3)

        return df_response
    else:
        return Response({}, status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run('127.0.0.1')