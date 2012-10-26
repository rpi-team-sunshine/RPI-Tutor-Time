import re

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
