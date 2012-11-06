# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import logout 
from tutor_time.models import Tutee, Tutor, Request
from tutor_time.utility import *

def index(request):
    context = RequestContext(request) 
    context.update(csrf(request))
    return render_to_response('index.html', context)

def create_account(request):
    c = {
        'password_error': '',
        'username_error': '',
        'email_error': ''
    }

    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['pwconfirm']
        valid = validate_creation(username, password, password_confirm, email)
        if valid is not None:
            c.update(valid)
            c.update(csrf(request))
            return render_to_response('create_account.html',
                                      context_instance=RequestContext(request, c))
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


def claim_tutee(request):
    c = RequestContext(request)
    c.update(csrf(request))
    if request.method == 'POST':
        request_user_and_id = request.POST['choice'].split('?^?')
        requests = Request.objects.all()
        for req in requests:
            if req.user == request_user_and_id[0]:
                if req.id == int(request_user_and_id[1]):
                    req.accepted_by = c['user'].username
                    req.save()
        c.update(csrf(request))
        return render_to_response('claim_tutee.html', c)
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


def request_help(request):
    c = RequestContext(request)
    if request.method == 'POST':
        fc = request.POST['for_class']
        desc = request.POST['description']
        d = request.POST['day']
        t = request.POST['time']
        helprequest = Request(user=c['user'].username, first_name=c['user'].first_name, last_name=c['user'].last_name, for_class=fc, description=desc, days=d, time=t)
        helprequest.save()
        return render_to_response('request_help.html', c)
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('request_help.html', c)

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

























