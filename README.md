
#### First Time

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
   2. run the script and follow prompts in terminal `$ python src/canvas_better_quiz_stats.py`
