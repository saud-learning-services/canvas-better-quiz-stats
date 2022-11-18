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

### `full_joined.csv`
- combination of the three files below
  
### `question_info.csv`
- the original question information (what the instructor would see when building the assessment

### `question_submission_info.csv`
- the question information (what the student sees)

### `student_submission_response_info.csv`
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
   1. update your environment (.env) file with new token
   1. run the script and follow prompts in terminal `$ python src/canvas_better_quiz_stats.py`
