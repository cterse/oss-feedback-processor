# oss-feedback-processor
Just a new line to test pull request comments.

Scripts to extract, process and transfer CSC 517 OSS project submissions' grading feedback from and to appropriate GitHub repositories.

## Input files 🗄️
We will deal with three main input Google Sheets. Multiple instances of each file may be present corresponding to different semesters.
1. OSS & wiki grades ([Fall 21](https://docs.google.com/spreadsheets/d/1BgqowvanfrwYZBZN6kIAZHKlDoUGF_CQKhWyFohBYOE/edit#gid=0), [Spring 22](https://docs.google.com/spreadsheets/d/1qY6wGMAqsA3gnAy2fll6nKq80ghtbUhgT24R2uNSGec/edit#gid=0))
2. Project demo evaluation rubric ([Fall 21](https://docs.google.com/spreadsheets/d/1B-Us7nXdNZbYGH1hQoz7OFXKh_qBXcTu9j2iUqddWlI/edit#gid=886687584), [Spring 22](https://docs.google.com/spreadsheets/d/1jtgJvDGeTDLGNlMC6eO-e-6ZXAQPrafPa5FhDPh4AJ8/edit#gid=370461803))
3. [Comprehensive Expertiza OSS and Final project history](https://docs.google.com/spreadsheets/d/1bUwyvxgWe6hRnUo1FkSz2PdQ6DQELS_VyQ1o8l4L0qM/edit#gid=1868522269)

### Relevant Columns in Input Files
#### OSS & wiki grades
| Column # | Column Name | Relevant? | Remarks |
|--------|--------|--------|--------|
| 1 | PID | ✔️ | Id |
| 2 | Project Name | ✔️ | Id |
| 3 | Email Addresses | | |	
| 4 | Mentor | | |
| 5 | OSS comments | ✔️ | feedback |
| 6 | OSS percentage | | |
| 7 | Wiki comments | ✔️ | feedback |
| 8 | Wiki score | | |
| 9 | Merge? | | |
| 10 | Status | | |	
| 11 | Exceptions | | |
| 12 | Column L | | |
| 13 | Column M | | |
| 14 | Column N | | |
| 15 | Column O | | |
| 16 | Column P | | |
| 17 | Column Q | | |
| 18 | Column R | | |
| 19 | 0 | | |

#### Project demo evaluation rubric
| Column # | Column Name | Relevant? | Remarks |
|--------|--------|--------|--------|
|	1	|	Timestamp	|		|		|
|	2	|	Email address	|		|		|
|	3	|	Column C	|		|		|
|	4	|	Your name	|		|		|
|	5	|	Project number and name	|	✔️ |	Id	|
|	6	|	User-IDs of team members:	|		|		|
|	7	|	List of features covered in the demo, and comments	|		|		|
|	8	|	Should this project be merged?  Why or why not?	|		|		|
|	9	|	Did the project implement the intended functionality?	|		|		|
|	10	|	What is the quality of the code changes in the repo?	|		|		|
|	11	|	How extensive are the tests?	|		|		|
|	12	|	How good is the documentation?	|		|		|
|	13	|	What is the overall value of the project?	|		|		|
|	14	|	Score for project	|		|		|
|	15	|	Average score for project	|		|		|
|	16	|	Project grade	|		|		|
|	17	|	Comments to be returned on project	|	✔️	|	feedback	|
|	18	|	Design-doc grade	|		|		|
|	19	|	Comments on design doc	|	✔️	|	feedback	|
|	20	|	Merge status	|		|		|

#### Comprehensive Expertiza OSS and Final project history
| Column # | Column Name | Relevant? | Remarks |
|--------|--------|--------|--------|
|	1	|	Semester	|		|		|
|	2	|	Project ID	|	✔️ |	Id	|
|	3	|	Project name	|		|		|
|	4	|	User-IDs of team members	|		|		|
|	5	|	Submitted Work	|	yes	|	links	|
|	6	|	Merged?	|		|		|
|	7	|	Slated to possibly be merged	|		|		|
|	8	|	Reuse	|		|		|
|	9	|	Project Grade	|		|		|
|	10	|	Design Document Grade	|		|		|
|	11	|	Feedback on project	|	✔️	|	feedback	|
|	12	|	Semester/team name	|		|		|
|	13	|	Feedback on design doc	|	✔️	|	feedback	|

## System Design 🔌
![system_design](/res/oss_feedback_system_design.png)

## Config File Structure 📜
To minimize code changes when adding or removing jobs, a [config.yml](./config.yml) file has been created that lists all the feedback extraction jobs to be performed. Make sure this config.yml is present in the project root.
Every feedback extraction and transfer task is specifed as a `subtask` in the `tasks` of the config file as follows:
```yaml
---
tasks:
  ...
  [task-name]:
    name: [name of the subtask]
    description: [description of the subtask. OPTIONAL]
    subtasks:
      - name: [name of the subtask]
        path: [local absolute path to xlsx file where feedback is present]
        url: [Google Docs URL of the sheet where feedback is present]
        sheet: [sheet number to be parsed]
        feedback_column_names: [list of columns that contain the feedback to be extracted]
        resource_column_names: [list of columns that contain any extra resources, like links, urls, etc., to be extracted]
        id_column_names: [list of columns that act as the primary keys of the sheet]
        enabled: [true|false process the job or not]
  ...
```

An example of a sheet parsing task in the `config.yaml` is shown below:
```yaml
---
tasks:
  ...
  oss_and_wiki_tasks:
    name: Parse OSS & wiki grades Sheet
    description: Parse OSS & wiki grades Sheet
    subtasks:
      - name: Parse OSS & wiki grades - Spring 22
        path: /Users/chinmay/dev/expertiza/oss-feedback-processor/data/spring-22/oss_and_wiki_grades_spring_2022.xlsx
        url: https://docs.google.com/spreadsheets/d/1qY6wGMAqsA3gnAy2fll6nKq80ghtbUhgT24R2uNSGec/edit#gid=0
        sheet: 0
        feedback_column_names: ['OSS Comments', 'Wiki comments']
        resource_column_names: []
        id_column_names: ["PID", "Project Name"]
        enabled: false
  ...
```
Use of a `config.yaml` file makes the design scalable, as new tasks can be added with ease, without much code changes. 

To add a new parsing task for an already existing sheet type (OSS and Wiki/Comprehensive History/Project Demo Eval): 
* Add a new subtask for the `subtasks` dict under the appropriate `task`

To add a new parsing task for a new sheet type: 
* Create a new task under `tasks`
* Give it a name using the `name` key
* Add the required `subtask`s

## Prerequisites ✅
- [ ] Python 3

## How to Run ⏯️
1. `git clone` this repository.
2. `cd` into the project root.
3. Create and activate a Python [virtual env](https://docs.python.org/3/tutorial/venv.html) (OPTIONAL).
4. Run `pip install -r requirements.txt` to install project dependencies
5. ❗❗ Check the `config.yml` file for correctness in case of of any editions to it. Check that it is present in the project root.
6. Run `python3 src/parse.py`

## Project Structure 🏗️
```bash
oss-feedback-processor
├── README.md   # This file
├── config.yml    # config file containing the feedback extraction tasks    
├── data    # input xlsx sheets dir
│   └── spring-22   # arranged in groups
│       ├── comprehensive_expertiza_OSS_and_final_project_history.xlsx
│       ├── oss_and_wiki_grades_spring_2022.xlsx
│       └── project_demo_evaluation_rubric_spring_2022.xlsx
├── requirements.txt    # Python requirements.txt
├── res   # Resources for the README
│   ├── oss_feedback_system_design.drawio
│   └── oss_feedback_system_design.png
└── src   # main source dir
    └── parse.py    # Main script

4 directories, 9 files
```
