import pandas as pd
import yaml
import os
import requests

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
    all_subtasks = get_all_subtasks(config_dict)
    # print(subtasks)
    print(f'Found {len(all_subtasks)} subtasks.\n')

    subtasks = list(filter(is_enabled, all_subtasks))
    print(f'Processing {len(subtasks)} subtasks.\n')

    for subtask in subtasks:
        process_subtask(subtask)
        print(f'Processed subtask: {subtask["name"]}')
        print('-' * 20)

def is_enabled(subtask):
    """
    Returns True if the subtask is enabled.
    """
    return subtask['enabled'] if subtask and 'enabled' in subtask else True

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
    feedback_df = get_all_feedback(subtask)

    # Write the feedback to a CSV file
    if not feedback_df.empty: write_feedback_to_csv(feedback_df, subtask)

def write_feedback_to_csv(feedback_df, subtask):
    """
    Writes the feedback dataframe to a CSV file.
    """
    try:
        # Create the directory if it doesn't exist
        if not os.path.exists(temp_output_dir):
            os.makedirs(temp_output_dir)
            print(f'Created directory: {temp_output_dir}')

        csv_file_path = os.path.join(temp_output_dir, subtask['name'] + '.csv')
        feedback_df.to_csv(csv_file_path, index=False)
    except Exception as e:
        print(f'Error writing CSV file: {e}')

def get_all_feedback(subtask):
    """
    Returns all feedback to be returned.
    """
    feedback = []
    
    excel_data_df = get_excel_dataframe(subtask['path'])
    if excel_data_df is None or excel_data_df.empty:
        return feedback
    # print(excel_data_df.head())

    # Get ID Column names
    id_col_names = get_id_col_names(subtask)
    if not id_col_names:
        print('No ID columns found.')
        return feedback

    # Check if ID columns exist
    if not all(col in excel_data_df.columns for col in id_col_names):
        print('ID columns not found. Check config file. Exiting.')
        return feedback

    # Get Feedback Column names
    feedback_col_names = get_feedback_col_names(subtask)
    print(f'Feedback column names: {feedback_col_names}')
    if len(feedback_col_names) == 0:
        print('No feedback columns found.')
        return feedback
    
    # check if feedback columns exist
    if not all(col in excel_data_df.columns for col in feedback_col_names):
        print('Feedback columns not found. Incorrect column names? Check config file. Exiting.')
        return feedback

    # Get the feedback
    feedback_df = get_feedback_df(excel_data_df, id_col_names, feedback_col_names)
    # print(f'Feedback dataframe:\n{feedback_df}')

    return feedback_df

def get_feedback_df(excel_data_df, id_col_names, feedback_col_names):
    """
    Returns feedback dataframe from the main excel dataframe.
    """
    feedback_df = excel_data_df[id_col_names + feedback_col_names].copy()
    
    clean_feedback_df(feedback_df, id_col_names)

    return feedback_df

def clean_feedback_df(feedback_df, id_col_names):
    """
    Cleans the feedback dataframe.
    """
    # Remove rows with no ID
    feedback_df.dropna(axis=0, how='all', subset=id_col_names, inplace=True)

    # Replace no feedback with empty string
    feedback_df.fillna('', inplace=True)

    # Strip whitespace from entire dataframe
    for col in feedback_df.columns:
        feedback_df[col] = feedback_df[col].str.strip()

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

def get_id_col_names(subtask):
    """
    Returns a list of ID column names.
    """
    return [col.strip().lower() for col in subtask['id_column_names']] if 'id_column_names' in subtask else []

def get_all_subtasks(config_dict):
    """
    Returns a list of all subtasks in the config file.
    """
    subtasks = []
    for task in config_dict['tasks'].values():
        if 'subtasks' in task:
            subtasks.extend(task['subtasks'])

    return subtasks

def write_comment_to_pr(comment, pr_number):
    """
    Writes a comment to the PR.
    """
    print(f'Writing comment: {comment}')
    
    repo_owner = 'expertiza'
    repo_name = 'expertiza'
    github_token = os.environ['OSS_GITHUBTOKEN']

    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments'

    headers = {
        'Authorization': f'token {github_token}',
        'Content-Type': 'application/json'
    }

    data = {
        'body': comment
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        print(f'Comment ID: {response.json()["id"]}')
        print(f'HTML URL: {response.json()["html_url"]}')

        return response.json()['id']
    except Exception as e:
        print(f'Error writing comment: {e}')

    return -1

config_dict = read_config_file(os.path.join(os.path.dirname(__file__), '..', 'config.yml'))
# print(config_dict)

temp_output_dir = os.path.join(os.path.dirname(__file__), '..', 'temp')

process_tasks(config_dict)