from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User

from app.models import UserProfileModel

def match_user_skills(request):
    total_user_count = User.objects.all().count()
    print total_user_count
    logged_user = UserProfileModel.objects.get(user_id = request.user.id)
    logged_user_skills = logged_user.skills.all()
    skillArr = []
    skill_slug_Arr = []
    for skill in logged_user_skills:
        skillArr.append(skill.name)
        skill_slug_Arr.append(skill.slug)
    skill_stat_dict = {skill:[] for skill in skill_slug_Arr}
    for skill in skill_slug_Arr:
        skill_user_count = UserProfileModel.objects.filter(skills__slug = skill).distinct().count()
        skill_user_percentile = (skill_user_count/float(total_user_count))*100
        skill_stat_dict[skill].append(skill_user_count)
        skill_stat_dict[skill].append(skill_user_percentile)
    matched_users_list = UserProfileModel.objects.filter(skills__name__in = skillArr).exclude(user_id = request.user.id).distinct()       #user list having similar skills
    return render(request,'match_skill/match_user_skills.html',{'logged_user_skills':skillArr,'matched_users_list':matched_users_list,'skill_stat_dict':skill_stat_dict})



def search_users_by_skill(request,skill_slug_str):
    result = UserProfileModel.objects.filter(skills__slug = skill_slug_str)
    return render(request,'match_skill/search_users_by_skill.html',{'result':result,'skill_search_str':skill_slug_str})


def get_all_skills_stat(request):
    all_skills = UserProfileModel.skills.all()
    total_users = User.objects.all().count()
    skill_count_dict = { skill: '' for skill in all_skills }  # have the count of users in a particular skill
    skill_per_dict = {skill: '' for skill in all_skills }  #have the percentage of peoples having same skill
    for skill in all_skills:
        skill_user_count = UserProfileModel.objects.filter(skills__name__in = [skill]).count()
        skill_user_per = (skill_user_count / float(total_users))*100

        skill_count_dict[skill] = skill_user_count
        skill_per_dict[skill] = skill_user_per
    # print skill_count_dict
    # print skill_per_dict
    return render(request,'match_skill/get_all_skills_stat.html',{'skill_count_dict':skill_count_dict,'skill_per_dict':skill_per_dict})
