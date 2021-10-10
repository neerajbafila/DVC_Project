import os
from flask.wrappers import Response
import yaml
import joblib
import numpy as np
import json

params_path = "params.yaml"
schema_path = os.path.join("prediction_service", "schema.json")

class NotinRange(Exception):
    """[If user sending value which are not in range as per dataset]

    Args:
        Exception ([type]): [description]
    """
    def __init__(self, message="Given value are not in range"):
        self.message = message
        super().__init__(self.message)


class NotinColumn(Exception):
    """[if user sending request from the
        from tool like postman in that case he might add some exta column]

    Args:
        Exception ([type]): []
    """
    def __init__(self, message="Not in columnn"):
        self.message = message
        super().__init__(self, message)


def read_params(config_path=params_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
        return config

def predict_y(dic_data):
    print(dic_data.values())
    data = np.array([list(dic_data.values())])
    config = read_params(config_path=params_path)
    model_dir_path = config['webapp_model_dir']
    scaler_dir_path = config['webapp_scaler_dir']
    model = joblib.load(model_dir_path)
    scaler = joblib.load(scaler_dir_path)
    scaled_data = scaler.transform(data)
    prediction = model.predict(scaled_data)
    
    """[restricting prediction range between 0 to 100]
    """
    try:
        if 0 <= prediction <=100:
            return prediction
        else:
            raise NotinRange
    except NotinRange:
        return "Unexcepted error occurred"

def get_schema(schema_path= schema_path):
    with open(schema_path) as json_file:
        schema = json.load(json_file)
        return schema

def validate_input(dic_data):
    
    # def validate_cols(col): #for API input
    #     schema = get_schema()
    #     actual_col = schema.keys()
    #     if col not in actual_col:
    #         raise NotinColumn
    def validate_values(col, val):
        schema = get_schema()
        if not (schema[col]["min"] <= float(dic_data[col]) <=schema[col]["max"]):
            raise NotinRange
    for col, val in dic_data.items():
        # validate_cols(col)
        validate_values(col, val)
    return True

def form_response(dic_data):
    if validate_input(dic_data):
        response = predict_y(dic_data)
        return response