import validators

def process_comprehensive_feedback_df(feedback_df):
    """
    Maps the "Submitted work" column in feedback_df to the pull request present in column cells
    """
    
    feedback_df['submitted work'] = feedback_df['submitted work'].apply(get_pr_url_from_col_value)

    return feedback_df

def get_pr_url_from_col_value(value):
    """
    Returns the pull request URL from the ID value.
    """
    
    if not value:
        return None

    # split id_value over newlines
    try:
        lines = value.split('\n')
        return extract_pull_request_url(lines)
    except Exception as e:
        print(f'Error processing value: {value}')
        print(e)
    
    return None

def extract_pull_request_url(lines):
    """
    Extracts the pull request URL from strings separated by newlines.
    """
    for line in lines:
        if is_github_pr_url(line):
            return line
    return None

def is_github_pr_url(url):
    """
    Returns True if the URL is a GitHub pull request URL.
    """
    return url and validators.url(url) and 'github.com' in url and '/pull/' in url