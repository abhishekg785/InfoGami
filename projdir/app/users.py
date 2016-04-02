from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django import template
from django.utils.safestring import mark_safe
import hashlib
import urllib

from .forms import UserProfileForm
from .models import UserProfileModel
import datetime

register = template.Library()

@register.filter
def gravatar_url(email, size=128):
  default = "http://example.com/static/images/defaultavatar.jpg"
  return "http://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.lower()).hexdigest(), urllib.urlencode({'d':default, 's':str(size)}))


@register.filter
def gravatar(email, size=128):
    url = gravatar_url(email, size)
    # return mark_safe('<img src="%s" height="%d" width="%d">' % (url, size, size))
    return url


def get_users(request):
    return HttpResponse(gravatar('abhishekg785@gmail.com'))

def user_profile(request,user_id):
    info = User.objects.get(id = user_id)
    try:
        user_profile = UserProfileModel.objects.get(user_id = user_id)
    except:
        user_profile = False
    user_gravatar_url = gravatar(info.email)
    print user_gravatar_url
    return render(request,'users/user_profile.html',{'user_info':info,'user_profile':user_profile,'gravatar_url':user_gravatar_url})


#CREATE DECORATOR TO CHECK THE PERSON EDITIING THE FORM
def edit_user_profile(request,user_id):
    data = ['user_description','skills','user_type_select']
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            try:
                profile_details = UserProfileModel.objects.get(user_id = user_id)
            except:
                user = User.objects.get(id = user_id)
                profile_details = UserProfileModel(user = user,timeStamp = datetime.datetime.now())
            form = UserProfileForm(request.POST,instance = profile_details)
            form.save()
    else:
        try:
            profile_details = UserProfileModel.objects.get(user_id = user_id)
        except:
            print 'No data yet'
            profile_details = []
        if not profile_details:
            form_data = {key:'' for key in data}
        else:
            form_data = {'user_description':profile_details.user_description,'skills':profile_details.skills,'user_type_select':profile_details.user_type_select}
        form = UserProfileForm(initial = form_data)
    return render(request,'users/edit_user_profile.html',{'form':form})
