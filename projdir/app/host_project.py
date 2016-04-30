from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User

from app.forms import HostProjectForm,SearchForm
from app.models import HostProjectModel,UserProfileModel
from app.codehub import do_pagination
from app.views import loginRequired


def check_project_active_or_not(func):
    def wrapper(request,project_id,*args,**kwargs):
        project_details = get_object_or_404(HostProjectModel,id = project_id)
        if project_details.project_status == 'deactive' and project_details.user.id != request.user.id:
            return redirect('/')
        return func(request,project_id,*args,**kwargs)
    return wrapper



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
            print 'saved'
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
    return render(request,'host_project/project_details.html',{'project_details':project_details})




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
