from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django import template
from django.utils.safestring import mark_safe
import hashlib
import urllib

from .forms import UserProfileForm

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

def user_profile(request,id):
    info = User.objects.get(id = id)
    user_gravatar_url = gravatar(info.email)
    print user_gravatar_url
    return render(request,'users/user_profile.html',{'user_info':info,'gravatar_url':user_gravatar_url})


def edit_user_profile(request,id):
    form = UserProfileForm()
    return render(request,'users/edit_user_profile.html',{'form':form})
