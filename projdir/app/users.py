from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django import template
from django.utils.safestring import mark_safe
import hashlib
import urllib

from sets import Set

from .views import loginRequired
from .forms import UserProfileForm,SearchForm
from .models import UserProfileModel,CodehubTopicModel,CodehubQuestionModel,BlogPostModel
import datetime

#pagination stuff
from .codehub import do_pagination

register = template.Library()

#decorator to check user has access to edit profile or not
def check_user_access_for_profile_edit(func):
    def wrapper(request,user_id,*args,**kwargs):
        print int(request.user.id) == int(user_id)
        if int(request.user.id) != int(user_id):
            return redirect('/users/profile/'+str(user_id))
        return func(request,user_id,*args,**kwargs)
    return wrapper


@register.filter
def gravatar_url(email, size=128):
  default = "http://example.com/static/images/defaultavatar.jpg"
  return "http://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.lower()).hexdigest(), urllib.urlencode({'d':default, 's':str(size)}))


@register.filter
def gravatar(email, size=128):
    url = gravatar_url(email, size)
    # return mark_safe('<img src="%s" height="%d" width="%d">' % (url, size, size))
    return url

@loginRequired
def get_users(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            user_str = form.cleaned_data['search_str']
            users = User.objects.filter(username__contains = user_str)
            return render(request,'users/search_user.html',{'form':form,'result':users,'search_str':user_str})
    else:
        form = SearchForm()
    users_list = User.objects.values('id','username')
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
    user_gravatar_url = gravatar(info.email)
    print user_gravatar_url
    return render(request,'users/user_profile.html',{'user_info':info,'user_profile':user_profile,'gravatar_url':user_gravatar_url})


@loginRequired
@check_user_access_for_profile_edit
def edit_user_profile(request,user_id):
    data = ['user_description','skills','user_type_select']
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            try:
                profile_details = UserProfileModel.objects.get(user_id = user_id)
            except:
                user = User.objects.get(id = user_id)
                profile_details = UserProfileModel(user = user)
            form = UserProfileForm(request.POST,instance = profile_details)
            form.save()
            return redirect('/users/profile/'+str(user_id))
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
            print skills
            for skill in skills:
                skillArr.append(skill.name)
            skills = ",".join(skillArr)
            form_data = {'user_description':profile_details.user_description,'skills':skills,'user_type_select':profile_details.user_type_select}
        form = UserProfileForm(initial = form_data)
    return render(request,'users/edit_user_profile.html',{'form':form})


@loginRequired
def get_user_topics(request,user_id):
    topics = CodehubTopicModel.objects.filter(user_id = user_id).order_by("-created")
    topic_user = get_object_or_404(User,id = user_id).username
    return render(request,'codehub/topic/get_user_topics.html',{'topics':topics,'topic_user':topic_user})

@loginRequired
def get_user_questions(request,user_id):
    questions = CodehubQuestionModel.objects.filter(user_id = user_id).order_by("-created")
    question_user = get_object_or_404(User,id = user_id).username
    return render(request,'codehub/question/get_user_questions.html',{'questions':questions,'question_user':question_user})

@loginRequired
def get_user_new_ideas(request,user_id):
    return HttpResponse('user questions')

@loginRequired
def get_user_talks_or_events(request,user_id):
    return HttpResponse('user questions')

@loginRequired
def get_user_articles_or_blogs(request,user_id):
    return HttpResponse('user questions')


def user_blog(request,user_id):
    user_details = get_object_or_404(User,id = user_id)
    # user_profile = get_object_or_404(UserProfileModel,user_id = user_id)
    try:
        user_profile = UserProfileModel.objects.get(user_id = user_id)
    except:
        user_profile = False
    user_gravatar_url = gravatar(user_details.email)
    #get all tags related
    tagArr = []
    blog_posts = BlogPostModel.objects.filter(user_id = user_id)
    for post in blog_posts:
        for tag in post.tags.all():
            tagArr.append(tag)
    tagArr = Set(tagArr)
    return render(request,'blog/user_blog.html',{'user_info':user_details,'user_profile':user_profile,'blog_posts':blog_posts,'user_gravatar_url':user_gravatar_url,'tagArr':tagArr})


    def search_post_by_slug(request,slug):
        return HttpResponse(slug)
