from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
import hashlib
import urllib
import datetime


# Create your views here.

#decorator for authenticating the user is logged in or not
def loginRequired(func):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated():
            return redirect('login_view')
        return func(request,*args,**kwargs)
    return wrapper


#route for login the user
def index(request):
    return render(request,'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username,password = password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('codehub')
            else:
                print 'The password is valid,but the account has been disabled'
        else:
            print 'Invalid username or password'
            return HttpResponse('Invalid username or password')
    return render(request,'auth/login.html')



#route for registering the user
def register_view(request):
    if request.method == 'POST':
       fname = request.POST['fname']
       lname = request.POST['lname']
       username = request.POST['username']
       email = request.POST['email']
       password = request.POST['password']
       User.objects.create_user(first_name = fname,last_name = lname,username = username,email = email,password = password)
       return HttpResponse('Successfully registered');
    return render(request,'auth/register.html')



@loginRequired
def logout_view(request):
    logout(request)
    return redirect('/auth/login')
