from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import hashlib
import urllib
import datetime

from .models import UserProfileModel
# Create your views here.

#decorator for authenticating the user is logged in or not
def loginRequired(func):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated():
            return redirect('login_view')
        return func(request,*args,**kwargs)
    return wrapper



def check_if_user_profile_exists(func):
    def wrapper(request,*args,**kwargs):
        try:
            user_profile = UserProfileModel.objects.get(user_id = request.user.id)
        except:
            return redirect('/users/profile/'+str(request.user.id)+'/edit')
        return func(request,*args,**kwargs)
    return wrapper



#route for login the user
@loginRequired
@check_if_user_profile_exists
def index(request):
    return render(request,'index.html')


def about_view(request):
    return render(request,'auth/about.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username,password = password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('/')
            else:
                # print 'The password is valid,but the account has been disabled'
                messages.warning(request,'The password is valid,but the account has been disabled')
                return redirect('/auth/login')
        else:
            messages.warning(request,'Invalid username or password')
            return redirect('/auth/login')
    return render(request,'auth/login.html')



#route for registering the user
def register_view(request):
    if request.method == 'POST':
       fname = request.POST['fname']
       lname = request.POST['lname']
       username = request.POST['username']
       email = request.POST['email']
       password = request.POST['password']
       try:
           User.objects.get(username = username)
           messages.warning(request,'Username already exists')
           return redirect('/auth/register')
       except:
           user = User.objects.create_user(first_name = fname,last_name = lname,username = username,email = email,password = password)
           new_user_profile = UserProfileModel(user = user)
           new_user_profile.save()
           messages.success(request,'Successfully Registered')
           return redirect('/auth/login')
    return render(request,'auth/register.html')



@loginRequired
def logout_view(request):
    logout(request)
    return redirect('/auth/login')
