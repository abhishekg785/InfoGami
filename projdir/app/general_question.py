from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
import datetime

from app.forms import GeneralQuestionForm,SearchForm
from app.models import GeneralQuestionModel,UserProfileModel

from itertools import chain
from sets import Set

def ask_general_question(request):
    question_form = GeneralQuestionForm()
    if request.method == 'POST':
        question_form = GeneralQuestionForm(request.POST)
        if question_form.is_valid():
            ques_tags = question_form.cleaned_data['ques_tags']
            new_question = GeneralQuestionModel(
                user = User.objects.get(id = request.user.id),
                user_profile = UserProfileModel.objects.get(user_id = request.user.id),
                ques_text = question_form.cleaned_data['ques_text'],
            )
            new_question.save()
            new_question.ques_tags.add(*ques_tags)
            return redirect('/general-question/ask')
    search_form = SearchForm()
    questions = GeneralQuestionModel.objects.all().order_by('-created')[:4]
    return render(request,'general_question/ask_question.html',{'question_form':question_form,'search_form':search_form,'questions':questions})



#search in the question text as well as in the question tags
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



def get_general_question_details(request,ques_id):
    question_result = get_object_or_404(GeneralQuestionModel,id = ques_id)
    return render(request,'general_question/question_details.html',{'ques_details':question_result})
