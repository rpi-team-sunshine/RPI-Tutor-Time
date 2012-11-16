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

        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['pwconfirm']

        useracct = User.objects.create_user(username,email,password)
        useracct.first_name = fname
        useracct.last_name = lname
        useracct.is_staff = False
        useracct.save()

        t = Tutee(user=useracct)
        t.save()
        c.update(csrf(request))
        return render_to_response('index.html',
                                  context_instance=RequestContext(request, c))
    else:
        c.update(csrf(request))
        return render_to_response('create_account.html',
                                  context_instance=RequestContext(request, c))

def logout_view(request):
    logout(request)
    return index(request)


@login_required(login_url='/')
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

@login_required(login_url='/')
def email_tutee(request):
    c = RequestContext(request)
    c.update(csrf(request))
    if request.method == 'POST':
        print request.POST
        target = Tutee.objects.get(user__username=request.POST['tutee']).user
        emailer = emails()
        message = request.POST['message']
        emailer.send_email(target, message, "A Message from your Tutor")
        return render_to_response('index.html', c)
    else:
        pass
        
@login_required(login_url='/')
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
            helprequest.save()
            if c['firstname'] != '' and c['lastname'] != '':
                specific_request = True
                c.update({'specific_request': specific_request})
                target = Tutee.obgects.get(user__first_name=c['firstname'], user__last_name=c['lastname']).user
                emailer = emails()
                message = 'You have been requested as a tutor by ' +\
                          c['user'].first_name + ' ' + c['user'].last_name +\
                          '.  Log in to RPI Tutor Time to view their request.'
                emailer.send_email(target, message, 'Tutor Request')

        return render_to_response('request_help.html', c)
    else:
        return render_to_response('request_help.html', c)

@login_required(login_url='/')
def profile(request):
    c = RequestContext(request)
    c.update(csrf(request))
    
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

@login_required(login_url='/')
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
        return render_to_response('request_help.html', { 'firstname': tutor_name[0], 'lastname': tutor_name[1] })

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
