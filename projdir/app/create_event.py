from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User

from .forms import CodehubCreateEventForm,CodehubEventQuestionForm,SearchForm,ProposeEventForm
from .models import CodehubCreateEventModel,CodehubEventQuestionModel,UserProfileModel,ProposeEventModel,ProposeEventVoteModel
from .views import loginRequired
import datetime

from taggit.models import Tag
from itertools import chain
from sets import Set

from .codehub import do_pagination

def check_user_access_for_event_edit(func):
    def wrapper(request,event_id,*args,**kwargs):
        event_user = get_object_or_404(CodehubCreateEventModel,id = event_id).user.username
        if event_user != request.user.username:
            return redirect('/codehub/event/'+str(event_id)+'/details/')
        return func(request,event_id,*args,**kwargs)
    return wrapper


@loginRequired
def codehub_events(request):
    events_list = CodehubCreateEventModel.objects.all().order_by("-created")
    events = do_pagination(request,events_list,5)
    search_form = SearchForm()
    return render(request,'codehub/event/events.html/',{'events':events,'search_form':search_form})



@loginRequired
def codehub_event_details(request,event_id):
    if request.method == 'POST':
        form = CodehubEventQuestionForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username = request.user.username)
            event = get_object_or_404(CodehubCreateEventModel,id = event_id)
            new_question = CodehubEventQuestionModel(
                user = user,
                user_profile = UserProfileModel.objects.get(user_id = request.user.id),
                event = event,
                question_text = form.cleaned_data['question_text'],
            )
            new_question.save()
            print 'saved'
            #flash message
            return redirect('/codehub/event/'+str(event_id)+'/details/')
    else:
        form = CodehubEventQuestionForm()
    event_details = get_object_or_404(CodehubCreateEventModel,id = event_id)
    # event_questions = get_object_or_404(CodehubEventQuestionModel,event_id = event_id)
    event_questions = CodehubEventQuestionModel.objects.filter(event_id = event_id).order_by("-created")
    return render(request,'codehub/event/event_details.html',{'event':event_details,'form':form,'event_questions':event_questions})



@loginRequired
def create_codehub_event(request):
    if request.method == 'POST':
        form = CodehubCreateEventForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            new_event = CodehubCreateEventModel(
                user = request.user,
                user_profile = UserProfileModel.objects.get(user_id = request.user.id),
                event_heading = form.cleaned_data['event_heading'],
                event_date = form.cleaned_data['event_date'],
                event_venue = form.cleaned_data['event_venue'],
                event_description = form.cleaned_data['event_venue'],
                event_for = form.cleaned_data['event_for'],
            )
            new_event.save()
            new_event.tags.add(*tags)
            return redirect('/codehub/events')
            #flash message  for event created
            #return redirect('codehub_events')
    else:
        form = CodehubCreateEventForm()
    search_form = SearchForm()
    events = CodehubCreateEventModel.objects.all().order_by("-created")[:5]
    return render(request,'codehub/event/create_event.html',{'form':form,'events':events,'search_form':search_form})


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
        tagArr = []
        for tag in event_details.tags.all():
            tagArr.append(tag.name)
        tags = ",".join(tagArr)
        data = {'event_heading':event_details.event_heading,'event_date':event_details.event_date,'event_venue':event_details.event_venue,'event_description':event_details.event_description,'event_for':event_details.event_for,'tags':tags}
        form = CodehubCreateEventForm(initial = data)
    return render(request,'codehub/event/edit_event.html',{'form':form,'event_title':event_details.event_heading})


@loginRequired
@check_user_access_for_event_edit
def remove_codehub_event(request,event_id):
    get_object_or_404(CodehubCreateEventModel,id = event_id).delete()
    print 'event deleted'
    return redirect('/codehub/events')
    #flash message


#decorators for event_question comes here
def check_user_acess_for_question_edit(func):
    def wrapper(request,ques_id,*args,**kwargs):
        ques_details = get_object_or_404(CodehubEventQuestionModel,id = ques_id)
        event_id = ques_details.event.id
        if ques_details.user.username != request.user.username:
            return redirect('/codehub/event/'+str(event_id)+'/details/')
        return func(request,ques_id,*args,**kwargs)
    return wrapper


def check_user_access_for_question_remove(func):
    def wrapper(request,ques_id,*args,**kwargs):
        ques_details = get_object_or_404(CodehubEventQuestionModel,id = ques_id)
        event_id = ques_details.event.id
        event_user = ques_details.event.user.username
        print 'event_user',event_user
        ques_user = ques_details.user.username
        if event_user == request.user.username or ques_user == request.user.username:
            return func(request,ques_id,*args,**kwargs)
        else:
            return redirect('/codehub/event/'+str(event_id)+'/details/')
    return wrapper


#edit option should be available only to the creator of the question
@loginRequired
@check_user_acess_for_question_edit
def edit_codehub_event_question(request,ques_id):
    if request.method == 'POST':
        form = CodehubEventQuestionForm(request.POST)
        if form.is_valid():
            ques_details = get_object_or_404(CodehubEventQuestionModel,id = ques_id)
            event_id = ques_details.event.id
            form = CodehubEventQuestionForm(request.POST,instance = ques_details)
            form.save()
            print 'data updated'
            #flash message
            return redirect('/codehub/event/'+str(event_id)+'/details/')
    else:
        quest_details = get_object_or_404(CodehubEventQuestionModel,id = ques_id)
        ques_data = {'question_text':quest_details.question_text}
        form = CodehubEventQuestionForm(initial = ques_data)
    return render(request,'codehub/event/edit_event_question.html',{'form':form})



#decorator comes here
#remove option should be available only to the event creator and the user of the question
@loginRequired
@check_user_access_for_question_remove
def remove_codehub_event_question(request,ques_id):
    quest_details = get_object_or_404(CodehubEventQuestionModel,id = ques_id)
    event_id = quest_details.event.id
    quest_details.delete()
    print 'question deleted'
    return redirect('/codehub/event/'+str(event_id)+'/details/')


@loginRequired
def search_codehub_event(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_str = form.cleaned_data['search_str']
            event_by_name_list = CodehubCreateEventModel.objects.filter(event_heading__contains = search_str)
            event_by_tag_list = CodehubCreateEventModel.objects.filter(tags__name__in = [search_str])
            result_list = list(chain(event_by_name_list,event_by_tag_list))
            result_list = Set(result_list)
            form = SearchForm()
            return render(request,'codehub/event/search_event.html',{'search_form':form,'result':result_list,'search_str':search_str})
    else:
        form = SearchForm()
    return render(request,'codehub/event/search_event.html',{'search_form':form})



@loginRequired
def propose_event(request):
    if request.method == 'POST':
        form = ProposeEventForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            new_event = ProposeEventModel(
                user = request.user,
                user_profile = UserProfileModel.objects.get(user_id = request.user.id),
                event_heading = form.cleaned_data['event_heading'],
                event_description = form.cleaned_data['event_description'],
                event_type = form.cleaned_data['event_type']
            )
            new_event.save()
            new_event.tags.add(*tags)
            return redirect('/event/propose-event')
    else:
        form = ProposeEventForm()
    search_form = SearchForm()
    events = ProposeEventModel.objects.all().order_by('-created')[:5]
    return render(request,'propose_event/propose_event.html',{'form':form,'search_form':search_form,'events':events})


@loginRequired
def propose_event_details(request,event_id):
    event_details = ProposeEventModel.objects.get(id = event_id)
    try:
        voteStatus = ProposeEventVoteModel.objects.get(event_id = event_id,user_id = request.user.id)
    except:
        voteStatus = "none"
    up_vote_count = ProposeEventVoteModel.objects.filter(event_id = event_id,vote = 'upVote').count()
    down_vote_count = ProposeEventVoteModel.objects.filter(event_id = event_id,vote = 'downVote').count()
    return render(request,'propose_event/event_details.html',{'event':event_details,'voteStatus':voteStatus,'up_vote_count':up_vote_count,'down_vote_count':down_vote_count})


def check_downVoted_or_not(func):
    def wrapper(request,event_id,*args,**kwargs):
        try:
            ProposeEventVoteModel.objects.get(event_id = event_id,user_id = request.user.id,vote = 'downVote')
            return redirect('/')
        except:
            return func(request,event_id,*args,**kwargs)
    return wrapper

def check_upVoted_or_not(func):
    def wrapper(request,event_id,*args,**kwargs):
        try:
            ProposeEventVoteModel.objects.get(event_id = event_id,user_id = request.user.id,vote = 'upVote')
            return redirect('/')
        except:
            return func(request,event_id,*args,**kwargs)
    return wrapper


@loginRequired
@check_upVoted_or_not
def upVote_propose_event(request,event_id):
    try:
        down_vote_exists_or_not = ProposeEventVoteModel.objects.get(event_id = event_id,user_id = request.user.id ,vote = 'downVote')
        down_vote_exists_or_not.delete()
    except:
        print 'no downvote'
    event = get_object_or_404(ProposeEventModel,id = event_id)
    new_vote = ProposeEventVoteModel(
        user = request.user,
        user_profile = UserProfileModel.objects.get(user_id = request.user.id),
        event = event,
        vote = 'upVote'
    )
    new_vote.save()
    return redirect('/event/propose-event/'+str(event_id)+'/details')



@loginRequired
@check_downVoted_or_not
def downVote_propose_event(request,event_id):
    try:
        up_vote_exists_or_not = ProposeEventVoteModel.objects.get(event_id = event_id,user_id = request.user.id,vote = 'upVote')
        up_vote_exists_or_not.delete()
    except:
        print 'no upVote'
    event = get_object_or_404(ProposeEventModel,id = event_id)
    new_vote = ProposeEventVoteModel(
        user = request.user,
        user_profile = UserProfileModel.objects.get(user_id = request.user.id),
        event = event,
        vote = 'downVote'
    )
    new_vote.save()
    return redirect('/event/propose-event/'+str(event_id)+'/details')



@loginRequired
def propose_event_users_upvoted(request,event_id):
    event_details = get_object_or_404(ProposeEventModel,id = event_id)
    up_vote_users = ProposeEventVoteModel.objects.filter(event_id = event_id,vote = 'upVote').distinct()
    return render(request,'propose_event/up_vote_users.html',{'users':up_vote_users,'event_details':event_details})



@loginRequired
def propose_event_users_downvoted(request,event_id):
    pass



def check_user_acess_for_propose_event_edit(func):
    def wrapper(request,event_id,*args,**kwargs):
        event_details = get_object_or_404(ProposeEventModel,id = event_id)
        if event_details.user.id != request.user.id:
            return redirect('/')
        return func(request,event_id,*args,**kwargs)
    return wrapper



@loginRequired
@check_user_acess_for_propose_event_edit
def edit_propose_event(request,event_id):
    if request.method == 'POST':
        form = ProposeEventForm(request.POST)
        if form.is_valid():
            event_details = ProposeEventModel.objects.get(id = event_id)
            form = ProposeEventForm(request.POST,instance = event_details)
            form.save()
            print 'saved'
    else:
        tagArr = []
        event_details = ProposeEventModel.objects.get(id = event_id)
        for tag in event_details.tags.all():
            tagArr.append(tag.name)
        tags = ",".join(tagArr)
        event_data = {'event_heading':event_details.event_heading,'event_description':event_details.event_heading,'event_description':event_details.event_description,'tags':tags,'event_type':event_details.event_type}
        form = ProposeEventForm(initial = event_data)
    return render(request,'propose_event/edit_propose_event.html',{'form':form})




@loginRequired
@check_user_acess_for_propose_event_edit
def remove_propose_event(request,event_id):
    return HttpResponse(event_id)
