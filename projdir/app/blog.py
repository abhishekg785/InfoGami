from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User

from .forms import BlogForm
from .views import loginRequired

@loginRequired
def blog(request):
    form = BlogForm()
    return render(request,'blog/index.html',{'form':form})
