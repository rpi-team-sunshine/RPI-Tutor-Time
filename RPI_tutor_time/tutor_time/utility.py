import re
from tutor_time.models import *
from settings import CAMPUS_EMAIL_ENDING

def validate_creation(info):
    errors = {}

    # Check to make sure things are existing
    if 'username' not in info or info['username'] == '':
        errors['username_error'] = 'Username field is empty'
    if 'password' not in info or info['password'] == '':
        errors['password_error'] = 'Password field is empty'
    if 'pwconfirm' not in info or info['pwconfirm'] == '':
        errors['password_error'] = 'Password confirm field is empty'
    if 'email' not in info or info['email'] == '':
        errors['email_error'] = 'Email field is empty'
    if 'fname' not in info or info['fname'] == '':
        errors['firstname_error'] = 'First name field is empty'
    if 'lname' not in info or info['lname'] == '':
        errors['lastname_error'] = 'Last name field is empty'

    if len(errors) != 0:
        return errors

    # Make sure passwords are the same
    if info['password'] != info['pwconfirm']:
        errors['password_error'] = 'Passwords do not match'

    # Make sure password is at least 6 characters
    if len(info['password']) < 6:
        errors['password_error'] = 'Password is too short'

    # Make sure username is good
    if re.match('^[a-z]+[0-9]*$',info['username']) is None:
        errors['username_error'] = 'Username must be lowercase a-z followed by optional digits'

    # Make sure email is from rpi (eventually change to campus .edu email)
    if re.match('^[a-z]+[0-9]*@' + CAMPUS_EMAIL_ENDING.replace('.','\\.') + '$', info['email']) is None:
        errors['email_error'] = 'E-mail must be an RPI email'

    if len(errors) != 0:
        return errors

    # No errors
    return None

def promote_user(user_obj):
    """
    Given a User object, creates and returns a Tutor
    """
    tutor = Tutor(tutee_ptr=user_obj.get_profile())
    tutor.__dict__.update(user_obj.get_profile().__dict__)
    tutor.save()
    return tutor
