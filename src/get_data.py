# read params
# process
# return data

import os
import argparse
import yaml
import pandas as pd


def read_params(config_path):
    with open(config_path, 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)
        return config

def get_data(config_path):
    # print(config_path)
    config = read_params(config_path)
    data_path = config['data_source']['s3_scource']
    df = pd.read_csv(data_path)
    return df
    

if __name__=='__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    config_path = parsed_args.config
    data = get_data(config_path=config_path)


   
  