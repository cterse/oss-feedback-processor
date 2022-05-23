from time import process_time_ns
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

def process_tasks(config_dict):
    """
    Processes the tasks in the config file and returns a list of task dictionaries.
    """
    subtasks = get_all_subtasks(config_dict)
    # print(subtasks)
    print(f'Found {len(subtasks)} subtasks.')

def get_all_subtasks(config_dict):
    """
    Returns a list of all subtasks in the config file.
    """
    subtasks = []
    for task in config_dict['tasks'].values():
        if 'subtasks' in task:
            subtasks.extend(task['subtasks'])
            
    return subtasks

config_dict = read_config_file(os.path.join(os.path.dirname(__file__), '..', 'config.yml'))
# print(config_dict)

process_tasks(config_dict)