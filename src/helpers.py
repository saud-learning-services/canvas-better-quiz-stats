from canvasapi import Canvas
import util
import sys

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