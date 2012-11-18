from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import logout 
from tutor_time.models import Tutee, Tutor, Request
from tutor_time.utility import *
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db import IntegrityError

# If we're testing by simulating emails (ie no SMTP server avaliable)
try:
  from settings import SIMULATE_EMAIL
except ImportError:
  SIMULATE_EMAIL = False

if SIMULATE_EMAIL:
  from tutor_time.emails import dummy_emails as emails
else:
  from tutor_time.emails import emails

def index(request):
    context = RequestContext(request) 
    context.update(csrf(request))
    return render_to_response('index.html', context)

def create_account(request):
    """
    View responsible for creating an account. If the request coming in is a GET request,
    It will load the template. If the request is a POST it will validate the data, and if
    there is an error, it will return the template with error messages, otherwise it will
    build the account then send a verification email, then it will return a template with
    a success message.
    """

    # Error messages
    c = {
        'password_error': '',
        'username_error': '',
        'email_error': '',
        'firstname_error': '',
        'lastname_error': ''
    }

    if request.method == 'POST':
        # Check if data is ok
        valid = validate_creation(request.POST)

        # If there was a dictionary returned, load the template with the error messages
        if valid is not None:
            c.update(valid)
            c.update(csrf(request))
            return render_to_response('create_account.html',
                                      context_instance=RequestContext(request, c))

        # Otherwise attempt to create an account and if we get an error, render the error message
        try:
            t = create_tutee(request.POST)
        except IntegrityError:
            c['username_error'] = 'Username already Exists'
            return render_to_response('create_account.html',
                                      context_instance=RequestContext(request, c))

        # Account creation a success! Make an email message and send it out!
        msg = """<br />
            Welcome to Tutor Time! Please click the link to verify your account.<br />
            <a href="http://localhost:8000/verify_account/{0}">Verify the account</a>.<br />
            If you cannot see the link above, please copy and paste the link below<br />
            http://localhost:8000/verify_account/{0}<br />
            """
        emails().send_email(t.user, msg.format(t.verification_id), "Please verify your account")
        #emails().simulate_send(t.user, msg.format(t.verification_id), "Please verify your account")

        # Load success page
        c.update(csrf(request))
        c.update({'message': 'Success! Please check your email for activation', 'error': False})
        return render_to_response('display_message.html',
                                  context_instance=RequestContext(request, c))

    # GET request, Return the page to create an account
    c.update(csrf(request))
    return render_to_response('create_account.html',
                              context_instance=RequestContext(request, c))

def logout_view(request):
    logout(request)
    return index(request)


@login_required(login_url='/loginerror')
def claim_tutee(request):
    c = RequestContext(request)
    c.update(csrf(request))
    is_tutor = False
    if tutor(c['user'].username):
        is_tutor = True
        c.update({'tutor': tutor})
    if request.method == 'POST':
        msg = 'Good news, your request has been accepted by ' +\
                c['user'].first_name + " " + c['user'].last_name +\
                ". They should be contacting you directly shortly"
        request_user_and_id = request.POST['choice'].split('?^?')
        requests = Request.objects.all()
        for req in requests:
            if req.user == request_user_and_id[0]:
                if req.id == int(request_user_and_id[1]):
                    req.accepted_by = c['user'].username
                    req.save()
                    usr = Tutee.objects.get(user__username=req.user).user
                    c.update({'target': req.user})
                    emailer = emails()
                    emailer.send_email(usr, msg, "Good News")
                    
        c.update(csrf(request))
        return render_to_response('email_tutee.html', c)
    else:
        c.update(csrf(request))
        tutee_list = Tutee.objects.all()
        requests = Request.objects.all()
        help_requests = []
        for tutee in tutee_list:
            for req in requests:
                if tutee.user.username == req.user and req.user != c['user'].username:
                    if not req.accepted_by:
                        help_requests.append(req)
 
        c.update(csrf(request))
        c.update({'help_requests': help_requests})
        return render_to_response('claim_tutee.html', c)

@login_required(login_url='/loginerror')
def email_tutee(request):
    c = RequestContext(request)
    c.update(csrf(request))
    if request.method == 'POST':
        target = Tutee.objects.get(user__username=request.POST['tutee']).user
        emailer = emails()
        message = request.POST['message']
        emailer.send_email(target, message, "A Message from your Tutor")
        return render_to_response('index.html', c)
    else:
        pass
        
@login_required(login_url='/loginerror')
def request_help(request):
    c = RequestContext(request)
    c.update({
        'class_error': '',
        'description_error': '',
        'day_error': '',
        'time_error': '',
        })
    c.update(csrf(request))
    if request.method == 'POST':
        validate = validate_help_request(request.POST)
        if validate is not None:
            c.update(validate)
            c.update(csrf(request))
            return render_to_response('request_help.html', c)

        fc = request.POST['for_class']
        desc = request.POST['description']
        d = request.POST['day']
        t = request.POST['time']
        users_requests = Request.objects.filter(user=c['user'].username)
        valid = False
        if len(users_requests) < 11:
            for req in users_requests:
                if req.for_class == fc:
                    c.update({'request_exists_error': 'A help request for this class already exists'})
                    valid = False
                else:
                    valid = True
        elif len(users_requests) > 10:
            c.update({'too_many_error': 'You have too many open requests'})

        if valid:
            helprequest = Request(user=c['user'].username, first_name=c['user'].first_name, last_name=c['user'].last_name, for_class=fc, description=desc, days=d, time=t)
            if c['user'].first_name != '' and c['user'].last_name != '':
                specific_request = True
                helprequest.requested = c['username']
                c.update({'specific_request': specific_request})
                target = Tutee.objects.get(user__username=c['username']).user
                emailer = emails()
                message = 'You have been requested as a tutor by ' +\
                          c['user'].first_name + ' ' + c['user'].last_name +\
                          '.  Log in to RPI Tutor Time to view their request.'
                emailer.send_email(target, message, 'Tutor Request')
            helprequest.save()

        return render_to_response('request_help.html', c)
    else:
        if c['user'].first_name != '' and c['user'].last_name != '':
            specific_request = True
        return render_to_response('request_help.html', c)

@login_required(login_url='/loginerror')
def profile(request):
    c = RequestContext(request)
    c.update(csrf(request))

    if c['user'].is_superuser:
      return redirect('/promote_user/', permanant=True)
    
    is_tutor = False
    if tutor(c['user'].username):
        is_tutor = True

    requests = Request.objects.all()
    pending_requests = []
    my_tutors = []
    if is_tutor:
        my_tutees = []
    for req in requests:
        if req.user == c['user'].username:
            if not req.accepted_by:
                pending_requests.append(req)
            else:
                my_tutors.append((Tutee.objects.get(user__username=req.accepted_by), req))
        elif is_tutor and req.accepted_by == c['user'].username:
            my_tutees.append((Tutee.objects.get(user__username=req.user), req))

    c.update(csrf(request))
    c.update({'pending_requests': pending_requests})
    c.update({'my_tutors': my_tutors})
    c.update({'tutor': is_tutor})
    if is_tutor:
        c.update({'my_tutees': my_tutees})
    return render_to_response('profile.html', c)

@login_required(login_url='/loginerror')
def lookup(request):
    c = RequestContext(request)
    c.update(csrf(request))
    tutor_list = get_all_tutors(c['user'].username)

    is_tutor = False
    if tutor(c['user'].username):
        is_tutor = True
        tutee_list = get_all_users(c['user'].username)
        c.update({'tutee_list': tutee_list})

    if request.method == 'POST':
        tutor_name = request.POST['choice'].split('^?^')
        return render_to_response('request_help.html', { 'firstname': tutor_name[0], 'lastname': tutor_name[1], 'username': tutor_name[2] })

    c.update({'tutor': is_tutor})
    c.update({'tutor_list': tutor_list})
    return render_to_response('lookup.html', c)

def get_all_users(current_user):
    '''gets the tutee object for everyone except the current user'''
    everyone = Tutee.objects.exclude(user__username=current_user)
    return everyone

def get_all_tutors(current_user):
    '''get all the tutors except current user'''
    everyone = get_all_users(current_user)
    tutor_list = []
    for person in everyone:
        if person.is_tutor():
            tutor_list.append(person)
    return tutor_list

def tutor(current_user):
    cu = Tutee.objects.get(user__username=current_user)
    if cu.is_tutor():
        return True
    else:
        return False

def verify_account(request, v_id):
    """
    verify_account takes a request and an v_id which is grabbed from the url.
    The view will try to compare the id with the one stored for that user, and if
    they equal, it will set the user to be active. Otherwise it will result in an error.
    """
    c = RequestContext(request)
    c.update(csrf(request))
    account = None
    
    # Find the user who has the id and if they do not exist, render an error message
    try:
        account = Tutee.objects.get(verification_id=v_id)
    except Tutee.DoesNotExist:
        message = 'Account does not exist'
        error = True
        c.update({'message': message, 'error': error})
        return render_to_response('display_message.html',c)

    # If somehow the DB returns None, also render an error page
    if account is None:
        message = 'Account does not exist'
        error = True
        c.update({'message': message, 'error': error})
        return render_to_response('display_message.html',c)

    # Otherwise set user to be active and render a success message
    account.user.is_active = True
    account.user.save()
    message = 'Account successfully activated, you may now log in'
    error = False
    c.update({'message': message, 'error': error})
    return render_to_response('display_message.html',c)
    
@login_required(login_url='/loginerror')
def promote_user(request):
    """
    promote_user is a view for just the superuser(s). It renders a page with a dropdown list
    of tutees and the superuser can promote them to a tutor.
    """
    c = RequestContext(request)
    c.update(csrf(request))
    user = c['user']
    if not user.is_superuser:
        raise Http404

    message = ''
    error = False

    # On POST request promote the tutee being passed in.
    if request.method == 'POST':
        try:
            person = User.objects.get(username=request.POST['tutee'])
            promote_to_tutor(person)
            message = "User was successfully promoted"
        except User.DoesNotExist:
            message = "User not found in the database"
            error = True

    # Load the page with optional messages
    c.update({'message': message, 'error': error})

    # Grab all tutees who are active and not a tutor already
    all_tutees = [tutee for tutee in get_all_users(user.username) if not tutee.is_tutor()]
    print all_tutees
    all_tutees = [tutee for tutee in all_tutees if tutee.user.is_active]
    print all_tutees
    c.update({'tutees': all_tutees})

    return render_to_response('promote_user.html', c)

def loginerror(request):
    """
    Loads a message requesting a user log in. This is displayed when
    a user attempts to go somewhere without being logged in when they
    should be.
    """
    c = RequestContext(request)
    c.update(csrf(request))
    c.update({'message': 'Please log in to view the page', 'error': True})
    return render_to_response('display_message.html', c)
