from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
import datetime
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator,EmptyPage,InvalidPage

from .forms import CodehubTopicForm,CodehubTopicCommentForm,SearchForm,CodehubQuestionForm,CodehubQuestionCommentForm,CodehubInnovationPostForm,CodehubInnovationCommentForm
from .models import CodehubTopicModel,CodehubTopicCommentModel,CodehubQuestionModel,CodehubQuestionCommentModel,CodehubInnovationPostModel,CodehubInnovationCommentModel
from .views import loginRequired

from taggit.models import Tag
from itertools import chain
from sets import Set

from os.path import join as isfile
from django.conf import settings
import os

#decorator for checking that only the user of the topic can comment
def check_user_access_for_topic_edit(func):
    def wrapper(request,id,*args,**kwargs):
        # topic_details = CodehubTopicModel.objects.get(id = id)
        topic_details = get_object_or_404(CodehubTopicModel,id =id)
        if topic_details.user.username != request.user.username:
            return redirect('/codehub/topic')
        return func(request,id,*args,**kwargs)
    return wrapper


#does the pagination stuff here
def do_pagination(request,list,num_of_pages):
    paginator = Paginator(list,num_of_pages)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1

    try:
        data = paginator.page(page)
    except(EmptyPage,InvalidPage):
        data = paginator.page(paginator.num_pages)

    return data


@loginRequired
def codehub(request):
    form = CodehubTopicForm()
    return render(request,'codehub/index.html',{'form':form})


@loginRequired
def codehub_topic(request):
    if request.method == 'POST':
        form = CodehubTopicForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            try:
                file = request.FILES['file']
            except MultiValueDictKeyError:
                file = ''
            new_topic = CodehubTopicModel(
                user = request.user,
                topic_heading = form.cleaned_data['topic_heading'],
                topic_detail = form.cleaned_data['topic_detail'],
                topic_link = form.cleaned_data['topic_link'],
                topic_type = form.cleaned_data['topic_type'],
                file = file,
            )
            new_topic.save()
            new_topic.tags.add(*tags)
            #add flash message
            return redirect('/codehub/topic')
    else:
        form = CodehubTopicForm()
    search_form = SearchForm()
    topics_list = CodehubTopicModel.objects.all().order_by('-created')
    topics = do_pagination(request,topics_list,5)  #it does the pagination stuff
    return render(request,'codehub/topic/topic.html',{'form':form,'topics':topics,'search_form':search_form})




@loginRequired
@check_user_access_for_topic_edit
def edit_topic(request,id):
    if request.method == 'POST':
        form = CodehubTopicForm(request.POST)
        if form.is_valid():
            initial_topic_details = CodehubTopicModel.objects.get(id=id)
            try:
                file = request.FILES['file']
            except:
                file = ''
            if initial_topic_details.file != file:
                if initial_topic_details.file:
                    file_path = os.path.join(settings.MEDIA_ROOT,initial_topic_details.file.name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
            initial_topic_details.file = file
            form = CodehubTopicForm(request.POST,instance = initial_topic_details)
            form.save()
            #flash message for edit data
            print 'data edited'
            return redirect('/codehub/topic')
    else:
        topic_details = CodehubTopicModel.objects.get(id = id)
        tagArr = []
        for tag in topic_details.tags.all():
            tagArr.append(tag.name)
        tags = ",".join(tagArr)
        data = {'topic_heading':topic_details.topic_heading,'topic_detail':topic_details.topic_detail,'topic_link':topic_details.topic_link,'file':topic_details.file,'topic_type':topic_details.topic_type,'tags':tags}
        form = CodehubTopicForm(initial = data)
    return render(request,'codehub/topic/edit_topic.html',{'form':form})



#check that only the user can delete or removw his posts only
@loginRequired
@check_user_access_for_topic_edit
def remove_topic(request,id):
    topic_obj = get_object_or_404(CodehubTopicModel,id = id)
    topic_obj.delete()
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
            )
            new_comment.save()
            #flash message here
            return redirect("/codehub/topic/"+id+"/comment")
    else:
        form = CodehubTopicCommentForm()
    comments = CodehubTopicCommentModel.objects.filter(topic_id = id).order_by('-created')
    topic_details = CodehubTopicModel.objects.get(id = id)
    return render(request,'codehub/topic/comment_on_topic.html',{'form':form,'comments':comments,'topic':topic_details})



@loginRequired
def search_topic(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_str = form.cleaned_data['search_str']
            list_by_topic_name = CodehubTopicModel.objects.filter(topic_heading__contains=search_str)
            list_by_slug = CodehubTopicModel.objects.filter(tags__name__in = [search_str]).distinct()
            #merging the two queries
            result_list = list(chain(list_by_topic_name,list_by_slug))
            result_list = Set(result_list)
            form = SearchForm()
            return render(request,'codehub/topic/search_topic.html',{'search_str':search_str,'results':result_list,'form':form})
    else:
        form = SearchForm()
    return render(request,'codehub/topic/search_topic.html',{'form':form})



#COMMENT ROUTES START here
def check_user_access_for_comment_edit(func):
    def wrapper(request,id,*args,**kwargs):
        # comment_details = CodehubTopicCommentModel.objects.get(id = id)
        comment_details = get_object_or_404(CodehubTopicCommentModel,id = id)
        if comment_details.user.username != request.user.username:
            return redirect('/codehub/topic')
        return func(request,id,*args,**kwargs)
    return wrapper



@loginRequired
@check_user_access_for_comment_edit
def remove_topic_comment(request,id):
    #get the id of the topic of the comment
    # topic_id = CodehubTopicCommentModel.objects.get(id = id).topic.id
    topic_id = get_object_or_404(CodehubTopicCommentModel,id =id).topic.id
    get_object_or_404(CodehubTopicCommentModel,id = id).delete()

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
    return render(request,'codehub/topic/edit_comment_on_topic.html',{'form':form})



#question section starts here

#decorators for login section comes here
def check_user_access_for_question_edit_or_remove(func):
    def wrapper(request,ques_id,*args,**kwargs):
        ques_details = get_object_or_404(CodehubQuestionModel,id = ques_id)
        if ques_details.user.username != request.user.username:
            return redirect('/codehub')
        return func(request,ques_id,*args,**kwargs)
    return wrapper


@loginRequired
def codehub_question(request):
    if request.method == 'POST':
        form = CodehubQuestionForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['question_tags']
            new_ques = CodehubQuestionModel(
                user = request.user,
                question_heading = form.cleaned_data['question_heading'],
                question_description = form.cleaned_data['question_description'],
                question_link = form.cleaned_data['question_link'],
                question_type = form.cleaned_data['question_type']
            )
            new_ques.save()
            new_ques.question_tags.add(*tags)
            return redirect('/codehub/question')
    else:
        form = CodehubQuestionForm()
    search_form = SearchForm()
    codehub_questions_list = CodehubQuestionModel.objects.all().order_by("-created")
    codehub_questions = do_pagination(request,codehub_questions_list,2)
    return render(request,'codehub/question/question.html',{'form':form,'questions':codehub_questions,'search_form':search_form})



@loginRequired
def codehub_question_details(request,ques_id):
    if request.method == 'POST':
        form = CodehubQuestionCommentForm(request.POST)
        if form.is_valid():
            new_answer = CodehubQuestionCommentModel(
                user = request.user,
                question = get_object_or_404(CodehubQuestionModel,id = ques_id),
                comment_text = form.cleaned_data['comment_text']
            )
            new_answer.save()
            print 'saved'
    else:
        form = CodehubQuestionCommentForm()
    ques_details = get_object_or_404(CodehubQuestionModel,id = ques_id)
    ques_answers = CodehubQuestionCommentModel.objects.filter(question_id = ques_id).order_by("-created")
    return render(request,'codehub/question/question_details.html',{'ques_details':ques_details,'form':form,'ques_answers':ques_answers})


@loginRequired
@check_user_access_for_question_edit_or_remove
def remove_codehub_question(request,ques_id):
    ques_details = get_object_or_404(CodehubQuestionModel,id = ques_id)
    ques_user_id = ques_details.user.id
    ques_details.delete()
    print 'deleted'
    return redirect('/user/'+str(ques_user_id)+'/questions/')
    #flash message here

@loginRequired
@check_user_access_for_question_edit_or_remove
def edit_codehub_question(request,ques_id):
    if request.method == 'POST':
        form = CodehubQuestionForm(request.POST)
        if form.is_valid():
            ques_details = get_object_or_404(CodehubQuestionModel,id = ques_id)
            form = CodehubQuestionForm(request.POST,instance = ques_details)
            form.save()
            # flash messge here
            return redirect('/codehub/question/' +str(ques_id) + '/details/')
    else:
        ques_details = get_object_or_404(CodehubQuestionModel,id = ques_id)
        tagArr = []
        for tag in ques_details.question_tags.all():
            tagArr.append(tag.name)
        tags = ",".join(tagArr)
        ques_data = {'question_heading':ques_details.question_heading,'question_description':ques_details.question_description,'question_link':ques_details.question_link,'question_type':ques_details.question_type,'question_tags':tags}
        form = CodehubQuestionForm(initial = ques_data)
    return render(request,'codehub/question/edit_question.html',{'form':form})


@loginRequired
def remove_codehub_question_comment(request,ans_id):
    c_details = get_object_or_404(CodehubQuestionCommentModel,id = ans_id)
    ques_id = c_details.question.id
    c_details.delete()
    return redirect('/codehub/question/'+str(ques_id)+'/details/')


@loginRequired
def edit_codehub_question_comment(request,ans_id):
    if request.method == 'POST':
        form = CodehubQuestionCommentForm(request.POST)
        if form.is_valid():
            ans_details = get_object_or_404(CodehubQuestionCommentModel,id = ans_id)
            ques_id = ans_details.question.id
            form = CodehubQuestionCommentForm(request.POST,instance = ans_details)
            form.save()
            #flash message here
            return redirect('/codehub/question/'+str(ques_id)+'/details')
    else:
        ans_details = get_object_or_404(CodehubQuestionCommentModel,id = ans_id)
        ans_data = {'comment_text':ans_details.comment_text}
        form = CodehubQuestionCommentForm(initial = ans_data)
    return render(request,'codehub/question/edit_question_comment.html',{'form':form})


@loginRequired
def search_question(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_str = form.cleaned_data['search_str']
            list_by_question_heading = CodehubQuestionModel.objects.filter(question_heading__contains = search_str)
            list_by_tags = CodehubQuestionModel.objects.filter(question_tags__name__in = [search_str]).distinct()
            result_list = list(chain(list_by_question_heading,list_by_tags))
            result_list = Set(result_list)
            form = SearchForm()
            return render(request,'codehub/question/search_question.html',{'form':form,'results':result_list,'search_str':search_str})
    else:
        form = SearchForm()
    return render(request,'codehub/question/search_question.html',{'form':form})


@loginRequired
#codehub innovatio center comes here
def codehub_innovation(request):
    if request.method == 'POST':
        form = CodehubInnovationPostForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            new_idea = CodehubInnovationPostModel(
                user = request.user,
                title = form.cleaned_data['title'],
                description = form.cleaned_data['description'],
            )
            new_idea.save()
            new_idea.tags.add(*tags)
            return redirect('/codehub/innovation')

    else:
        form = CodehubInnovationPostForm()
    search_form = SearchForm()
    ideas = CodehubInnovationPostModel.objects.all().order_by('-created')
    return render(request,'codehub/innovation/innovation.html',{'form':form,'ideas':ideas,'search_form':search_form})


@loginRequired
def codehub_innovation_details(request,idea_id):
    if request.method == 'POST':
        form = CodehubInnovationCommentForm(request.POST)
        if form.is_valid():
            new_comment = CodehubInnovationCommentModel(
                user = request.user,
                innovation_post = get_object_or_404(CodehubInnovationPostModel,id = idea_id),
                comment_text = form.cleaned_data['comment_text']
            )
            new_comment.save()
            return redirect('/codehub/innovation/'+str(idea_id)+'/details')
    else:
        form = CodehubInnovationCommentForm()
    idea_details = get_object_or_404(CodehubInnovationPostModel,id = idea_id)
    comments_on_post = CodehubInnovationCommentModel.objects.filter(innovation_post_id = idea_id).order_by('-created')
    return render(request,'codehub/innovation/innovation_details.html',{'idea_details':idea_details,'form':form,'comments':comments_on_post})


#decorators for new ideas
def check_user_access_for_edit_ideas(func):
    def wrapper(request,idea_id,*args,**kwargs):
        idea_user = get_object_or_404(CodehubInnovationPostModel,id = idea_id).user.username
        if idea_user != request.user.username:
            return redirect('/')
        return func(request,idea_id,*args,**kwargs)
    return wrapper



@loginRequired
@check_user_access_for_edit_ideas
def edit_codehub_innovation_idea(request,idea_id):
    if request.method == 'POST':
        form = CodehubInnovationPostForm(request.POST)
        if form.is_valid():
            # idea_details = CodehubInnovationPostModel(id = idea_id)
            idea_details = get_object_or_404(CodehubInnovationPostModel,id = idea_id)
            form = CodehubInnovationPostForm(request.POST,instance = idea_details)
            form.save()
            return redirect('/codehub/innovation')
    else:
        tagArr = []
        idea_details = get_object_or_404(CodehubInnovationPostModel,id = idea_id)
        tags = idea_details.tags.all()
        for tag in tags:
            tagArr.append(tag.name)
        tags = ",".join(tagArr)
        idea_data = {'title':idea_details.title,'description':idea_details.description,'tags':tags}
        form = CodehubInnovationPostForm(initial = idea_data)
    return render(request,'codehub/innovation/edit_innovation_idea.html',{'form':form})


@loginRequired
@check_user_access_for_edit_ideas
def remove_codehub_innovation_idea(request,idea_id):
    idea_obj = get_object_or_404(CodehubInnovationPostModel,id = idea_id)
    idea_obj.delete()
    return redirect('/codehub/innovation')

#decorator for comment comes here
def check_user_access_for_innovation_comment_edit(func):
    def wrapper(request,idea_id,com_id,*args,**kwargs):
        comment_details = get_object_or_404(CodehubInnovationCommentModel,id = com_id)
        if comment_details.user.username != request.user.username:
            return redirect('/')
        return func(request,idea_id,com_id,*args,**kwargs)
    return wrapper



@loginRequired
@check_user_access_for_innovation_comment_edit
def edit_codehub_innovation_idea_comment(request,idea_id,com_id):
    if request.method == 'POST':
        form = CodehubInnovationCommentForm(request.POST)
        if form.is_valid():
            comment_details = get_object_or_404(CodehubInnovationCommentModel,id = com_id)
            form = CodehubInnovationCommentForm(request.POST,instance = comment_details)
            form.save()
            return redirect('/codehub/innovation/'+str(idea_id)+'/details')
    else:
        comment_details = get_object_or_404(CodehubInnovationCommentModel,id = com_id)
        comment_data = {'comment_text':comment_details.comment_text}
        form = CodehubInnovationCommentForm(initial = comment_data)
    return render(request,'codehub/innovation/edit_comment.html',{'form':form})



@loginRequired
@check_user_access_for_innovation_comment_edit
def remove_codehub_innovation_idea_comment(request,idea_id,com_id):
    comment_details = get_object_or_404(CodehubInnovationCommentModel,id = com_id)
    comment_details.delete()
    return redirect('/codehub/innovation/'+str(idea_id)+'/details')




@loginRequired
def search_codehub_innovation_post(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_str = form.cleaned_data['search_str']
            list_by_title = CodehubInnovationPostModel.objects.filter(title__contains = search_str)
            list_by_tags = CodehubInnovationPostModel.objects.filter(tags__name__in = [search_str])
            result_list = list(chain(list_by_title,list_by_tags))
            result_list = Set(result_list)
            search_form = SearchForm()
            return render(request,'codehub/innovation/search_idea.html',{'form':search_form,'results':result_list,'search_str':search_str})
    else:
        form = SearchForm()
    return render(request,'codehub/innovation/search_idea.html',{'form':form})
