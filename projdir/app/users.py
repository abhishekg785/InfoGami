from django.shortcuts import render,redirect
from django.http import HttpResponse
from django import template
from django.utils.safestring import mark_safe
import hashlib
import urllib

register = template.Library()

@register.filter
def gravatar_url(email, size=128):
  default = "http://example.com/static/images/defaultavatar.jpg"
  return "http://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.lower()).hexdigest(), urllib.urlencode({'d':default, 's':str(size)}))


@register.filter
def gravatar(email, size=128):
    url = gravatar_url(email, size)
    return mark_safe('<img src="%s" height="%d" width="%d">' % (url, size, size))


def get_users(request):
    return HttpResponse(gravatar('abhishekg785@gmail.com'))

def user_profile(request,id):
    return HttpResponse(id)
