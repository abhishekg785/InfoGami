from django.conf.urls import url

from app.host_project import work_collaborately,host_project,get_all_hosted_projects,hosted_project_details,edit_hosted_project,remove_hosted_project,activate_hosted_project,deactivate_hosted_project,skill_matched_hosted_project,user_hosted_projects,ping_hosted_project,hosted_project_interested_users,search_hosted_project,accept_hosted_project_request,reject_hosted_project_request,edit_hosted_project_query,remove_hosted_project_query

urlpatterns = [
    url(r'^work-and-collaborate/$',work_collaborately, name = 'work_collaborately'),
    url(r'^host-project/$',host_project,name = 'host_project'),
    url(r'^all-hosted-projects/$',get_all_hosted_projects,name = 'get_all_hosted_projects'),
    url(r'^host-project/(?P<project_id>\d+)/details/$',hosted_project_details,name = 'hosted_project_details'),
    url(r'^host-project/(?P<project_id>\d+)/edit/$',edit_hosted_project,name = 'edit_hosted_project'),
    url(r'^host-project/(?P<project_id>\d+)/remove/$',remove_hosted_project,name = 'remove_hosted_project'),
    url(r'^host-project/(?P<project_id>\d+)/activate/$',activate_hosted_project,name = 'activate_hosted_project'),
    url(r'^host-project/(?P<project_id>\d+)/deactivate/$',deactivate_hosted_project,name = 'deactivate_hosted_project'),
    url(r'^matched-hosted-project/$',skill_matched_hosted_project,name = 'skill_matched_hosted_project'),
    url(r'^user/(?P<user_id>\d+)/hosted-projects/$',user_hosted_projects,name = 'user_hosted_projects'),
    url(r'^hosted-project/(?P<project_id>\d+)/ping/$',ping_hosted_project,name = 'ping_hosted_project'),
    url(r'^search-hosted-project/$',search_hosted_project,name = 'search_hosted_project'),
    url(r'^host-project/interested-users/$',hosted_project_interested_users,name = 'hosted_project_interested_users'),
    url(r'^hosted-project/(?P<project_id>\d+)/user/(?P<user_id>\d+)/accept-request/$',accept_hosted_project_request,name = 'accept_hosted_project_request'),
    url(r'^hosted-project/(?P<project_id>\d+)/user/(?P<user_id>\d+)/reject-request/$',reject_hosted_project_request,name = 'reject_hosted_project_request'),
    url(r'^hosted-project/(?P<project_id>\d+)/query/(?P<query_id>\d+)/edit/$',edit_hosted_project_query,name = 'edit_hosted_project_query'),
    url(r'^hosted-project/(?P<project_id>\d+)/query/(?P<query_id>\d+)/remove/$',remove_hosted_project_query,name = 'remove_hosted_project_query'),
]
