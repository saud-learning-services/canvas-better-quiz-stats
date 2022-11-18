# Canvas Get More Quiz Details
> name: canvas-better-quiz-stats
> runs-with: terminaal
> python >= 3.8
> canvasapi>=2.0.0 (likely built with 3.0)

## Summary
Canvas quiz statistics are unavailable for large courses, and do not display useful information when randomization in questions (either through pick X, or variables) are used. This script creates a number of csv files for a single quiz - including the questions as seen (and responded to) by individual students, as well as the original question information. 

## Input

* Canvas Instance (instance of Canvas being used - ex. https://ubc.instructure.com)
* Canvas API Token (generate through Account => Settings)
* Course ID (last digits of URL when visiting course page)
* Quiz ID

## Output

Creates outputs in folder: `data/course_id/quiz_id`
> - Note: question points possible not included - for grouped questions (i.e. "pick X of Y") the points applied may overwrite original question points

#### `full_joined.csv`
This file is a combination of the three files listed below. 

  
- **quiz_id**: the Canvas quiz id
- **attempt**: the quiz attempt of the individual student
- **user_id**: the Canvas user id of the submission
- **quiz_submission_id**: a Canvas submission id (unique to student and attempt)
- **quiz_submission_question_id**: the question id of the submission (should match the question_id, included as sanity check)
- **question_id**: the Canvas question id
- **quiz_submission_question_question_name**: the submission question name (as seen by the student). Important for "pick X" type questions and/or randomization of order. This will be the question order as seen by the student
- **quiz_submission_question_question_text**: the submission question text as seen by the student
**quiz_submission_question_variables**: the submission question variables (for question specific to student in case of randomization)
- **submission_history_id**: (submission_id) a unique id for the student's submission
**submission_data_correct**: for the student whether the submission is correct (TRUE, FALSE, undefined, and partial)
- **submission_data_points**: the points given to the student's question submission
**submission_data_text**: the text of the student question submission - Canvas also uses text for m/c and other variable inputs, can be joined with "answers"
- **question_name_tagged**: the name of the question as created by the instructor. This is not visible to students
- **question_type**: the question type
**question_text_original**: the original question text (if variables or randomization included)
- **variables**: the original question variables
- **answers**: answers to the original question

#### `question_info.csv`
- the original question information (what the instructor would see when building the assessment

#### `question_submission_info.csv`
- the question information (what the student sees)

#### `student_submission_response_info.csv`
- the submission answers for the student

## Getting Started

#### First Time (do once)

1. Ensure you have [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) installed (Python 3.9 version)
2. Clone **Canvas Better Quiz Stats** repository
3. Import environment (once): `$ conda env create -f environment.yml`
4. Create .env file and include:

```
API_KEY = ''
API_URL = 'https://ubc.instructure.com'
```

#### Every Time

1. Run:
   1. navigate to your directory `$ cd YOUR_PATH/canvas-better-quiz-stats`
   1. activate the environment (see step 3 on first run) `$ conda activate canvas_better_quiz_stats`
   1. update your environment (.env) file with new token as needed
   1. run the script and follow prompts in terminal `$ python src/canvas_better_quiz_stats.py`
