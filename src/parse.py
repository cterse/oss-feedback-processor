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
    print(subtasks[0])
    print(f'Found {len(subtasks)} subtasks.')

    for subtask in subtasks:
        process_subtask(subtask)

def process_subtask(subtask):
    """
    Processes a subtask.
    """
    print(f'Processing subtask: {subtask["name"]}')

    file_path = subtask['path']

    if not os.path.isfile(file_path):
        print(f'File not found: {file_path}')
        return

    # Get the feedback columns
    feedback = get_all_feedback(subtask)

def get_all_feedback(subtask):
    """
    Returns a all feedback to be returned.
    """
    feedback = []
    
    excel_data_df = pd.read_excel(subtask['path'])
    # print(excel_data_df.head())

    feedback_col_names = get_feedback_col_names(subtask)
    print(f'Feedback column names: {feedback_col_names}')
    if len(feedback_col_names) == 0:
        print('No feedback columns found.')
        return feedback

def get_feedback_col_names(subtask):
    """
    Returns a list of feedback column names.
    """
    return subtask['feedback_column_names'] if 'feedback_column_names' in subtask else []

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