from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
import datetime
from django.utils.datastructures import MultiValueDictKeyError

from .forms import CodehubTopicForm,CodehubTopicCommentForm,SearchForm
from .models import CodehubTopicModel,CodehubTopicCommentModel
from .views import loginRequired

#decorator for checking that only the user of the topic can comment
def check_user_access_for_topic_edit(func):
    def wrapper(request,id,*args,**kwargs):
        topic_details = CodehubTopicModel.objects.get(id = id)
        if topic_details.user.username != request.user.username:
            return redirect('/codehub/topic')
        return func(request,id,*args,**kwargs)
    return wrapper


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
            try:
                file = request.FILES['file']
            except MultiValueDictKeyError:
                file = False
            new_topic = CodehubTopicModel(
                user = user,
                topic_heading = form.cleaned_data['topic_heading'],
                topic_detail = form.cleaned_data['topic_detail'],
                topic_link = form.cleaned_data['topic_link'],
                tags = form.cleaned_data['tags'],
                topic_type = form.cleaned_data['topic_type'],
                file = file,
                timeStamp = datetime.datetime.now(),
            )
            new_topic.save()
            #add flash message
            return redirect('/codehub/topic')
    else:
        form = CodehubTopicForm()
        search_form = SearchForm()
    topics = CodehubTopicModel.objects.all().order_by('-timeStamp')
    return render(request,'codehub/topic.html',{'form':form,'topics':topics,'search_form':search_form})


@loginRequired
@check_user_access_for_topic_edit
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
@check_user_access_for_topic_edit
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
    comments = CodehubTopicCommentModel.objects.filter(topic_id = id).order_by('-timeStamp')
    topic_details = CodehubTopicModel.objects.get(id = id)
    return render(request,'codehub/comment_on_topic.html',{'form':form,'comments':comments,'topic':topic_details})



@loginRequired
def search_topic(request):
    if request.method == 'POST':
        string = request.POST['search_str']
        result = CodehubTopicModel.objects.filter(topic_heading__contains=string)
        return HttpResponse(result)
    return HttpResponse('cdcdjkcbk')



#COMMENT ROUTES START here
def check_user_access_for_comment_edit(func):
    def wrapper(request,id,*args,**kwargs):
        comment_details = CodehubTopicCommentModel.objects.get(id = id)
        if comment_details.user.username != request.user.username:
            return redirect('/codehub/topic')
        return func(request,id,*args,**kwargs)
    return wrapper



@loginRequired
@check_user_access_for_comment_edit
def remove_topic_comment(request,id):
    #get the id of the topic of the comment
    topic_id = CodehubTopicCommentModel.objects.get(id = id).topic.id
    CodehubTopicCommentModel.objects.get(id = id).delete()
    return redirect('/codehub/topic/'+str(topic_id)+'/comment')



@loginRequired
@check_user_access_for_comment_edit
def edit_topic_comment(request,id):
    if request.method == 'POST':
        form = CodehubTopicCommentForm(request.POST)
        if form.is_valid():
            comment = CodehubTopicCommentModel.objects.get(id = id)
            form = CodehubTopicCommentForm(request.POST,instance = comment)
            form.save()
            return redirect('/codehub/topic/'+str(comment.topic.id)+'/comment')
    else:
        comment = CodehubTopicCommentModel.objects.get(id = id)
        comment_data = {'comment_text':comment.comment_text}
        form = CodehubTopicCommentForm(initial = comment_data)
    return render(request,'codehub/edit_comment_on_topic.html',{'form':form})
