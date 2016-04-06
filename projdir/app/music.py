from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User

from .models import MusicModel
from .views import loginRequired

@loginRequired
def music_list(request):
    music_list = MusicModel.objects.all()
    return render(request,'music/music_list.html',{'music_list':music_list})
