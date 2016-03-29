from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.

#route for login the user
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username,password = password)
        if user is not None:
            if user.is_active:
                print 'The user is valid,active and authenticated'
            else:
                print 'The password is valid,but the account has been disabled'
        else:
            print 'Invalid username or password'
    return render(request,'auth/login.html')


#route for registering the user
def register(request):
    if request.method == 'POST':
       fname = request.POST['fname']
       lname = request.POST['lname']
       username = request.POST['username']
       email = request.POST['email']
       password = request.POST['password']
       User.create_user(first_name = fname,last_name = lname,username = username,email = email,password = password)
       return HttpResponse('Successfully registered');
    return render(request,'auth/register.html')
