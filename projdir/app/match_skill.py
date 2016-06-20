from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User

from app.models import UserProfileModel

from app.codehub import loginRequired
import json





@loginRequired
def get_all_users_skill_count_arr(request):
    all_skills = UserProfileModel.skills.all()
    total_users = User.objects.all().count()
    skill_count_arr = []  # have the count of users in a particular skill
    for skill in all_skills:
        skill_user_count = UserProfileModel.objects.filter(skills__name__in = [skill]).count()
        obj = {'skill':skill.name,'count':skill_user_count}
        skill_count_arr.append(obj)
    return skill_count_arr





@loginRequired
def get_all_users_skill_percent_arr(request):
    all_skills = UserProfileModel.skills.all()
    total_users = User.objects.all().count()
    skill_per_arr = []
    for skill in all_skills:
        skill_user_count = UserProfileModel.objects.filter(skills__name__in = [skill]).count()
        skill_user_per = (skill_user_count / float(total_users))*100
        skill_user_per = round(skill_user_per,2)
        obj = {'skill':skill.name,'count':skill_user_per}
        skill_per_arr.append(obj)
    return skill_per_arr




@loginRequired
def match_user_skills(request):
    total_user_count = User.objects.all().count()
    logged_user_profile = UserProfileModel.objects.get(user_id = request.user.id)
    logged_user_skills = logged_user_profile.skills.all()
    skill_user_count_dict = {skill:'' for skill in logged_user_skills}   #have the count of the users having the skills
    skill_user_per_dict =  {skill:'' for skill in logged_user_skills}   #have the percentile of the user having the skills
    logged_user_skills_arr = []
    for skill in logged_user_skills:
        logged_user_skills_arr.append(skill)
    matched_users_list = UserProfileModel.objects.filter(skills__name__in = logged_user_skills_arr).exclude(user_id = request.user.id).distinct()
    for skill in logged_user_skills_arr:
        skill_user_count = UserProfileModel.objects.filter(skills__name__in = [skill]).count()
        skill_user_per = (skill_user_count/float(total_user_count)) * 100
        skill_user_per_round = round(skill_user_per,2)
        skill_user_count_dict[skill] = skill_user_count
        skill_user_per_dict[skill] = skill_user_per_round
    return render(request,'match_skill/match_user_skills.html',{'logged_user_skills':logged_user_skills_arr,'matched_users_list':matched_users_list,'skill_user_count_dict':skill_user_count_dict,'skill_user_per_dict':skill_user_per_dict})



@loginRequired
def search_users_by_skill(request,skill_slug_str):
    result = UserProfileModel.objects.filter(skills__slug = skill_slug_str)
    return render(request,'match_skill/search_users_by_skill.html',{'result':result,'skill_search_str':skill_slug_str})




@loginRequired
def get_all_skills_stat(request):
    all_skills = UserProfileModel.skills.all()
    total_users = User.objects.all().count()
    skill_count_dict = { skill: '' for skill in all_skills }  # have the count of users in a particular skill
    skill_per_dict = {skill: '' for skill in all_skills }  #have the percentage of peoples having same skill
    for skill in all_skills:
        skill_user_count = UserProfileModel.objects.filter(skills__name__in = [skill]).count()
        skill_user_per = (skill_user_count / float(total_users))*100
        round_skill_per = round(skill_user_per,2)
        skill_count_dict[skill] = skill_user_count
        skill_per_dict[skill] = round_skill_per
    # print skill_count_dict
    # print skill_per_dict
    return render(request,'match_skill/get_all_skills_stat.html',{'skill_count_dict':skill_count_dict,'skill_per_dict':skill_per_dict})





#apis for getting a json response for skills statstics
@loginRequired
def get_all_skills_stat_apiv1(request):
    #get user stats
    skill_count_arr = get_all_users_skill_percent_arr(request)
    return HttpResponse(json.dumps(skill_count_arr),content_type = 'application/json')





#api for getting skill statistsics according to a user
def get_user_skills_stat_apiv1(request,user_id):
    user_skill_stat_arr = []
    total_user_count = User.objects.all().count()
    user_skills = UserProfileModel.objects.get(user_id  = user_id).skills.all()
    for skill in user_skills:
        skill_count = UserProfileModel.objects.filter(skills__name__in = [skill]).count()
        skill_per  = (skill_count / float(total_user_count))*100
        skill_per = round(skill_per,2)
        obj = {'skill':skill.name,'count':skill_per}
        user_skill_stat_arr.append(obj)
    return HttpResponse(json.dumps(user_skill_stat_arr),content_type = 'application/json')
