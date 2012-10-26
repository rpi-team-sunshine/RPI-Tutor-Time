# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from tutor_time.utility import *

def index(request):
    return render_to_response('index.html')

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
        user = User.objects.create_user(username,email,password)
        user.first_name = fname
        user.last_name = lname
        user.is_staff = False
        user.save()
        return render_to_response('index.html')
    else:
        c.update(csrf(request))
        return render_to_response('create_account.html',
                                  context_instance=RequestContext(request, c))
