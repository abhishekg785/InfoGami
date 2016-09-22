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
from .models import UserProfileModel,CodehubTopicModel,CodehubQuestionModel,BlogPostModel,CodehubInnovationPostModel,CodehubCreateEventModel,FollowUserModel,MesssageModel
import datetime

#pagination stuff
from .codehub import do_pagination
from os.path import join as isfile
from django.conf import settings
import os
import json
import time

from django.db.models import Count


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
    data = ['user_description', 'skills', 'user_type_select', 'programme', 'branch', 'graduation_year', 'college_year', 'user_profile_pic']
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        print form
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
            form_data = {
              'user_description':profile_details.user_description,
              'skills':skills,
              'user_type_select':profile_details.user_type_select,
              'programme' : profile_details.programme,
              'branch' : profile_details.branch,
              'college_year' : profile_details.college_year,
              'graduation_year' : profile_details.graduation_year,
              'user_profile_pic':profile_details.user_profile_pic
            }
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



@loginRequired
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
    return HttpResponse(followed_user_arr)


#the route is for getting the following users
@loginRequired
def get_following_users(request,user_id):
    username = User.objects.get(id = user_id).username  #username if the name of the user with id = user_id
    following_users = FollowUserModel.objects.filter(followed_user_id = user_id)
    followers_count = following_users.count()
    return render(request,'users/following_users_view.html',{'username':username,'user_id':user_id,'following_users':following_users,'followers_count':followers_count})


#this gives the users i am following
@loginRequired
def get_users_followed(request,user_id):
    username = User.objects.get(id = user_id)
    followed_users = FollowUserModel.objects.filter(following_user_id = user_id)
    followed_count = followed_users.count()
    return render(request,'users/followed_users_list.html',{'username':username,'user_id':user_id,'followed_users':followed_users,'followed_count':followed_count})





#sends the new messages of the user
@loginRequired
def user_new_messages_api(request):
    #select sender_id,count(messages) from <table name> group by sender_id where receiver_id = user.id
    #getting all unseen messages
    new_message_arr = []
    sender_message_count_arr = MesssageModel.objects.filter( message_status = 'False',receiver_id = request.user.id).values('sender_id').annotate(message_count = Count('sender_id'))
    if not sender_message_count_arr:
        return HttpResponse(json.dumps([]),content_type = 'application/json')
    else:
        for sender in sender_message_count_arr:
            sender_message_count = sender['message_count']
            sender_id = sender['sender_id']
            sender_username = User.objects.get(id = sender_id).username
            sender_profile_pic = UserProfileModel.objects.get(user_id = sender_id).user_profile_pic.name
            latest_message = MesssageModel.objects.filter(message_status = 'False' , sender_id = sender_id).values('message_text','created').order_by('-created')[:1]
            message_obj = {'sender_id':sender_id,'sender':sender_username,'message_count':sender_message_count,'latest_message':latest_message[0]['message_text'],'sender_profile_pic':sender_profile_pic,'created':str(latest_message[0]['created'])}
            new_message_arr.append(message_obj)
    return HttpResponse(json.dumps(new_message_arr),content_type = 'application/json')





@loginRequired
def post_message_api(request):
    error_msg = {'message':'Error'}
    success_msg = {'message':'success'}
    if request.method == 'POST':
        sender_id = request.POST['sender_id']
        receiver_id = request.POST['receiver_id']
        message_text = request.POST['message_text']
        new_message = MesssageModel(
            sender = User.objects.get(id = sender_id),
            receiver = User.objects.get(id = receiver_id),
            sender_profile = UserProfileModel.objects.get(user_id = sender_id),
            receiver_profile = UserProfileModel.objects.get(user_id = receiver_id),
            message_text = message_text
        )
        new_message.save();
        return HttpResponse(json.dumps(success_msg),content_type = 'application/json')
    else:
        # return HttpResponse('cdcjkdbckjdbckjdc')
        return HttpResponse(json.dumps(error_msg),content_type = 'application/json')




#deals with the all messages of the user
@loginRequired
def get_user_messages(request):
    new_messages = MesssageModel.objects.filter(receiver_id = request.user.id)
    message_count = new_messages.count()
    return HttpResponse(message_count)
    # return HttpResponse('message section');




#api to set the status of all the messages to true
@loginRequired
def set_message_status_true_api(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        new_messages = MesssageModel.objects.filter(receiver_id = user_id , message_status = False)
        for msg in new_messages:
            msg.message_status = True
            msg.save()
    return HttpResponse('success')






#MESSAGE CENTER apis
#fetch the user's messages by the given sender

@loginRequired
def get_message_center(request):
    return render(request,'users/message_center.html')



    # """
    # sender
    # received messages
    # sent messages
    # """
    # messages = MesssageModel.objects.filter(receiver_id = request.user.id)
    # return HttpResponse(messages)




#api to fetch data for message center api
@loginRequired
def get_message_center_data_api(request):
    received_message_data = []
    sent_message_data = []
    rec_messages = MesssageModel.objects.filter(receiver_id = request.user.id).order_by('-created').distinct()
    for msg in rec_messages:
        created = msg.created
        sender_pic = msg.sender_profile.user_profile_pic.name
        obj1 = {'sender':msg.sender.username,'message':msg.message_text,'sender_profile_pic':sender_pic,'created':str(created)}
        received_message_data.append(obj1)
    sent_messages = MesssageModel.objects.filter(sender_id = request.user.id).order_by('-created').distinct()
    for msg in sent_messages:
        receiver_pic = msg.receiver_profile.user_profile_pic.name
        obj2 = {'receiver':msg.receiver.username,'message':msg.message_text,'receiver_profile_pic':receiver_pic,'created':str(msg.created)}
        sent_message_data.append(obj2)
    final_obj = {'sent_message_data':sent_message_data,'received_message_data':received_message_data}
    print final_obj
    return HttpResponse(json.dumps(final_obj),content_type = 'application/json')






@loginRequired
def fetch_user_messages_message_center_api(request,sender_id):
    #fetch user messages by the sender having id = sender_id
    messages = MesssageModel.objects.filter(receiver_id = request.user.id, sender_id = sender_id).order_by('-created')
    return HttpResponse(messages)
    #return HttpResponse(json.dumps(messages), content_type = 'application/json')
