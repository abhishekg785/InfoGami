from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django import template
from django.utils.safestring import mark_safe
from django.contrib import messages
import hashlib
import urllib

from sets import Set

from .views import loginRequired
from .forms import UserProfileForm,SearchForm
from .models import UserProfileModel,CodehubTopicModel,CodehubQuestionModel,BlogPostModel,CodehubInnovationPostModel,CodehubCreateEventModel,FollowUserModel
import datetime

#pagination stuff
from .codehub import do_pagination
from os.path import join as isfile
from django.conf import settings
import os

register = template.Library()

#decorator to check user has access to edit profile or not
def check_user_access_for_profile_edit(func):
    def wrapper(request,user_id,*args,**kwargs):
        print int(request.user.id) == int(user_id)
        if int(request.user.id) != int(user_id):
            return redirect('/users/profile/'+str(user_id))
        return func(request,user_id,*args,**kwargs)
    return wrapper



@loginRequired
def get_users(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            user_str = form.cleaned_data['search_str']
            users =  User.objects.filter(username__contains = user_str)
            return render(request,'users/search_user.html',{'form':form,'result':users,'search_str':user_str})
    else:
        form = SearchForm()
    users_list = User.objects.values('id','username').exclude(id = request.user.id)
    users = do_pagination(request,users_list,5)
    return render(request,'users/user_list.html',{'users':users,'form':form})


@loginRequired
def user_profile(request,user_id):
    # info = User.objects.get(id = user_id)
    info = get_object_or_404(User,id = user_id)
    try:
        user_profile = UserProfileModel.objects.get(user_id = user_id)
    except:
        user_profile = False
    #getting user following data
    try:
        follow_result = FollowUserModel.objects.get(following_user_id = request.user.id,followed_user_id = user_id)
        is_following = follow_result
    except:
        is_following = False
    return render(request,'users/user_profile.html',{'user_info':info,'user_profile':user_profile,'is_following':is_following})


@loginRequired
@check_user_access_for_profile_edit
def edit_user_profile(request,user_id):
    data = ['user_description','skills','user_type_select','user_profile_pic']
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            try:
                file = request.FILES['user_profile_pic']
            except:
                file = ''
            # profile_details = get_object_or_404(UserProfileModel,user_id = user_id)
            try:
                profile_details = UserProfileModel.objects.get(user_id = user_id)
                if profile_details.user_profile_pic != file:
                    if profile_details.user_profile_pic:
                        file_path = os.path.join(settings.MEDIA_ROOT,profile_details.user_profile_pic.name)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                profile_details.user_profile_pic = file
            except:
                user = User.objects.get(id = user_id)
                profile_details = UserProfileModel(user = user)
                profile_details.user_profile_pic = file
            form = UserProfileForm(request.POST,instance = profile_details)
            form.save()
            messages.success(request,'User profile edited Successfully')
            return redirect('/user/profile/'+str(user_id))
    else:
        try:
            profile_details = UserProfileModel.objects.get(user_id = user_id)
        except:
            print 'No data yet'
            profile_details = []
        if not profile_details:
            form_data = {key:'' for key in data}
        else:
            skillArr = []
            skills = profile_details.skills.all()
            for skill in skills:
                skillArr.append(skill.name)
            skills = ",".join(skillArr)
            form_data = {'user_description':profile_details.user_description,'skills':skills,'user_type_select':profile_details.user_type_select,'user_profile_pic':profile_details.user_profile_pic}
        form = UserProfileForm(initial = form_data)
    return render(request,'users/edit_user_profile.html',{'form':form})


def get_username(request,user_id):
    username = get_object_or_404(User,id = user_id).username
    return username


@loginRequired
def get_user_topics(request,user_id):
    topics_list = CodehubTopicModel.objects.filter(user_id = user_id).order_by("-created")
    topics = do_pagination(request,topics_list,5)
    topic_user = get_username(request,user_id)
    return render(request,'codehub/topic/get_user_topics.html',{'topics':topics,'topic_user':topic_user})

@loginRequired
def get_user_questions(request,user_id):
    questions_list = CodehubQuestionModel.objects.filter(user_id = user_id).order_by("-created")
    questions = do_pagination(request,questions_list,5)
    question_user = get_username(request,user_id)
    return render(request,'codehub/question/get_user_questions.html',{'questions':questions,'question_user':question_user})

@loginRequired
def get_user_new_ideas(request,user_id):
    innovation_list = CodehubInnovationPostModel.objects.filter(user_id = user_id).order_by("-created")
    innovations = do_pagination(request,innovation_list,5)
    username = get_username(request,user_id)
    return render(request,'codehub/innovation/get_user_innovations.html',{'innovations':innovations,'username':username})



@loginRequired
def get_codehub_user_events(request,user_id):
    event_list = CodehubCreateEventModel.objects.filter(user_id = user_id).order_by('-created')
    print event_list
    events = do_pagination(request,event_list,5)
    username = get_username(request,user_id)
    return render(request,'codehub/event/get_user_events.html',{'events':events,'username':username})



@loginRequired
def get_user_articles_or_blogs(request,user_id):
    return HttpResponse('user questions')

@loginRequired
def user_blog(request,user_id):
    user_details = get_object_or_404(User,id = user_id)
    # user_profile = get_object_or_404(UserProfileModel,user_id = user_id)
    try:
        user_profile = UserProfileModel.objects.get(user_id = user_id)
    except:
        user_profile = False
    #get all tags related
    tagArr = []
    blog_posts = BlogPostModel.objects.filter(user_id = user_id).order_by('-created')
    for post in blog_posts:
        for tag in post.tags.all():
            tagArr.append(tag)
    tagArr = Set(tagArr)
    return render(request,'blog/user_blog.html',{'user_info':user_details,'user_profile':user_profile,'blog_posts':blog_posts,'tagArr':tagArr})



def check_user_access_to_follow(func):
    def wrapper(request,user_id,*args,**kwargs):
        if str(request.user.id) == str(user_id):
            return redirect('/')
        return func(request,user_id,*args,**kwargs)
    return wrapper



def check_if_user_followed(func):
    def wrapper(request,user_id,*args,**kwargs):
        try:
            result = FollowUserModel.objects.get(following_user_id = request.user.id,followed_user_id = user_id)
            return redirect('/')
        except:
            print 'no record'
        return func(request,user_id,*args,**kwargs)
    return wrapper



#decorator for not following himsel again
#decorator for not following twice
@loginRequired
@check_user_access_to_follow
@check_if_user_followed
def follow_user_profile(request,user_id):           #user_id is the id of the user being followed
    followed_user = get_object_or_404(User,id = user_id)
    following_user_profile = get_object_or_404(UserProfileModel,user_id = request.user.id)
    followed_user_profile = get_object_or_404(UserProfileModel,user_id = user_id)
    new_user = FollowUserModel(
        following_user = request.user,
        followed_user = followed_user,
        following_user_profile = following_user_profile,
        followed_user_profile = followed_user_profile
    )
    new_user.save()
    messages.success(request,'User followed Successfully')
    return redirect('/user/profile/'+str(user_id))


@loginRequired
@check_user_access_to_follow
def unfollow_user_profile(request,user_id):
    result = get_object_or_404(FollowUserModel,following_user_id = request.user.id,followed_user_id = user_id)
    result.delete()
    messages.success(request,'User has been unfollowed')
    return redirect('/user/profile/'+str(user_id))


def get_user_notifications(request):
    followed_user_arr = []
    followed_users = FollowUserModel.objects.filter(following_user_id = request.user.id)
    for user_obj in followed_users:
        followed_user_arr.append(user_obj.followed_user.username)
    print followed_user_arr
    #get the blog_posts
    #get_user_questions
    #get user_topics
    #get user_ideas
    #return render(request,'users/notifications.html',{'notifications':followed_users})
    return HttpResponse('to be implemented')
