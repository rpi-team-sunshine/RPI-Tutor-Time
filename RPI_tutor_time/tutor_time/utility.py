import re
from tutor_time.models import *

def validate_creation(username, password, pwconfirm, email):
    errors = {}

    # Make sure passwords are the same
    if password != pwconfirm:
        errors['password_error'] = 'Passwords do not match'

    # Make sure password is at least 6 characters
    if len(password) < 6:
        errors['password_error'] = 'Password is too short'

    # Make sure username is good
    if re.match('^[a-z]+[0-9]*$',username) is None:
        errors['username_error'] = 'Username must be lowercase a-z followed by optional digits'

    # Make sure email is from rpi (eventually change to campus .edu email)
    if re.match('^[a-z]+[0-9]*@rpi\.edu$', email) is None:
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
