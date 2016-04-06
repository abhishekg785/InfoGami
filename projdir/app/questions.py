from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User

from .views import loginRequired
from .forms import CodehubQuestionForm

from .models import CodehubQuestionModel

@loginRequired
def codehub_question(request):
    if request.method == 'POST':
        form = CodehubQuestionForm(request.POST)
        if form.is_valid():
            new_ques = CodehubQuestionModel(
                user = request.user,
                question_heading = form.cleaned_data['question_heading'],
                question_description = form.cleaned_data['question_description'],
                question_link = form.cleaned_data['question_link'],
                question_tags = form.cleaned_data['question_tags'],
                question_type = form.cleaned_data['question_type']
            )
            new_ques.save()
            print 'data saved'
    else:
        form = CodehubQuestionForm()
    return render(request,'codehub/question/question.html',{'form':form})
