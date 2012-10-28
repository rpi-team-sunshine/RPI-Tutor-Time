# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from pprint import pprint

def index(request):
    return render_to_response('index.html')

def create_account(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username,email,password)
        user.first_name = fname
        user.last_name = lname
        user.is_staff = False
        user.save()
        return render_to_response('index.html')
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('create_account.html',c)
		
def claim_tutee(request):
    tutee_list = User.objects.all()
    return render_to_response('claim_tutee.html', tutee_list)
