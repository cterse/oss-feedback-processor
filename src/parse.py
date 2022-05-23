import pandas as pd
import yaml
import os

def read_config_file(config_filepath):
    """
    Reads in a config file and returns a dictionary.
    """
    config_dict = {}
    
    with open(config_filepath, 'r') as config_file:
        try:
            config_dict = yaml.full_load(config_file)
        except yaml.YAMLError as exc:
            print(exc)

    return config_dict

config_dict = read_config_file(os.path.join(os.path.dirname(__file__), '..', 'config.yml'))
# print(config_dict)