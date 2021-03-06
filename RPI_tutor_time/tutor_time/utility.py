import re
from tutor_time.models import *
from settings import CAMPUS_EMAIL_ENDING
import uuid
import hashlib
from django.contrib.auth.models import User

def validate_creation(info):
    """
    validate_creation takes a dictionary info and returns a dictionary of error messages
    or None if there were no issues with the data being passed in.
    """

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

    # Make sure email is from the campus email
    if re.match('^[a-z]+[0-9]*@' + CAMPUS_EMAIL_ENDING.replace('.','\\.') + '$', info['email']) is None:
        errors['email_error'] = 'E-mail must be an RPI email'

    if len(errors) != 0:
        return errors

    # No errors
    return None

def validate_help_request(info):
    errors = {}

    if 'for_class' not in info or info['for_class'] == '':
        errors['class_error'] = 'For Class field is empty'
    if 'description' not in info or info['description'] == '':
        errors['description_error'] = 'Description field is empty'
    if 'day' not in info or info['day'] == '':
        errors['day_error'] = 'Day field is empty'
    if 'time' not in info or info['time'] == '':
        errors['time_error'] = 'Time field is empty'

    if len(errors) != 0:
        return errors


def promote_to_tutor(user_obj):
    """
    Given a User object, creates and returns a Tutor
    """
    tutor = Tutor(tutee_ptr=user_obj.get_profile())
    tutor.__dict__.update(user_obj.get_profile().__dict__)
    tutor.save()
    return tutor

def create_tutee(post_data):
    """
    create_tutee takes a dictionary representing post_data to the create_account view
    and creates a User account and a Tutee account for that person. Returns a Tutee object
    on success. Failure can occur on a IntegrityError (Please try/except when calling this function)
    """

    username = post_data['username']
    fname = post_data['fname']
    lname = post_data['lname']
    email = post_data['email']
    password = post_data['password']
    password_confirm = post_data['pwconfirm']

    useracct = User.objects.create_user(username,email,password)
    useracct.first_name = fname
    useracct.last_name = lname
    useracct.is_staff = False
    useracct.is_active = False
    useracct.save()

    t = Tutee(user=useracct)
    t.verification_id = hashlib.sha1(str(uuid.uuid4())).hexdigest()
    t.save()
    return t
