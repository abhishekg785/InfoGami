from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
import datetime

import operator
from django.db.models import Q

import json
import time

from app.codehub import loginRequired
from app.forms import TheInfoAddQueryForm,TheInfoQueryAnswerForm
from app.models import TheInfoAddQueryModel,UserProfileModel,TheInfoQueryAnswerModel,TheInfoQueryAnswerVoteModel

from slugify import slugify

from taggit.models import Tag
from itertools import chain
from sets import Set

@loginRequired
def the_info_main_page(request):
    if request.method == 'POST':
        answer_text = request.POST['answerText']
        form = TheInfoAddQueryForm(request.POST)
        if form.is_valid():
            print form.cleaned_data['queryTags']
            queryText = form.cleaned_data['queryText']
            queryTags = form.cleaned_data['queryTags']
            query_text_slug = slugify(queryText)
            query_word_arr = query_text_slug.split('-')
            minimized_word_arr = minimize_word_arr(query_word_arr)
            print minimized_word_arr
            query = reduce(operator.and_, (Q(queryText__contains = item) for item in minimized_word_arr))
            result = TheInfoAddQueryModel.objects.filter(query)
            print result
            if(result):
                return render(
                    request,
                    'theInfo/queryExists.html',
                    {
                        'query_text':queryText,
                        'matched_queries':result
                    }
                );
            new_query = TheInfoAddQueryModel(
                user = User.objects.get(id = request.user.id),
                user_profile = UserProfileModel.objects.get(user_id = request.user.id),
                queryText = queryText
            )
            new_query.save()
            new_query.queryTags.add(*queryTags)
            if answer_text:
                user_id = request.user.id
                answer_to_query = TheInfoQueryAnswerModel(
                    info_query = TheInfoAddQueryModel(id = new_query.id),
                    user = User.objects.get(id = user_id),
                    user_profile = UserProfileModel.objects.get(user_id = user_id),
                    answer_text = answer_text
                )
                answer_to_query.save()
            messages.success(request,'Query saved Successfully');
            return redirect('/theInfo/')
    query_form = TheInfoAddQueryForm()
    query_answer_form = TheInfoQueryAnswerForm()
    return render(request,'theInfo/main.html',{'queryForm':query_form,'queryAnswerForm':query_answer_form});   #main.html is the page having the search engine




"""
   found the results from the tags
   found the results matching the query text stored in db
"""
@loginRequired
def search_query(request):
    if request.method == 'POST':
        query_text = request.POST['query_text']
        query_text_slug = slugify(query_text)
        #logic for finding results comes here
        all_tags = TheInfoAddQueryModel.queryTags.all()
        query_word_arr = query_text_slug.split('-')
        #removing words
        minimized_word_arr = minimize_word_arr(query_word_arr)
        result_tags = TheInfoAddQueryModel.objects.filter(queryTags__name__in = minimized_word_arr).distinct()
        result_ques_text = TheInfoAddQueryModel.objects.filter(queryText__contains = query_text).distinct()
        minimize_word_arr_query = reduce(operator.and_, (Q(queryText__contains = item) for item in minimized_word_arr))
        result_minimized_word_arr = TheInfoAddQueryModel.objects.filter(minimize_word_arr_query)
        result_list = list(chain(result_tags,result_ques_text,result_minimized_word_arr))
        query_result_list = Set(result_list)
        response_arr = []
        for query in query_result_list:
            ans_arr = []   #ans_arr for each query
            tag_arr = []
            query_id = query.id
            query_text = query.queryText
            query_tags = query.queryTags.all()
            for tag in query_tags:
                tag_arr.append(tag.name)
            answers = TheInfoQueryAnswerModel.objects.filter(info_query_id = query_id)
            for ans in answers:
                ans_user_id = ans.user_id
                vote_status_for_logged_user = False
                ans_username = User.objects.get(id = ans_user_id).username
                #for finding votes to a answer
                answer_vote = TheInfoQueryAnswerVoteModel.objects.filter(answer_id = ans.id).count()
                #vote status of a logged user for a particular answer
                try:
                    result = TheInfoQueryAnswerVoteModel.objects.get(user_id = request.user.id, answer_id = ans.id)
                    if(result):
                        vote_status_for_logged_user = True
                except:
                    vote_status_for_logged_user = False
                ans_obj = {'ans_text':ans.answer_text,'ans_vote':answer_vote,'ans_id':ans.id,'ans_username':ans_username,'ans_user_id':ans_user_id,'vote_status_for_logged_user':vote_status_for_logged_user}
                ans_arr.append(ans_obj)
            query_obj = {'query_id':query_id,'query_text':query_text,'query_tags':tag_arr,'query_answers':ans_arr}
            response_arr.append(query_obj)
        return HttpResponse(json.dumps(response_arr),content_type = 'application/json')



def minimize_word_arr(word_arr):
    extras = ['or','and','is','there','best','the','for','what']
    for ext in extras:
        if ext in word_arr:
            word_arr.remove(ext)
    return word_arr




#check that user does not vote twice
# if user exists then just return answer vote count
# if not then insert the user and vote into the model and return count
@loginRequired
def vote_query_answer(request):
    if request.method == 'POST':
        ans_id = request.POST['answer_id']
        try:
            result = TheInfoQueryAnswerVoteModel.objects.get(user_id = request.user.id,answer_id = ans_id)
            if(result):
                vote_count = TheInfoQueryAnswerVoteModel.objects.filter(answer_id = ans_id).count()
                vote_obj = {'newVoteCount':vote_count}
        except:
            #user has not Voted
            new_vote = TheInfoQueryAnswerVoteModel(
                user = User.objects.get(id = request.user.id),
                user_profile = UserProfileModel.objects.get(user_id = request.user.id),
                answer = TheInfoQueryAnswerModel.objects.get(id = ans_id)
            )
            new_vote.save()
            new_vote_count = TheInfoQueryAnswerVoteModel.objects.filter(answer_id = ans_id).count()
            vote_obj = {'newVoteCount':new_vote_count}
        return HttpResponse(json.dumps(vote_obj),content_type = 'application/json')
    return render(request,'404.html');



@loginRequired
def undo_answer_vote(request):
    if request.method == 'POST':
        ans_id = request.POST['answer_id']
        try:
            result = TheInfoQueryAnswerVoteModel.objects.get(answer_id = ans_id,user_id = request.user.id)
            if(result):
                result.delete()
                new_vote_count = TheInfoQueryAnswerVoteModel.objects.filter(answer_id = ans_id).count()
                vote_obj = {'newVoteCount':new_vote_count}
                return HttpResponse(json.dumps(vote_obj),content_type = 'application/json')
        except:
            vote_count = TheInfoQueryAnswerVoteModel.objects.filter(answer_id = ans_id).count()
            vote_obj = {'newVoteCount':vote_count}
            return HttpResponse(json.dumps(vote_obj),content_type = 'application/json')
    return render(request,'404.html')



@loginRequired
def query_details(request, query_id):
    if request.method == 'POST':
        form = TheInfoQueryAnswerForm(request.POST)
        if form.is_valid():
            answer_text = form.cleaned_data['answerText']
            new_answer = TheInfoQueryAnswerModel(
                info_query = TheInfoAddQueryModel.objects.get(id = query_id),
                user = User.objects.get(id = request.user.id),
                user_profile = UserProfileModel.objects.get(user_id = request.user.id),
                answer_text = answer_text
            )
            new_answer.save()
            messages.success(request,'Answer saved Successfully');
            return redirect("/theInfo/query/" + query_id +"/details/")
    answer_form = TheInfoQueryAnswerForm()
    query = TheInfoAddQueryModel.objects.get(id = query_id)
    answers = TheInfoQueryAnswerModel.objects.filter(info_query_id = query.id)
    answers_count = answers.count()
    response_obj = []
    for ans in answers:
        vote_count = TheInfoQueryAnswerVoteModel.objects.filter(answer_id = ans.id).count()
        try:
            result = TheInfoQueryAnswerVoteModel.objects.get(answer_id = ans.id , user_id = request.user.id)
            if(result):
                logged_user_vote_status = True
        except:
            logged_user_vote_status = False
        ans_obj = {'answer_text':ans.answer_text,'vote_count':vote_count,'answer_id':ans.id,'answer_user_id':ans.user.id,'ans_user_name':ans.user.username,'vote_status':logged_user_vote_status}
        response_obj.append(ans_obj)
    answer_count = len(response_obj)
    return render(request,'theInfo/query_details.html',{'answer_obj':response_obj,'answer_form':answer_form,'query':query,'answer_count':answer_count})



@loginRequired
def query_records(request):
    queries = TheInfoAddQueryModel.objects.all().order_by('-created')
    return render(request,'theInfo/queryRecords.html',{'queries':queries})
