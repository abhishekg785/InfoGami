"""
  author: abhishek goswami
  abhishekg785@gmail.com

"""

from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
import datetime
from django.utils.datastructures import MultiValueDictKeyError


from .forms import CreateUserGroupForm,SearchForm,GroupUserCommentForm
from app.models import CreateUserGroupModel,UserProfileModel,GroupUsersInterestTrackModel,MesssageModel,GroupUserCommentModel
from app.codehub import loginRequired

from slugify import slugify
import operator
from django.db.models import Q
from itertools import chain
from sets import Set
import json


#decorators come here
def check_user_access_for_edit_group(func):
    def wrapper(request,group_id,*args,**kwargs):
        group_details = get_object_or_404(CreateUserGroupModel,id = group_id)
        if group_details.user.username != request.user.username:
            return redirect('/')
        return func(request,group_id,*args,**kwargs)
    return wrapper



#prevent the owner of the group to send the request to join
#prevent joining closed groups
#prevent joining twice or more
def check_user_access_to_join_group(func):
    def wrapper(request,group_id,*args,**kwargs):
        try:
            GroupUsersInterestTrackModel.objects.get(group_id = group_id,user_id = request.user.id)
            return redirect('/')
        except:
            print 'unique case'
        group_details = get_object_or_404(CreateUserGroupModel,id = group_id)
        if str(group_details.user.id) == str(request.user.id) or group_details.group_status == 'deactive':
            return redirect('/')
        return func(request,group_id,*args,**kwargs)
    return wrapper


def check_user_access_to_remove_from_group(func):
    def wrapper(request,group_id,user_id,*args,**kwargs):
        group_details = get_object_or_404(CreateUserGroupModel,id = group_id)
        if group_details.user.id != request.user.id:
            return redirect('/')
        return func(request,group_id,user_id,*args,**kwargs)
    return wrapper



@loginRequired
def create_group_main_page(request):
    form = CreateUserGroupForm()
    if request.method == 'POST':
        group_name = request.POST['group_name']
        # CreateUserGroupModel.objects.get(group_name = group_name)
        try:
            CreateUserGroupModel.objects.get(group_name = group_name)
            messages.warning(request,'The group name already exists')
            return redirect('/group/create')
        except:
            form = CreateUserGroupForm(request.POST)
            if form.is_valid():
                tags = form.cleaned_data['group_tags']
                new_group = CreateUserGroupModel(
                    user = User.objects.get(id = request.user.id),
                    user_profile = UserProfileModel.objects.get(user_id = request.user.id),
                    group_name = form.cleaned_data['group_name'],
                    group_description = form.cleaned_data['group_description']
                )
                new_group.save()
                new_group.group_tags.add(*tags)
                messages.success(request,'Group created Successfully')
                return redirect('/group/create')
    groups = CreateUserGroupModel.objects.all().order_by('-created')
    search_form = SearchForm()
    return render(request,'create_group/create_group.html',{'form':form,'groups':groups,'search_form':search_form})



@loginRequired
def get_user_created_groups(request,user_id):
    pass


@loginRequired
def search_group(request):
    suggestions = find_suggestions_for_user(request)
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_str = form.cleaned_data['search_str']
            search_str_slug = slugify(search_str);
            group_name_search_result = CreateUserGroupModel.objects.filter(group_name__contains = search_str)
            minimized_word_arr = minimize_arr(search_str_slug)
            tag_search_result = CreateUserGroupModel.objects.filter(group_tags__name__in = minimized_word_arr)
            query = reduce(operator.and_, (Q(group_name__contains = item) for item in minimized_word_arr))
            topic_name_minimized_search_result = CreateUserGroupModel.objects.filter(query)
            result_list = list(chain(group_name_search_result,tag_search_result,topic_name_minimized_search_result))
            result_list = Set(result_list)  #removes duplicates
            return render(request,'create_group/search_group.html',{'search_form':form,'search_str':search_str,'results':result_list,'suggestions':suggestions})
    return render(request,'create_group/search_group.html',{'search_form':form,'suggestions':suggestions})





def minimize_arr(search_str_slug):
    exclude = ['group','groups','the']
    minimized_word_arr = search_str_slug.split('-')
    for ext in exclude:
        if ext in minimized_word_arr:
            minimized_word_arr.remove(ext)
    return minimized_word_arr




"""
 remove the groups created by the user itself in the suggestions
"""
@loginRequired
def find_suggestions_for_user(request):
    user_skill_arr = []
    user_skills = UserProfileModel.objects.get(user_id = request.user.id).skills.all()
    for skill in user_skills:
        user_skill_arr.append(skill.name)
    user_group_arr = find_group_users(request)
    suggestions = CreateUserGroupModel.objects.filter(group_tags__name__in = user_skill_arr).exclude(user_id = request.user.id).exclude(group_name__in = user_group_arr).distinct()
    return suggestions



"""
return me the array of groups user is part of
"""
@loginRequired
def find_group_users(request):
    group_arr = []
    groups = GroupUsersInterestTrackModel.objects.filter(user_id = request.user.id,request_status = 'accepted').distinct()
    for group in groups:
        group_arr.append(group.group.group_name)
    return group_arr


@loginRequired
def get_group_details(request,group_id):
    form = GroupUserCommentForm()
    if request.method == 'POST':
        form = GroupUserCommentForm(request.POST)
        if form.is_valid():
            comment_text = request.POST['comment_text']
            new_comment = GroupUserCommentModel(
                user = User.objects.get(id = request.user.id),
                user_profile = UserProfileModel.objects.get(user_id = request.user.id),
                group = CreateUserGroupModel.objects.get(id = group_id),
                comment_text = comment_text
            )
            new_comment.save()
            messages.success(request,'Comment posted Successfully')
            return redirect('/group/'+str(group_id)+'/details')
    group_details = get_object_or_404(CreateUserGroupModel,id = group_id)
    try:
        user_group_status_details = GroupUsersInterestTrackModel.objects.get(group_id = group_id,user_id = request.user.id)
        user_group_request_status = user_group_status_details.request_status
        print user_group_request_status
    except:
        user_group_request_status = False
    comments = GroupUserCommentModel.objects.filter(group_id = group_id).order_by('-created')
    return render(request,'create_group/group_details.html',{'group_details':group_details,'user_request_status':user_group_request_status,'comment_form':form,'comments':comments})





@loginRequired
@check_user_access_for_edit_group
def edit_group_details(request,group_id):
    group_details = get_object_or_404(CreateUserGroupModel,id = group_id,user_id = request.user.id)
    if request.method == 'POST':
        form = CreateUserGroupForm(request.POST)
        if form.is_valid():
            initial_group_details = get_object_or_404(CreateUserGroupModel,id = group_id,user_id = request.user.id)
            form = CreateUserGroupForm(request.POST,instance = initial_group_details)
            form.save()
            messages.success(request,'Group details edited Successfully')
            return redirect('/group/' + str(group_id) + '/details')
    else:
        group_tag_arr = []
        group_tags = group_details.group_tags.all()
        for tag in group_tags:
            group_tag_arr.append(tag.name)
        group_tag_str = ",".join(group_tag_arr)
        group_obj = {'group_name':group_details.group_name,'group_description':group_details.group_description,'group_tags':group_tag_str}
        form = CreateUserGroupForm(initial = group_obj)
    return render(request,'create_group/edit_group_details.html',{'form':form,'group_name':group_details.group_name})




@check_user_access_to_join_group
@loginRequired
def user_request_for_group(request,group_id):
    group_obj = get_object_or_404(CreateUserGroupModel,id = group_id)
    user_profile_obj = UserProfileModel.objects.get(user_id = request.user.id)
    user_obj = User.objects.get(id = request.user.id)
    new_request = GroupUsersInterestTrackModel(
       user = user_obj,
       user_profile = user_profile_obj,
       group = group_obj,
       request_status = 'waiting',
    )
    new_request.save()
    return redirect('/group/'+str(group_id)+'/details')




"""
check whether grop exists and is active
"""
def deactivate_group(request,group_id):
    try:
        group_obj = CreateUserGroupModel.objects.get(id = group_id,user_id = request.user.id,group_status = 'active')
        group_obj.group_status = 'deactive'
        group_obj.save()
        messages.success(request,'Group deactivated Successfully')
        return redirect('/group/'+str(group_id)+'/details')
    except:
        messages.warning(request,'Not allowed')
        return redirect('/')



def activate_group(request,group_id):
    try:
        group_obj = CreateUserGroupModel.objects.get(id = group_id,user_id = request.user.id,group_status = 'deactive')
        group_obj.group_status = 'active'
        group_obj.save()
        messages.success(request,'Group activated Successfully')
        return redirect('/group/'+str(group_id)+'/details')
    except:
        messages.success(request,'Not allowed')
        return redirect('/')



"""
get all the user created groups
"""
def get_group_dashboard(request):
    groups = CreateUserGroupModel.objects.filter(user_id = request.user.id)
    group_user_dict = {group:'' for group in groups}
    for group in groups:
        interested_users = GroupUsersInterestTrackModel.objects.filter(group_id = group.id)
        group_user_dict[group] = interested_users
    print group_user_dict
    # group_user_count = GroupUsersInterestTrackModel.objects.filter(group_id = group_id,request_status = 'accepted').count()
    return render(request,'create_group/group_dashboard.html',{'group_user_dict':group_user_dict})




"""
  check user access
  check user doing this is the owner of the group: request.user.id == group.user.id
  otherwise redirect him somewhere
"""

@check_user_access_to_remove_from_group
def remove_or_reject_user_from_group(request,group_id,user_id):
    try:
        group_obj = GroupUsersInterestTrackModel.objects.get(group_id = group_id,user_id = user_id)
        group_obj.delete()
        messages.success(request,'The user was Successfully removed')
        return redirect('/group/dashboard')
    except:
        messages.success(request,'No such thing exists')
        return redirect('/')




@check_user_access_to_remove_from_group
def accept_user_join_request(request,group_id,user_id):
    try:
        group_obj = GroupUsersInterestTrackModel.objects.get(group_id = group_id,user_id = user_id,request_status = 'waiting')
        group_obj.request_status = 'accepted'
        group_obj.save()
        messages.success(request,'User Successfully added to the group')
        return redirect('/group/dashboard')
    except:
        messages.success(request,'No such thing exists')
        return redirect('/')




def send_message_to_group_members_api(request):
    message_text = request.POST['messageText']
    success_msg = {'message':'success'}
    error_msg = {'message':'nouser'}
    group_id = request.POST['group_id']
    group_details = CreateUserGroupModel.objects.get(id = group_id)
    group_owner = group_details.user
    group_users = GroupUsersInterestTrackModel.objects.filter(group_id = group_id,request_status = 'accepted')
    if len(group_users) > 0:
        for user in group_users:
            new_message = MesssageModel(
              sender = group_owner,
              receiver = User.objects.get(id = user.user_id),
              sender_profile = UserProfileModel.objects.get(user_id = group_owner.id),
              receiver_profile = UserProfileModel.objects.get(user_id = user.user_id),
              message_text = 'Message regarding group "'+ group_details.group_name +'":' + message_text
            )
            new_message.save()
            # messages.success(request,'Message sent Successfully to group members')
        return HttpResponse(json.dumps(success_msg),content_type = 'application/json')
    else:
        return HttpResponse(json.dumps(error_msg),content_type = 'application/json')



def edit_group_comment(request,group_id,comment_id):
    try:
        comment_obj = GroupUserCommentModel.objects.get(id = comment_id,group_id = group_id,user_id = request.user.id)
        comment_details_obj = {'comment_text':comment_obj.comment_text}
    except:
        messages.success('No such thing exists')
        return redirect('/')
    if request.method == 'POST':
        form = GroupUserCommentForm(request.POST)
        if form.is_valid():
            form = GroupUserCommentForm(request.POST,instance = comment_obj)
            form.save()
            messages.success(request,'Comment edited Successfully')
            return redirect('/group/'+str(group_id)+'/details')
    else:
        form = GroupUserCommentForm(initial = comment_details_obj)
    return render(request,'create_group/edit_group_comment.html',{'form':form,'group_id':group_id,'comment_text':comment_obj.comment_text})



def remove_group_comment(request,group_id,comment_id):
    try:
        comm_obj = GroupUserCommentModel.objects.get(id = comment_id,group_id = group_id,user_id = request.user.id)
        comm_obj.delete()
        messages.success(request,'comment has been deleted Successfully')
        return redirect('/group/'+ str(group_id)+'/details')
    except:
        messages.warning(request,'No such thing exists')
        return redirect("/")
