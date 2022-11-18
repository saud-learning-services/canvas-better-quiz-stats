from canvasapi import Canvas
import util
import sys
import settings
import itertools
import pandas as pd
import pprint
from pathlib import Path
from yaspin import yaspin

def create_instance(API_URL, API_KEY):
    try:
        canvas = Canvas(API_URL, API_KEY)
        util.print_success("Token Valid: {}".format(str(canvas.get_user('self'))))
        return(canvas)
    except Exception as e:
        util.print_error("\nInvalid Token: {}\n{}".format(API_KEY, str(e)))
        sys.exit(1)
        #raise

def _get_course(canvas_obj, course_id):
    '''
    Get Canvas course using canvas object from canvasapi
    Parameters:
        course (Canvas): canvasapi instance
        course_id (int): Canvas course ID
    Returns:
        canvasapi.course.Course object
    '''
    try:
        course = canvas_obj.get_course(course_id)
        util.print_success(f'Entered id: {course_id}, Course: {course.name}.')
    except Exception:
        util.shut_down(f'ERROR: Could not find course [ID: {course_id}]. Please check course id.')

    return course

def create_dict_from_object(theobj, list_of_attributes):
    """given an object and list of attributes return a dictionary
    Args:
        theobj (a Canvas object)
        list_of_attributes (list of strings)
    Returns:
        mydict
    """

    def get_attribute_if_available(theobj, attrname):
        if hasattr(theobj, attrname):
            return {attrname: getattr(theobj, attrname)}
        else:
            return {attrname: None}

    mydict = {}
    for i in list_of_attributes:
        mydict.update(get_attribute_if_available(theobj, i))
    return mydict


def create_folder(folder_path):
    Path(folder_path).mkdir(parents=True, exist_ok=True)
    return(f'creating {folder_path}')

def _create_sub_dict_from_id_list(og_dict, dict_key_prefix, list_key_prefix, list_keys_no_prefix):
    
    new_dict = {}
    
    if list_keys_no_prefix:
    
        for i in list_keys_no_prefix:

            new_dict.update({
                f'{i}': og_dict.get(i)
            })
    
    if list_key_prefix:   
        for i in list_key_prefix:

            new_dict.update({
                f'{dict_key_prefix}_{i}': og_dict.get(i)
            })
        
    return(new_dict)

def create_quiz_question_df(quiz):
    
    quiz_questions = quiz.get_questions()
    quiz_question_attrs = ['id', 'quiz_id', 'question_name', 'question_type', 'question_text', 'variables', 'answers']
    quiz_question_list = [create_dict_from_object(i, quiz_question_attrs) for i in quiz_questions]
    
    df = pd.DataFrame(quiz_question_list)
    df = df.rename({"id": "question_id",
                        "question_name": "question_name_tagged",
                        "question_text": "question_text_original"}, axis=1)
    return(df)

def create_quiz_submission_df(quiz):
    quiz_submissions = quiz.get_submissions()

    quiz_submissions_and_questions_list = []
    quiz_submissions_attrs = ['id', 'quiz_id', 'quiz_version', 'user_id','submission_id', 'attempt']
    
    print("Getting Quiz Submission Questions")
    for ind, i in enumerate(quiz_submissions):
        
        with yaspin(text=f"{ind}: {i}") as spinner:

            quiz_submission_dict = create_dict_from_object(i, quiz_submissions_attrs)
            quiz_submission_questions = i.get_submission_questions()

            for j in quiz_submission_questions:

                qsq_dict = create_dict_from_object(j, ['id', 'quiz_id',
                                                      'position', 'question_name', 'variables', 'attempt', 'quiz_submission_id', 'correct'])

                qsq_dict = _create_sub_dict_from_id_list(qsq_dict, 'quiz_submission_question', 
                                                        ['id', 'position', 'question_name', 'variables'],
                                                        ['quiz_id', 'attempt', 'quiz_submission_id','correct'])

                qsq_dict.update(quiz_submission_dict)
                quiz_submissions_and_questions_list.append(qsq_dict)
                
    spinner.ok("✅ Done")
    
    df = pd.DataFrame(quiz_submissions_and_questions_list)
    return(df)
    
def create_quiz_submission_responses_df(course, quiz):
    
    print("Getting Quiz Submission Answers")
    
    quiz_assignment_id = quiz.assignment_id
    assignment = course.get_assignment(quiz_assignment_id)
    assignment_submissions = assignment.get_submissions(include="submission_history")
    
    assignment_submissions_attrs = ['id', 'user_id', 'submission_history']
    
    submission_history_list = []

    for ind, i in enumerate(assignment_submissions):
        
        submission_attempt_dict = create_dict_from_object(i, assignment_submissions_attrs)
        submission_attempt_history = submission_attempt_dict.get("submission_history")
        
        with yaspin(text=f"getting {ind}") as spinner:
            
            for j in submission_attempt_history:
                
                list_keys_no_prefix = ['user_id', 'attempt', 'submission_type']
                list_keys_prefix = ['id']
                submission_attempt_history_dict = _create_sub_dict_from_id_list(j, 'submission_history', list_keys_prefix, list_keys_no_prefix)

                submission_attempt_data = j.get("submission_data")

                if submission_attempt_data:

                    for k in submission_attempt_data:
                        list_keys_prefix = ['correct', 'points', 'text']
                        list_keys_no_prefix = ['question_id']

                        submission_attempt_data_dict = _create_sub_dict_from_id_list(k, 'submission_data', list_keys_prefix, list_keys_no_prefix)
                        submission_attempt_data_dict.update(submission_attempt_history_dict)

                        submission_history_list.append(submission_attempt_data_dict)
    
    spinner.ok("✅ Done")                
    df = pd.DataFrame(submission_history_list)
    return(df)
        