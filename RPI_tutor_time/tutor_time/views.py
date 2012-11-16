# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import logout 
from tutor_time.models import Tutee, Tutor, Request
from tutor_time.utility import *
from tutor_time.emails import emails
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db import IntegrityError

def index(request):
    context = RequestContext(request) 
    context.update(csrf(request))
    return render_to_response('index.html', context)

def create_account(request):
    c = {
        'password_error': '',
        'username_error': '',
        'email_error': '',
        'firstname_error': '',
        'lastname_error': ''
    }

    if request.method == 'POST':
        valid = validate_creation(request.POST)
        if valid is not None:
            c.update(valid)
            c.update(csrf(request))
            return render_to_response('create_account.html',
                                      context_instance=RequestContext(request, c))

        try:
            t = create_tutee(request.POST)
        except IntegrityError:
            c['username_error'] = 'Username already Exists'
            return render_to_response('create_account.html',
                                      context_instance=RequestContext(request, c))
        msg = """<br />
            Welcome to Tutor Time! Please click the link to verify your account.<br />
            <a href="http://localhost:8000/verify_account/{0}">Verify the account</a>.<br />
            If you cannot see the link above, please copy and paste the link below<br />
            http://localhost:8000/verify_account/{0}<br />
            """
        #emails().send_email(t.user, msg.format(t.verification_id), "Please verify your account")
        emails().simulate_send(t.user, msg.format(t.verification_id), "Please verify your account")
        c.update(csrf(request))
        c.update({'message': 'Success! Please check your email for activation', 'error': False})
        return render_to_response('display_message.html',
                                  context_instance=RequestContext(request, c))
    else:
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
    c.update(csrf(request))
    if request.method == 'POST':
        fc = request.POST['for_class']
        desc = request.POST['description']
        d = request.POST['day']
        t = request.POST['time']
        helprequest = Request(user=c['user'].username, first_name=c['user'].first_name, last_name=c['user'].last_name, for_class=fc, description=desc, days=d, time=t)
        helprequest.save()
        return render_to_response('request_help.html', c)
    else:
        return render_to_response('request_help.html', c)

@login_required(login_url='/loginerror')
def profile(request):
    c = RequestContext(request)
    c.update(csrf(request))
    
    current_user = Tutee.objects.get(user__username=c['user'].username)
    tutor = False
    if current_user.is_tutor():
        tutor = True

    requests = Request.objects.all()
    pending_requests = []
    my_tutors = []
    if tutor:
        my_tutees = []
    for req in requests:
        if req.user == c['user'].username:
            if not req.accepted_by:
                pending_requests.append(req)
            else:
                my_tutors.append((Tutee.objects.get(user__username=req.accepted_by), req))
        elif tutor and req.accepted_by == c['user'].username:
            my_tutees.append((Tutee.objects.get(user__username=req.user), req))

    c.update(csrf(request))
    c.update({'pending_requests': pending_requests})
    c.update({'my_tutors': my_tutors})
    c.update({'tutor': tutor})
    if tutor:
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
    c = RequestContext(request)
    c.update(csrf(request))
    account = None
    try:
        account = Tutee.objects.get(verification_id=v_id)
    except Tutee.DoesNotExist:
        message = 'Account does not exist'
        error = True
        c.update({'message': message, 'error': error})
        return render_to_response('display_message.html',c)

    if account is None:
        message = 'Account does not exist'
        error = True
        c.update({'message': message, 'error': error})
        return render_to_response('display_message.html',c)

    account.user.is_active = True
    account.user.save()
    message = 'Account successfully activated, you may now log in'
    error = False
    c.update({'message': message, 'error': error})
    return render_to_response('display_message.html',c)
    
@login_required(login_url='/loginerror')
def promote_user(request):
    c = RequestContext(request)
    c.update(csrf(request))
    user = c['user']
    if not user.is_superuser:
        raise Http404

    message = ''
    error = False
    if request.method == 'POST':
        try:
            person = User.objects.get(username=request.POST['tutee'])
            promote_to_tutor(person)
            message = "User was successfully promoted"
        except User.DoesNotExist:
            message = "User not found in the database"
            error = True

    c.update({'message': message, 'error': error})
    all_tutees = [tutee for tutee in get_all_users(user.username) if not tutee.is_tutor()]
    all_tutees = [tutee for tutee in all_tutees if tutee.user.is_active]
    c.update({'tutees': all_tutees})

    return render_to_response('promote_user.html', c)

def loginerror(request):
  c = RequestContext(request)
  c.update(csrf(request))
  c.update({'message': 'Please log in to view the page', 'error': True})
  return render_to_response('display_message.html', c)
