# oss-feedback-processor
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
| 1 | PID | | |
| 2 | Project Name | | |
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
|	5	|	Project number and name	|		|		|
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
|	2	|	Project ID	|		|		|
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
