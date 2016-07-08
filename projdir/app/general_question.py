from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
import datetime

from app.forms import GeneralQuestionForm,SearchForm,GeneralQuestionAnsweForm,GeneralQuestionAnswerModel
from app.models import GeneralQuestionModel,UserProfileModel

from itertools import chain
from sets import Set

from app.codehub import loginRequired,do_pagination

#decorators defined here'
def check_user_acess_to_edit_question(func):
    def wrapper(request,ques_id,*args,**kwargs):
        ques_details = get_object_or_404(GeneralQuestionModel,id = ques_id)
        if ques_details.user.username != request.user.username:
            return redirect('/')
        return func(request,ques_id,*args,**kwargs)
    return wrapper



def check_user_acess_for_question_answer_edit(func):
    def wrapper(request,ques_id,ans_id,*args,**kwargs):
        ans_obj = get_object_or_404(GeneralQuestionAnswerModel,id = ans_id)
        if ans_obj.user.username != request.user.username:
            return redirect('/')
        return func(request,ques_id,ans_id,*args,**kwargs)
    return wrapper



@loginRequired
def ask_general_question(request):
    question_form = GeneralQuestionForm()
    if request.method == 'POST':
        question_form = GeneralQuestionForm(request.POST)
        if question_form.is_valid():
            ques_tags = question_form.cleaned_data['ques_tags']
            print ques_tags
            new_question = GeneralQuestionModel(
                user = User.objects.get(id = request.user.id),
                user_profile = UserProfileModel.objects.get(user_id = request.user.id),
                ques_text = question_form.cleaned_data['ques_text'],
            )
            new_question.save()
            new_question.ques_tags.add(*ques_tags)
            messages.success(request,'Question posted Successfully')
            return redirect('/general-question/ask')
    search_form = SearchForm()
    questions = GeneralQuestionModel.objects.all().order_by('-created')[:4]
    return render(request,'general_question/ask_question.html',{'form':question_form,'search_form':search_form,'questions':questions})



#search in the question text as well as in the question tags
@loginRequired
def search_general_question(request):
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_str = form.cleaned_data['search_str']
            text_search_result = GeneralQuestionModel.objects.filter(ques_text__contains = search_str).order_by('-created')
            tag_search_result = GeneralQuestionModel.objects.filter(ques_tags__name__in = search_str).order_by('-created')
            results = list(chain(text_search_result,tag_search_result))
            results = Set(results)
            return render(request,'general_question/search_question.html',{'form':form,'results':results,'search_str':search_str});
    return render(request,'general_question/search_question.html',{'form':form})




@loginRequired
def get_general_question_details(request,ques_id):
    if request.method == 'POST':
        ans_form = GeneralQuestionAnsweForm(request.POST)
        if ans_form.is_valid():
            new_answer = GeneralQuestionAnswerModel(
              user = User.objects.get(id = request.user.id),
              user_profile = UserProfileModel.objects.get(user_id = request.user.id),
              question = GeneralQuestionModel.objects.get(id = ques_id),
              answer_text = ans_form.cleaned_data['answer_text']
            )
            new_answer.save()
            return redirect('/general-question/question/'+ str(ques_id) +'/details/')
    question_result = get_object_or_404(GeneralQuestionModel,id = ques_id)
    ans_form = GeneralQuestionAnsweForm()
    answers = GeneralQuestionAnswerModel.objects.filter(question_id = ques_id).order_by('-created')
    return render(request,'general_question/question_details.html',{'ques_details':question_result,'ans_form':ans_form,'answers':answers})





@loginRequired
@check_user_acess_to_edit_question
def edit_general_question(request,ques_id):
    form = GeneralQuestionForm()
    if request.method == 'POST':
        form = GeneralQuestionForm(request.POST)
        if form.is_valid():
            ques_details = get_object_or_404(GeneralQuestionModel,id = ques_id)
            form = GeneralQuestionForm(request.POST,instance = ques_details)
            form.save()
            messages.success(request,'Question Edited Successfully')
            return redirect('/general-question/question/'+ str(ques_id) +'/details/')
    ques_details = get_object_or_404(GeneralQuestionModel,id = ques_id)
    ques_tags = ques_details.ques_tags.all()
    ques_tag_arr = []
    for tag in ques_tags.all():
        ques_tag_arr.append(tag.name)
    ques_tags_str = ",".join(ques_tag_arr)
    ques_details_obj = {'ques_text':ques_details.ques_text,'ques_tags':ques_tags_str}
    form = GeneralQuestionForm(initial = ques_details_obj)
    return render(request,'general_question/edit_general_question.html',{'form':form})




@loginRequired
@check_user_acess_to_edit_question
def remove_general_question(request,ques_id):
    try:
        ques_obj = get_object_or_404(GeneralQuestionModel,id = ques_id,user_id = request.user.id)
        ques_obj.delete()
        messages.success(request,'Question deleted Successfully')
    except:
        messages.error(request,'Error Occurred:Try Again!!!')
        return redirect('/')
    return redirect('/general-question/ask');




@loginRequired
@check_user_acess_for_question_answer_edit
def edit_general_question_answer(request,ques_id,ans_id):
    if request.method == 'POST':
        ans_form = GeneralQuestionAnsweForm(request.POST)
        if ans_form.is_valid():
            ans_obj = get_object_or_404(GeneralQuestionAnswerModel,id = ans_id,question_id = ques_id,user_id = request.user.id)
            ans_form = GeneralQuestionAnsweForm(request.POST, instance = ans_obj)
            ans_form.save()
            messages.success(request,'Answer edited Successfully')
            return redirect('/general-question/question/'+ ques_id +'/details/')
    try:
        ans_details = get_object_or_404(GeneralQuestionAnswerModel,id = ans_id,user_id = request.user.id,question_id = ques_id)
        ans_obj = {'answer_text':ans_details.answer_text}
        ans_form = GeneralQuestionAnsweForm(initial = ans_obj)
        return render(request,'general_question/edit_general_question_answer.html',{'ans_form':ans_form,'ques_id':ques_id})
    except:
        return redirect('/')




@loginRequired
@check_user_acess_for_question_answer_edit
def remove_general_question_answer(request,ques_id,ans_id):
    try:
        ans_obj = get_object_or_404(GeneralQuestionAnswerModel,id = ans_id,user_id = request.user.id,question_id = ques_id)
        ans_obj.delete()
        messages.success(request,'Answer deleted Successfully')
    except:
        return redirect('/')
    return redirect('/general-question/question/'+ str(ques_id) +'/details/')




def get_all_general_questions(request):
    question_list = GeneralQuestionModel.objects.all().order_by('-created')
    questions = do_pagination(request,question_list,5)
    question_count = question_list.count()
    return render(request,'general_question/get_all_questions.html',{'questions':questions,'question_count':question_count})
