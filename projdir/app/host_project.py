from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User

from app.forms import HostProjectForm,SearchForm
from app.models import HostProjectModel,UserProfileModel,PingHostProjectModel
from app.codehub import do_pagination
from app.views import loginRequired

from taggit.models import Tag
from itertools import chain
from sets import Set


def check_project_active_or_not(func):
    def wrapper(request,project_id,*args,**kwargs):
        project_details = get_object_or_404(HostProjectModel,id = project_id)
        if project_details.project_status == 'deactive' and project_details.user.id != request.user.id:
            return redirect('/')
        return func(request,project_id,*args,**kwargs)
    return wrapper



@loginRequired
def work_collaborately(request):
    return render(request,'host_project/index.html')



@loginRequired
def host_project(request):
    if request.method  == 'POST':
        form = HostProjectForm(request.POST)
        if form.is_valid():
            skills = form.cleaned_data['skills']
            new_project = HostProjectModel(
                user = request.user,
                user_profile = UserProfileModel.objects.get(user_id = request.user.id),
                project_name = form.cleaned_data['project_name'],
                project_description = form.cleaned_data['project_description'],
            )
            new_project.save()
            new_project.skills.add(*skills)
            return redirect('/project/host-project/')
    else:
        form = HostProjectForm()
    search_form = SearchForm()
    projects = HostProjectModel.objects.filter(project_status = 'active').order_by('-created')[:5]
    return render(request,'host_project/host_project.html',{'form':form,'search_form':search_form,'projects':projects})




@loginRequired
def get_all_hosted_projects(request):
    project_list = HostProjectModel.objects.filter(project_status = 'active').order_by('-created')
    project_count = project_list.count()
    form = SearchForm()
    projects = do_pagination(request,project_list,5)
    return render(request,'host_project/get_all_projects.html',{'projects':projects,'form':form,'project_count':project_count})





@loginRequired
@check_project_active_or_not
def hosted_project_details(request,project_id):
    project_details = HostProjectModel.objects.get(id = project_id)
    try:
        ping = PingHostProjectModel.objects.get(hosted_project_id = project_id,user_id = request.user.id)
    except:
        ping = False
    return render(request,'host_project/project_details.html',{'project_details':project_details,'ping':ping})




def check_user_acess_for_project_edit(func):
    def wrapper(request,project_id,*args,**kwargs):
        project_details = get_object_or_404(HostProjectModel,id = project_id)
        if project_details.user.id != request.user.id:
            return redirect('/')
        return func(request,project_id,*args,**kwargs)
    return wrapper





@loginRequired
@check_user_acess_for_project_edit
def edit_hosted_project(request,project_id):
    project_details = get_object_or_404(HostProjectModel,id = project_id)
    if request.method == 'POST':
        form = HostProjectForm(request.POST)
        if form.is_valid():
            form = HostProjectForm(request.POST,instance = project_details)
            form.save()
            return redirect('/project/host-project/'+str(project_id)+'/details/')
    else:
        skillArr = []
        project_details = get_object_or_404(HostProjectModel,id = project_id)
        skills = project_details.skills.all()
        for skill in skills:
            skillArr.append(skill.name)
        skills = ','.join(skillArr)
        project_data = {'project_name':project_details.project_name,'project_description':project_details.project_description,'skills':skills}
        form = HostProjectForm(initial = project_data)
    return render(request,'host_project/edit_project.html',{'form':form,'project_name':project_details.project_name})





@loginRequired
@check_user_acess_for_project_edit
def remove_hosted_project(request,project_id):
    project_details = get_object_or_404(HostProjectModel,id = project_id)
    project_details.delete()
    return redirect('/project/host-project/')






def check_user_acess_to_activate_or_deactivate(func):
    def wrapper(request,project_id,*args,**kwargs):
        project_details = get_object_or_404(HostProjectModel,id = project_id)
        if project_details.user.id != request.user.id:
            return redirect('/')
        return func(request,project_id,*args,**kwargs)
    return wrapper





@loginRequired
@check_user_acess_to_activate_or_deactivate
def activate_hosted_project(request,project_id):
    project_details = get_object_or_404(HostProjectModel,id = project_id)
    if project_details.project_status == 'active':
        return redirect('/')
    elif project_details.project_status == 'deactive':
        project_details.project_status = 'active'
        project_details.save()
    return redirect('/project/host-project/'+str(project_id)+'/details/')






@loginRequired
@check_user_acess_to_activate_or_deactivate
def deactivate_hosted_project(request,project_id):
    project_details = get_object_or_404(HostProjectModel,id = project_id)
    if project_details == 'deactive':
        return redirect('/')
    elif project_details.project_status == 'active':
        project_details.project_status = 'deactive'
        project_details.save()
    return redirect('/project/host-project/'+str(project_id)+'/details/')





@loginRequired
def skill_matched_hosted_project(request):
    skillArr = []
    session_user_profile = UserProfileModel.objects.get(user_id = request.user.id)
    user_skills = session_user_profile.skills.all()
    for skill in user_skills:
        skillArr.append(skill.name)
    projects = HostProjectModel.objects.filter(skills__name__in = skillArr,project_status = 'active').exclude(user_id = request.user.id).distinct()
    project_count = projects.count()
    return render(request,'host_project/skill_matched_projects.html',{'projects':projects,'user_skills':user_skills,'project_count':project_count})






@loginRequired
def user_hosted_projects(request,user_id):
    user_details = User.objects.get(id = user_id)
    if user_id == str(request.user.id):
        user_projects = HostProjectModel.objects.filter(user_id = request.user.id)
    else:
        user_projects = HostProjectModel.objects.filter(user_id = user_id,project_status = 'active')
    return render(request,'host_project/user_hosted_projects.html',{'projects':user_projects,'user_details':user_details})





#check that the current user only pings the others and the active project
def check_user_access_for_ping_project(func):
    def wrapper(request,project_id,*args,**kwargs):
        project_details = get_object_or_404(HostProjectModel,id = project_id)
        if project_details.user.id == request.user.id or project_details.project_status == 'deactive':   #check that user does not ping its own and pings only active projects
            return redirect('/')
        return func(request,project_id,*args,**kwargs)
    return wrapper



#check that the user does not ping the same project again
@loginRequired
@check_user_access_for_ping_project
def ping_hosted_project(request,project_id):
    try:
        project_obj = PingHostProjectModel.objects.get(user_id = request.user.id,hosted_project_id = project_id)
        return redirect('/')
    except:
        new_ping = PingHostProjectModel(
            user = request.user,
            user_profile = UserProfileModel.objects.get(user_id = request.user.id),
            hosted_project = HostProjectModel.objects.get(id = project_id)
        )
        new_ping.save()
    return redirect('/project/host-project/'+str(project_id)+'/details/')





@loginRequired
def hosted_project_interested_users(request):
    print request.user.id
    projects = HostProjectModel.objects.filter(user_id = request.user.id,project_status ='active')
    if projects:
        project_dict = {project:[] for project in projects}
        print project_dict
        for project in projects:
            ping_project_obj = PingHostProjectModel.objects.filter(hosted_project_id = project.id)
            project_dict[project] = ping_project_obj
        return render(request,'host_project/interested_users.html',{'projects':projects,'project_dict':project_dict})
    else:
        return render(request,'host_project/interested_users.html',{'projects':False})





@loginRequired
def search_hosted_project(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_str = form.cleaned_data['search_str']
            list_by_name = HostProjectModel.objects.filter(project_status = 'active',project_name__contains = search_str)
            list_by_tags = HostProjectModel.objects.filter(project_status = 'active',skills__name__in = [search_str])
            result = list(chain(list_by_name,list_by_tags))
            result = Set(result)
            return render(request,'host_project/search_hosted_project.html',{'results':result,'form':form,'search_str':search_str})
    else:
        form = SearchForm()
    return render(request,'host_project/search_hosted_project.html',{'form':form})
