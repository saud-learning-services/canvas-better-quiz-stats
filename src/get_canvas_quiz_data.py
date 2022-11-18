from helpers import create_instance, create_folder, create_quiz_question_df, create_quiz_submission_df, create_quiz_submission_responses_df
import os
from dotenv import load_dotenv
import settings
from util import get_user_inputs

load_dotenv() 

API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')

def main():
    settings.init()
    canvas = create_instance(API_URL, API_KEY)
    get_user_inputs(canvas)


    course = settings.course
    quiz = settings.quiz

    output_folder = f"data/{course.id}/{quiz.id}"
    create_folder(output_folder)

    print("For large courses this may take some time ...")

    quiz_questions_df = create_quiz_question_df(quiz)
    quiz_submission_df = create_quiz_submission_df(quiz)
    quiz_submission_responses = create_quiz_submission_responses_df(course, quiz)

    submission_with_questions = quiz_submission_df.merge(quiz_submission_responses,left_on=["quiz_submission_question_question_id","quiz_submission_question_id", "user_id", "attempt"], right_on=["question_id","submission_history_id", "user_id", "attempt"], how="outer")

    submission_with_questions_and_info = submission_with_questions.merge(quiz_questions_df, how="left", left_on=["question_id", "quiz_id"], right_on=["question_id", "quiz_id"])

    quiz_questions_df.to_csv(f"{output_folder}/question_info.csv")
    quiz_submission_df.to_csv(f"{output_folder}/question_submission_info.csv") 
    quiz_submission_responses.to_csv(f"{output_folder}/student_submission_responses.csv")  
    submission_with_questions_and_info.to_csv(f"{output_folder}/full_joined.csv") 

    print(f"🥳 Complete")

if __name__ == "__main__":
    main()