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
    print(f'Found {len(subtasks)} subtasks.\n\n')

    for subtask in subtasks:
        process_subtask(subtask)
        print(f'Processed subtask: {subtask["name"]}')
        print('-' * 20)

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
    
    excel_data_df = get_excel_dataframe(subtask['path'])
    if excel_data_df is None or excel_data_df.empty:
        return feedback
    # print(excel_data_df.head())

    feedback_col_names = get_feedback_col_names(subtask)
    print(f'Feedback column names: {feedback_col_names}')
    if len(feedback_col_names) == 0:
        print('No feedback columns found.')
        return feedback
    
    # check if feedback columns exist
    if not all(col in excel_data_df.columns for col in feedback_col_names):
        print('Feedback columns not found. Incorrect column names? Check config file. Exiting.')
        return feedback

    # for index, row in excel_data_df.iterrows():
    #     feedback_row = {}
    #     for col_name in feedback_col_names:
    #         feedback_row[col_name] = row[col_name]
    #     feedback.append(feedback_row)
    
    # print(f'Found {len(feedback)} feedback.')
    # return feedback

def get_excel_dataframe(file_path):
    """
    Returns a dataframe from an excel file, after converting the column names to lowercase.
    """
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.lower()

    return df

def get_feedback_col_names(subtask):
    """
    Returns a list of feedback column names.
    """
    return [col.strip().lower() for col in subtask['feedback_column_names']] if 'feedback_column_names' in subtask else []

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