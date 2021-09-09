# load the train and test
# train algo
# save the metrices


import os
import pandas as pd
import argparse
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import  StandardScaler
import numpy as np
from sklearn.model_selection import train_test_split
from get_data import read_params
import joblib
import json


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2
# check null value
def check_null_value_and_replace(data): 
    df = data
    if df.isnull().sum().any():
        
        for col in df.columns:
            if df[col].isnull().sum():
                df[col] = df[col].fillna(df[col].mean())
                # print(df[col].isnull().sum())

def train_and_evaluate(config_path):
    config = read_params(config_path)
    test_data_path = config['split_data']['test_path']
    train_data_path = config['split_data']['train_path']
    model_dir = config['model_dir']
    split_ratio = config['split_data']['test_size']
    random_state = config['base']['random_state']
    target = [config['base']["target_col"]]
    
    

    train = pd.read_csv(train_data_path, sep=",")
    test = pd.read_csv(test_data_path, sep=",")
    train = train.drop(['Serial_No.'], axis=1)
    test = test.drop(['Serial_No.'], axis=1)

    check_null_value_and_replace(train)
    check_null_value_and_replace(test)

    train_x =  train.drop(target, axis=1)
    test_x = test.drop(target, axis=1)

    train_y =  train[target]
    test_y = test[target]
    
    # EDA
    scaler = StandardScaler()
    train_x = scaler.fit_transform(train_x)
    test_x = scaler.transform(test_x)

    lr = LinearRegression()
    lr.fit(train_x, train_y)
    prediction = lr.predict(test_x)

    (rmse, mae, r2) = eval_metrics(test_y, prediction)
    print("LinearRegression model")
    print("  RMSE: %s" % rmse)
    print("  MAE: %s" % mae)
    print("  R2: %s" % r2)
    score_file = config['reports']["scores"]
    with open(score_file, 'w') as f:
        scores = {
            "rmse": rmse,
            "mae": mae,
            "r2": r2
        }
        json.dump(scores, f, indent=4)

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.joblib")
    joblib.dump(lr, model_path)
    scaler_path = os.path.join(model_dir, "scaler.joblib")
    joblib.dump(scaler, scaler_path)

   

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    config_path = parsed_args.config
    train_and_evaluate(config_path=config_path)
    