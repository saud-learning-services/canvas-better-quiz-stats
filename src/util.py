from termcolor import cprint
import sys
from canvasapi import Canvas
import settings

def print_error(msg):
    '''
    Prints error without shutting down
    Parameters:
        msg (string): Error message to print
    Returns:
        None
    '''
    cprint(f'\n{msg}\n', 'red')


def shut_down(msg):
    ''' 
    Shuts down the script.
    Parameters:
        msg (string): Message to print before printing 'Shutting down...' and exiting the script.
    Returns:
        None
    '''
    cprint(f'\n{msg}\n', 'red')
    print('Shutting down...')
    sys.exit()

def print_success(msg):
    '''
    Prints success message
    Parameters:
        msg (string): Success message to print
    Returns:
        None
    '''
    cprint(f'\n{msg}\n', 'green')

def print_action(msg):
    '''
    Prints a message that requires the user to do something
    Parameters:
        msg (string): Action message to print
    Returns:
        None
    '''
    cprint(f'\n{msg}\n', 'blue')

def continue_quit(in_msg, move_on=False):
    '''
    Prints a message that requires the user to confirm to move forward or quit
    Parameters:
        msg (string): Action message to print
    Returns:
        True (boolean): only when selection == "Y", otherwise no action or sys.exit()
    '''
    if move_on:
        options = f'\nY - yes, continue\nN - no, continue\nAny other key - exit'
    else:
        options = f'\nY - confirmed, continue\nN - not confirmed, continue\nAny other key - exit'

    while True:
        print(f'{in_msg}{options}')
        selection = input('Enter Y/N: ').strip().upper()

        if selection == "Y":
            return True
        elif selection == "N":
            if move_on:
                break
            else:
                return (False)
                selection
        else:
            shut_down("Shut down selected. Ending process.")


def get_user_inputs(canvas):
    """Prompt user for required inputs. Queries Canvas API throughout to check for
    access and validity errors. Errors stop execution and print to screen.
    Returns:
        Dictionary containing inputs
    """

    # get user object
    try:
        user = canvas.get_user('self')
        cprint(f'\nHello, {user.name}!', 'green')
    except Exception:
        shut_down(
            """
            ERROR: could not get user from server.
            Please ensure token is correct and valid and ensure using the correct instance url.
            """
        )

    # get course object
    try:
        course_id = input('Course ID: ')
        print(course_id)
        course = canvas.get_course(course_id)
    
    except Exception as e:
        print(e)
        shut_down(
            f'ERROR: Course not found [ID: {course_id}]. Please check course number. {e}')


    try:
        quiz_id = input('Quiz ID: ')
        print(quiz_id)
        quiz = course.get_quiz(quiz_id)
    except Exception as e:
        shut_down(
            f'ERROR: Quiz not found [ID: {quiz_id}]')

    # prompt user for confirmation
    _prompt_for_confirmation(course.name, quiz.title)

    settings.course = course
    settings.quiz = quiz

    return()


def _prompt_for_confirmation(course_name, quiz_name):
    """Prints user inputs to screen and asks user to confirm. Shuts down if user inputs
    anything other than 'Y' or 'y'. Returns otherwise.
    Args:
        user_name (string): name of user (aka. holder of token)
        course_name (string): name of course returned from Canvas
    Returns:
        None -- returns only if user confirms
    """
    cprint('\nConfirmation:', 'blue')
    print(f'COURSE:  {course_name}')
    print(f'QUIZ:  {quiz_name}')
    print('\n')

    confirm = input(
    'Would you like to continue using the above information? [y/n]: \n')

    if confirm == 'y' or confirm == 'Y':
        return
    elif confirm == 'n' or confirm == 'N':
        shut_down('Exiting...')
    else:
        shut_down('ERROR: Only accepted values are y and n')        