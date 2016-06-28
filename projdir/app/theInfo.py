from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
import datetime


from app.codehub import loginRequired


@loginRequired
def get_generic_main_page(request):
    return render(request,'theInfo/main.html');   #main.html is the page having the search engine
