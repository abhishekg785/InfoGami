from django.conf.urls import url
from app.codehub import codehub_question,remove_codehub_question,edit_codehub_question,codehub,codehub_topic,edit_topic,remove_topic,comment_on_topic,search_topic,remove_topic_comment,edit_topic_comment,codehub_question_details,remove_codehub_question_comment,edit_codehub_question_comment,search_question,codehub_innovation,codehub_innovation_details,edit_codehub_innovation_idea,remove_codehub_innovation_idea,edit_codehub_innovation_idea_comment,remove_codehub_innovation_idea_comment,search_codehub_innovation_post,get_all_codehub_topics,get_all_codehub_questions

urlpatterns = [
    url(r'^$',codehub,name = codehub),
    url(r'^topic/$',codehub_topic,name = 'codehub_topic'),
    url(r'^topic/edit/(?P<id>\d+)/$',edit_topic,name = 'edit_topic'),
    url(r'^topic/remove/(?P<id>\d+)/$',remove_topic,name = 'remove_topic'),
    url(r'^topic/(?P<id>\d+)/comment/$',comment_on_topic,name = 'comment_on_topic'),
    url(r'^topic/search_topic/$',search_topic,name = 'search_topic'),
    url(r'^topic/comment/(?P<id>\d+)/remove/$',remove_topic_comment,name = 'remove_topic_comment'),
    url(r'^topic/comment/(?P<id>\d+)/edit/$',edit_topic_comment,name = 'edit_topic_comment'),
    url(r'^all_topics/$',get_all_codehub_topics,name = 'get_all_codehub_topics'),
]
