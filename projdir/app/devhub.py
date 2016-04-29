from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
import datetime

from taggit.models import Tag
from itertools import chain
from sets import Set

from app.codehub import  loginRequired,do_pagination

from app.forms import DevhubQuestionForm,SearchForm,DevhubQuestionAnswerForm,DevhubTopicForm,DevhubTopicCommentForm
from app.models import DevhubQuestionModel,UserProfileModel,DevhubQuestionAnswerModel,DevhubTopicModel,DevhubTopicCommentModel

from os.path import join as isfile
from django.conf import settings
import os


def devhub(request):
    return render(request,'devhub/index.html')



def devhub_question(request):
    if request.method == 'POST':
        form = DevhubQuestionForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['question_tags']
            new_question = DevhubQuestionModel(
                user = request.user,
                user_profile = UserProfileModel.objects.get(user_id = request.user.id),
                question_heading = form.cleaned_data['question_heading'],
                question_description = form.cleaned_data['question_description'],
                question_link = form.cleaned_data['question_link'],
                question_type = form.cleaned_data['question_type'],
            )
            new_question.save()
            new_question.question_tags.add(*tags)
            print 'saved'
            return redirect('/developer-section/ask-question')
    else:
        form = DevhubQuestionForm()
    search_form = SearchForm()
    questions = DevhubQuestionModel.objects.all().order_by('-created')[:5]
    return render(request,'devhub/question/ask_question.html',{'form':form,'questions':questions,'search_form':search_form})



@loginRequired
def devhub_question_details(request,ques_id):
    if request.method == 'POST':
        form = DevhubQuestionAnswerForm(request.POST)
        if form.is_valid():
            new_ans = DevhubQuestionAnswerModel(
                user = request.user,
                user_profile = UserProfileModel.objects.get(user_id = request.user.id),
                question = DevhubQuestionModel.objects.get(id = ques_id),
                answer_text = form.cleaned_data['answer_text']
            )
            new_ans.save()
            return redirect('/developer-section/question/'+str(ques_id)+'/details')
    else:
        form = DevhubQuestionAnswerForm()
    ques_details = get_object_or_404(DevhubQuestionModel,id = ques_id)
    ques_answers = DevhubQuestionAnswerModel.objects.all().order_by('-created')
    print ques_answers
    return render(request,'devhub/question/ques_details.html',{'ques_details':ques_details,'form':form,'ques_answers':ques_answers})




#decorator for checking user access for question edit and remove
def check_user_access_for_question_edit(func):
    def wrapper(request,ques_id,*args,**kwargs):
        ques_details = get_object_or_404(DevhubQuestionModel,id = ques_id)
        if ques_details.user.id != request.user.id:
            return redirect('/')
        return func(request,ques_id,*args,**kwargs)
    return wrapper


@loginRequired
@check_user_access_for_question_edit
def edit_devhub_question(request,ques_id):
    if request.method == 'POST':
        form = DevhubQuestionForm(request.POST)
        if form.is_valid():
            ques_details = DevhubQuestionModel.objects.get(id = ques_id)
            form = DevhubQuestionForm(request.POST,instance = ques_details)
            form.save();
            return redirect('/developer-section/question/'+str(ques_id)+'/details/')
    else:
        tagArr = []
        ques_details = DevhubQuestionModel.objects.get(id = ques_id)
        for tag in ques_details.question_tags.all():
            tagArr.append(tag.name)
        tags = ",".join(tagArr)
        ques_data = {'question_heading':ques_details.question_heading,'question_description':ques_details.question_description,'question_link':ques_details.question_link,'question_type':ques_details.question_type,'question_tags':tags}
        form = DevhubQuestionForm(initial = ques_data)
    ques_details = DevhubQuestionModel.objects.get(id = ques_id)
    return render(request,'devhub/question/edit_question.html',{'form':form,'ques_heading':ques_details.question_heading})


@loginRequired
@check_user_access_for_question_edit
def remove_devhub_question(request,ques_id):
    ques_details = DevhubQuestionModel.objects.get(id = ques_id)
    ques_details.delete()
    return redirect('/developer-section/ask-question/')





@loginRequired
def get_all_devhub_questions(request):
    question_list = DevhubQuestionModel.objects.all().order_by('-created')
    question_count = question_list.count()
    questions = do_pagination(request,question_list,5)
    form = SearchForm()
    return render(request,'devhub/question/get_all_devhub_questions.html',{'form':form,'questions':questions,'question_count':question_count})




@loginRequired
def search_devhub_question(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_str = form.cleaned_data['search_str']
            list_by_title = DevhubQuestionModel.objects.filter(question_heading__contains = search_str).order_by('-created')
            list_by_tags = DevhubQuestionModel.objects.filter(question_tags__name__in = [search_str]).order_by('-created')
            result = list(chain(list_by_title,list_by_tags))
            result = Set(result)
            return render(request,'devhub/question/search_question.html',{'form':form,'results':result})
    else:
        form = SearchForm()
    return render(request,'devhub/question/search_question.html',{'form':form})





@loginRequired
def edit_devhub_question_answer(request,ques_id,ans_id):
    if request.method == 'POST':
        form = DevhubQuestionAnswerForm(request.POST)
        if form.is_valid():
            ans_details = get_object_or_404(DevhubQuestionAnswerModel,id = ans_id)
            form = DevhubQuestionAnswerForm(request.POST,instance = ans_details)
            form.save()
            return redirect('/developer-section/question/'+str(ques_id)+'/details')
    else:
        ans_details = get_object_or_404(DevhubQuestionAnswerModel,id = ans_id)
        ans_data = {'answer_text':ans_details.answer_text}
        form = DevhubQuestionAnswerForm(initial = ans_data)
    return render(request,'devhub/question/edit_devhub_question_answer.html',{'form':form})






@loginRequired
def remove_devhub_question_answer(request,ques_id,ans_id):
    answer = DevhubQuestionAnswerModel.objects.get(id = ans_id)
    answer.delete()
    return redirect('/developer-section/question/'+str(ques_id)+'/details')




@loginRequired
def devhub_topic(request):
    if request.method == 'POST':
        form = DevhubTopicForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            try:
                file = request.FILES['file']
            except:
                file = ""
            new_topic = DevhubTopicModel(
                user = request.user,
                user_profile = UserProfileModel.objects.get(user_id = request.user.id),
                topic_heading = form.cleaned_data['topic_heading'],
                topic_link = form.cleaned_data['topic_link'],
                topic_detail = form.cleaned_data['topic_detail'],
                file = file
            )
            new_topic.save()
            new_topic.tags.add(*tags)
            return redirect('/developer-section/post-topic')
    else:
        form = DevhubTopicForm()
    search_form = SearchForm()
    topics = DevhubTopicModel.objects.all().order_by('-created')[:5]
    return render(request,'devhub/topic/post_topic.html',{'form':form,'search_form':search_form,'topics':topics})




@loginRequired
def get_all_devhub_topics(request):
    form = SearchForm()
    topics_list = DevhubTopicModel.objects.all().order_by('-created')
    topic_count = topics_list.count()
    topics = do_pagination(request,topics_list,5)
    return render(request,'devhub/topic/get_all_topics.html',{'topics':topics,'topic_count':topic_count,'form':form})




@loginRequired
def search_devhub_topic(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_str = form.cleaned_data['search_str']
            list_by_heading = DevhubTopicModel.objects.filter(topic_heading__contains = search_str).order_by('-created')
            list_by_tags = DevhubTopicModel.objects.filter(tags__name__in = [search_str]).order_by('-created').distinct()
            results = list(chain(list_by_heading,list_by_tags))
            results = Set(results)
            return render(request,'devhub/topic/search_topic.html',{'form':form,'results':results,'search_str':search_str})
    else:
        form = SearchForm()
    return render(request,'devhub/topic/search_topic.html',{'form':form})



@loginRequired
def devhub_topic_details(request,topic_id):
    if request.method == 'POST':
        form = DevhubTopicCommentForm(request.POST)
        if form.is_valid():
            new_comment = DevhubTopicCommentModel(
                user = request.user,
                user_profile = UserProfileModel.objects.get(user_id = request.user.id),
                topic = DevhubTopicModel.objects.get(id = topic_id),
                comment_text = form.cleaned_data['comment_text']
            )
            new_comment.save()
            return redirect('/developer-section/topic/'+str(topic_id)+'/details')
    else:
        form = DevhubTopicCommentForm()
    topic_details = get_object_or_404(DevhubTopicModel,id = topic_id)
    comments = DevhubTopicCommentModel.objects.all()
    return render(request,'devhub/topic/topic_details.html',{'topic':topic_details,'form':form,'comments':comments})




def check_user_acess_for_devhub_topic_edit(func):
    def wrapper(request,topic_id,*args,**kwargs):
        topic_details = get_object_or_404(DevhubTopicModel,id = topic_id)
        if topic_details.user.id != request.user.id:
            return redirect('/')
        return func(request,topic_id,*args,**kwargs)
    return wrapper



@loginRequired
@check_user_acess_for_devhub_topic_edit
def edit_devhub_topic(request,topic_id):
    if request.method == 'POST':
        form = DevhubTopicForm(request.POST)
        if form.is_valid():
            topic_details = get_object_or_404(DevhubTopicModel,id = topic_id)
            try:
                file = request.FILES['file']
            except:
                file = ''
            if topic_details.file != file:
                if topic_details.file:
                    file_path = os.path.join(settings.MEDIA_ROOT,topic_details.file.name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
            topic_details.file = file
            form = DevhubTopicForm(request.POST,instance = topic_details)
            form.save()
            return redirect('/developer-section/topic/'+str(topic_id)+'/details')
    else:
        tagArr = []
        topic_details = get_object_or_404(DevhubTopicModel,id = topic_id)
        tags = topic_details.tags.all()
        for tag in tags:
            tagArr.append(tag.name)
        tags = ",".join(tagArr)
        topic_data = {'topic_heading':topic_details.topic_heading,'topic_detail':topic_details.topic_detail,'topic_link':topic_details.topic_link,'file':topic_details.file,'tags':tags}
        form = DevhubTopicForm(initial = topic_data)
    return render(request,'devhub/topic/edit_topic.html',{'topic_heading':topic_details.topic_heading,'form':form})



@loginRequired
@check_user_acess_for_devhub_topic_edit
def remove_devhub_topic(request,topic_id):
    topic = get_object_or_404(DevhubTopicModel,id = topic_id)
    topic.delete()
    return redirect('/developer-section/post-topic/')




def check_user_acess_for_devhub_topic_comment_edit(func):
    def wrapper(request,topic_id,comm_id,*args,**kwargs):
        comm_details = get_object_or_404(DevhubTopicCommentModel,id = comm_id)
        if comm_details.user.id != request.user.id:
            return redirect('/')
        return func(request,topic_id,comm_id,*args,**kwargs)
    return wrapper



@loginRequired
@check_user_acess_for_devhub_topic_comment_edit
def edit_devhub_topic_comment(request,topic_id,comm_id):
    if request.method == 'POST':
        form = DevhubTopicCommentForm(request.POST)
        if form.is_valid():
            comment_details = get_object_or_404(DevhubTopicCommentModel,id = comm_id)
            form = DevhubTopicCommentForm(request.POST,instance = comment_details)
            form.save()
            return redirect('/developer-section/topic/'+str(topic_id)+'/details')
    else:
        comment_details = get_object_or_404(DevhubTopicCommentModel,id = comm_id)
        comment_data = {'comment_text':comment_details.comment_text}
        form = DevhubTopicCommentForm(initial = comment_data)
    return render(request,'devhub/topic/edit_topic_comment.html',{'form':form})




@loginRequired
@check_user_acess_for_devhub_topic_comment_edit
def remove_devhub_topic_comment(request,topic_id,comm_id):
    comment = get_object_or_404(DevhubTopicCommentModel,id = comm_id)
    comment.delete()
    return redirect('/developer-section/topic/'+str(topic_id)+'/details')
