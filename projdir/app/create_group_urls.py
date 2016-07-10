from django.conf.urls import url
from app.create_group import create_group_main_page,get_user_created_groups,search_group,get_group_details,edit_group_details,user_request_for_group,deactivate_group,activate_group

urlpatterns = [
    url(r'^create/$',create_group_main_page,name = 'create_group_main_page'),
    url(r'^user/(?P<user_id>\d+)/created-groups/$',get_user_created_groups,name = 'get_user_created_groups'),
    url(r'^search/$',search_group,name = 'search_group'),
    url(r'^(?P<group_id>\d+)/details/$',get_group_details,name = 'get_group_details'),
    url(r'^(?P<group_id>\d+)/edit/$',edit_group_details,name = 'edit_group_details'),
    url(r'^(?P<group_id>\d+)/join/$',user_request_for_group,name = 'user_request_for_group'),
    url(r'^(?P<group_id>\d+)/activate/$',activate_group,name = 'activate_group'),
    url(r'^(?P<group_id>\d+)/de-activate/$',deactivate_group,name = 'deactivate_group'),
]
