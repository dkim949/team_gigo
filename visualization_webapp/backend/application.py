import pandas as pd

from flask import Flask
from flask import request, jsonify
from flask_cors import CORS

import joblib

# create an app and load the model
app = Flask(__name__)
CORS(app)
model = joblib.load('model_forest.pkl')
scaler = joblib.load('scaler.pkl')

columns = ['dist_park',
           'retail_450',
           'retail_area',
           'dist_station',
           'residential_450',
           'idw_atvc_mean',
           'food_1000',
           'food_800',
           'idw_aadt_mean',
           'residential_area',
           'dist_school',
           'food_400',
           'office_450',
           'food_100']

@app.route('/predict', methods=['GET'])
def predict():
    try:

        # get request parameters
        query_parameters = request.args
        # convert the query parameters into a Python dictionary
        query_dict = dict(query_parameters)
        app.logger.info(query_parameters)
        # convert the dictionary into a pandas DataFrame
        df_input = pd.DataFrame([query_dict])

        df_input = df_input.loc[:,columns].astype(float)
        df_input = scaler.transform(df_input)
        df_input = pd.DataFrame(df_input, columns=columns)
        prediction = list(model.predict_proba(df_input))[0][1]
        
        return jsonify({'prediction': float(prediction)})
    except Exception as e:
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    app.run(debug=True)