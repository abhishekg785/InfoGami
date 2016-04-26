from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
import datetime

from app.codehub import  loginRequired

from app.forms import DevhubQuestionForm,SearchForm
from app.models import DevhubQuestionModel,UserProfileModel
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
    return render(request,'devhub/ask_question.html',{'form':form,'questions':questions,'search_form':search_form})



@loginRequired
def devhub_question_details(request,ques_id):
    ques_details = get_object_or_404(DevhubQuestionModel,id = ques_id)
    return render(request,'devhub/ques_details.html',{'ques_details':ques_details})

#decorator for checking user access for question edit and remove
def check_user_access_for_question_edit():
    def wrapper(request,ques_id,*args,**kwargs):
        DevhubQuestionModel.objects.get(id = ques_id)


@loginRequired
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
    return render(request,'devhub/edit_question.html',{'form':form,'ques_heading':ques_details.question_heading})


@loginRequired
def remove_devhub_question(request,ques_id):
    ques_details = DevhubQuestionModel.objects.get(id = ques_id)
    ques_details.delete()
    print 'deleted'

@loginRequired
def get_all_devhub_questions(request):
    pass



def search_devhub_question(request):
    pass
