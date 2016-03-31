from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
import hashlib
import urllib
from django import template
from django.utils.safestring import mark_safe
import datetime

from .forms import CodehubTopicForm,CodehubTopicCommentForm
from .models import CodehubTopicModel,CodehubTopicCommentModel

register = template.Library()
# Create your views here.

@register.filter
def gravatar_url(email, size=128):
  default = "http://example.com/static/images/defaultavatar.jpg"
  return "http://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.lower()).hexdigest(), urllib.urlencode({'d':default, 's':str(size)}))


@register.filter
def gravatar(email, size=128):
    url = gravatar_url(email, size)
    return mark_safe('<img src="%s" height="%d" width="%d">' % (url, size, size))


#decorator for authenticating the user is logged in or not
def loginRequired(func):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated():
            return redirect('login_view')
        return func(request,*args,**kwargs)
    return wrapper


#decorator for checking that only the user of the topic can comment
def check_user_access_for_topic_edit_or_comment(func):
    def wrapper(request,id,*args,**kwargs):
        topic_details = CodehubTopicModel.objects.get(id = id)
        if topic_details.user.username != request.user.username:
            return redirect('/codehub/topic')
        return func(request,id,*args,**kwargs)
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
                print 'The user is valid,active and authenticated'
                request.session['gravatar'] = gravatar(username)
                print gravatar(user.email)
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
def codehub(request):
    form = CodehubTopicForm()
    return render(request,'codehub/index.html',{'form':form})

@loginRequired
def codehub_topic(request):
    if request.method == 'POST':
        form = CodehubTopicForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username = request.user.username)
            new_topic = CodehubTopicModel(
                user = user,
                topic_heading = form.cleaned_data['topic_heading'],
                topic_detail = form.cleaned_data['topic_detail'],
                topic_link = form.cleaned_data['topic_link'],
                tags = form.cleaned_data['tags'],
                topic_type = form.cleaned_data['topic_type'],
                timeStamp = datetime.datetime.now()
            )
            new_topic.save()
            #add flash message
            return redirect('/codehub/topic')
    else:
        form = CodehubTopicForm()
    topics = CodehubTopicModel.objects.all().order_by('-timeStamp')
    return render(request,'codehub/topic.html',{'form':form,'topics':topics})


@loginRequired
@check_user_access_for_topic_edit_or_comment
def edit_topic(request,id):
    if request.method == 'POST':
        form = CodehubTopicForm(request.POST)
        if form.is_valid():
            initial_topic_details = CodehubTopicModel.objects.get(id=id)
            form =CodehubTopicForm(request.POST,instance = initial_topic_details)
            form.save()
            #flash message for edit data
            print 'data edited'
            return redirect('/codehub/topic')
    else:
        topic_details = CodehubTopicModel.objects.get(id = id)
        data = {'topic_heading':topic_details.topic_heading,'topic_detail':topic_details.topic_detail,'topic_link':topic_details.topic_link,'tags':topic_details.tags}
        form = CodehubTopicForm(initial = data)
    return render(request,'codehub/edit_topic.html',{'form':form})


#check that only the user can delete or removw his posts only
@loginRequired
@check_user_access_for_topic_edit_or_comment
def remove_topic(request,id):
    CodehubTopicModel.objects.get(id = id).delete()
    print 'deleted'
    return redirect('/codehub/topic')


@loginRequired
def comment_on_topic(request,id):
    if request.method == 'POST':
        form = CodehubTopicCommentForm(request.POST)
        if form.is_valid():
            new_comment = CodehubTopicCommentModel(
                user = User.objects.get(username = request.user.username),
                topic = CodehubTopicModel.objects.get(id = id),
                comment_text = form.cleaned_data['comment_text'],
                timeStamp = datetime.datetime.now()
            )
            new_comment.save()
            #flash message here
            return redirect("/codehub/topic/"+id+"/comment")
    else:
        form = CodehubTopicCommentForm()
    comments = CodehubTopicCommentModel.objects.all().order_by('-timeStamp')
    topic_details = CodehubTopicModel.objects.get(id = id)
    return render(request,'codehub/comment_on_topic.html',{'form':form,'comments':comments,'topic':topic_details})


@loginRequired
def logout_view(request):
    logout(request)
    return redirect('/auth/login')
