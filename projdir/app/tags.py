from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django import template

def tags(request):
    return render(request,'tags/index.html')
