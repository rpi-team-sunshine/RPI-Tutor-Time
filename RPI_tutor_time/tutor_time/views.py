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

def request_tutor(request):
    first_name = request.POST['first_name'];	
    last_name = request.POST['last_name'];
    for_class = request.POST['for_class'];
    description = request.POST['description'];

    #Request = Tutee.objects.request_tutor(username,email,password)
    r = Request    
    r.first_name = first_name
    r.last_name = last_name
    r.for_class = for_class
    r.description = description
    r.save()

    return render_to_response('index.html',
                                  context_instance=RequestContext(request, c))

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


def claim_tutee(request):
    tutee_list = Tutee.objects.all()
    return render_to_response('claim_tutee.html', {'tutee_list': tutee_list})




