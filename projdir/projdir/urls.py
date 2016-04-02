"""projdir URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from app.views import login_view,register_view,logout_view,index
from app.codehub import codehub,codehub_topic,edit_topic,remove_topic,comment_on_topic,search_topic,remove_topic_comment,edit_topic_comment
from app.users import get_users,user_profile,edit_user_profile

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',index,name = 'index'),
    url(r'^auth/login/$',login_view,name='login_view'),
    url(r'^auth/register/$',register_view,name='register_view'),
    url(r'^auth/logout/$',logout_view,name='logout_view'),
    url(r'^codehub/$',codehub,name='codehub'),
    url(r'^codehub/topic/$',codehub_topic,name = 'codehub_topic'),
    url(r'^codehub/topic/edit/(?P<id>\d+)/$',edit_topic,name = 'edit_topic'),
    url(r'^codehub/topic/remove/(?P<id>\d+)/$',remove_topic,name = 'remove_topic'),
    url(r'^codehub/topic/(?P<id>\d+)/comment/$',comment_on_topic,name = 'comment_on_topic'),
    url(r'^codehub/topic/search_topic/$',search_topic,name = 'search_topic'),
    url(r'^codehub/topic/comment/(?P<id>\d+)/remove$',remove_topic_comment,name = 'remove_topic_comment'),
    url(r'^codehub/topic/comment/(?P<id>\d+)/edit$',edit_topic_comment,name = 'edit_topic_comment'),
    url(r'^users/$',get_users,name='get_users'),
    url(r'^users/profile/(?P<user_id>\d+)/$',user_profile,name = 'user_profile'),
    url(r'^users/profile/(?P<user_id>\d+)/edit/$',edit_user_profile,name = 'edit_user_profile')
]
