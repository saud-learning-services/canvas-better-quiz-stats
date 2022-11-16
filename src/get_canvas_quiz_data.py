from helpers import create_instance
import os
from dotenv import load_dotenv
import settings
from util import get_user_inputs

load_dotenv() 

API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')

def setup():
    settings.init()
    canvas = create_instance(API_URL, API_KEY)
    get_user_inputs(canvas)

    return(canvas)

if __name__ == "__main__":
    
    setup()