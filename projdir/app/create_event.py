from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User

from .forms import CodehubCreateEventForm,CodehubEventQuestionForm
from .models import CodehubCreateEventModel
from .views import loginRequired
import datetime

def check_user_access_for_event_edit(func):
    def wrapper(request,event_id,*args,**kwargs):
        event_user = get_object_or_404(CodehubCreateEventModel,id = event_id).user.username
        if event_user != request.user.username:
            return redirect('/')
        return func(request,event_id,*args,**kwargs)
    return wrapper


@loginRequired
def codehub_events(request):
    events = CodehubCreateEventModel.objects.all().order_by("-timeStamp")
    return render(request,'codehub/events.html/',{'events':events})

@loginRequired
def codehub_event_details(request,event_id):
    form = CodehubEventQuestionForm()
    event_details = get_object_or_404(CodehubCreateEventModel,id = event_id)
    return render(request,'codehub/event_details.html',{'event':event_details,'form':form})

@loginRequired
def create_codehub_event(request):
    if request.method == 'POST':
        form = CodehubCreateEventForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username = request.user.username)
            new_event = CodehubCreateEventModel(
                user = user,
                event_heading = form.cleaned_data['event_heading'],
                event_date = form.cleaned_data['event_date'],
                event_venue = form.cleaned_data['event_venue'],
                event_description = form.cleaned_data['event_venue'],
                event_for = form.cleaned_data['event_for'],
                timeStamp = datetime.datetime.now()
            )
            new_event.save()
            return redirect('/codehub/events')
            #flash message  for event created
            #return redirect('codehub_events')
    else:
        form = CodehubCreateEventForm()
    return render(request,'codehub/create_event.html',{'form':form})


@loginRequired
@check_user_access_for_event_edit
def edit_codehub_event(request,event_id):
    if request.method == 'POST':
        form = CodehubCreateEventForm(request.POST)
        if form.is_valid():
            event_details = get_object_or_404(CodehubCreateEventModel,id = event_id)
            form = CodehubCreateEventForm(request.POST,instance = event_details)
            form.save()
            #flash message here
            return redirect('/codehub/events')
    else:
        event_details = get_object_or_404(CodehubCreateEventModel,id = event_id)
        data = {'event_heading':event_details.event_heading,'event_date':event_details.event_date,'event_venue':event_details.event_venue,'event_description':event_details.event_description,'event_for':event_details.event_for}
        form = CodehubCreateEventForm(initial = data)
    return render(request,'codehub/edit_event.html',{'form':form})


@loginRequired
@check_user_access_for_event_edit
def remove_codehub_event(request,event_id):
    get_object_or_404(CodehubCreateEventModel,id = event_id).delete()
    print 'event deleted'
    return redirect('/codehub/events')
    #flash message

@loginRequired
def codehub_event_question(request,event_id):
