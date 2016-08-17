from django.conf.urls import url
from app.devhub import devhub,devhub_question,devhub_question_details,edit_devhub_question,remove_devhub_question,get_all_devhub_questions,search_devhub_question,edit_devhub_question_answer,remove_devhub_question_answer,devhub_topic,get_all_devhub_topics,search_devhub_topic,devhub_topic_details,edit_devhub_topic,remove_devhub_topic,edit_devhub_topic_comment,remove_devhub_topic_comment
from app.create_event import create_devhub_event,get_devhub_events,devhub_event_details,edit_devhub_event,remove_devhub_event,edit_devhub_event_question,remove_devhub_event_question,search_devhub_event

urlpatterns = [
url(r'^$',devhub,name = 'devhub'),
url(r'^ask-question/$',devhub_question,name = 'devhub_question'),
url(r'^question/(?P<ques_id>\d+)/details/$',devhub_question_details,name = 'devhub_question_details'),
url(r'^question/(?P<ques_id>\d+)/edit/$',edit_devhub_question,name = 'edit_devhub_question'),
url(r'^question/(?P<ques_id>\d+)/remove/$',remove_devhub_question,name = 'remove_devhub_question'),
url(r'^question/(?P<ques_id>\d+)/answer/(?P<ans_id>\d+)/edit/$',edit_devhub_question_answer,name = 'edit_devhub_question_answer'),
url(r'^question/(?P<ques_id>\d+)/answer/(?P<ans_id>\d+)/remove/$',remove_devhub_question_answer,name = 'remove_devhub_question_answer'),
url(r'^all-questions/$',get_all_devhub_questions,name = 'get_all_devhub_questions'),
url(r'^search-question/$',search_devhub_question,name = 'search_devhub_question'),
url(r'^post-topic/$',devhub_topic,name = 'devhub_topic'),
url(r'^all-topics/$',get_all_devhub_topics,name = 'get_all_devhub_topics'),
url(r'^search-topic/$',search_devhub_topic,name = 'search_devhub_topic'),
url(r'^topic/(?P<topic_id>\d+)/details/$',devhub_topic_details,name = 'devhub_topic_details'),
url(r'^topic/(?P<topic_id>\d+)/edit/$',edit_devhub_topic,name = 'edit_devhub_topic'),
url(r'^topic/(?P<topic_id>\d+)/remove/$',remove_devhub_topic,name = 'remove_devhub_topic'),
url(r'^topic/(?P<topic_id>\d+)/comment/(?P<comm_id>\d+)/edit/$',edit_devhub_topic_comment,name = 'edit_devhub_topic_comment'),
url(r'^topic/(?P<topic_id>\d+)/comment/(?P<comm_id>\d+)/remove/$',remove_devhub_topic_comment,name = 'remove_devhub_topic_comment'),

#creating developer meetuos/events/talks
url(r'^create-event/$',create_devhub_event,name = 'create_devhub_event'),
url(r'^events/$',get_devhub_events,name = 'get_devhub_events'),
url(r'^event/(?P<event_id>\d+)/details/$',devhub_event_details,name = 'devhub_event_details'),
url(r'^event/(?P<event_id>\d+)/edit/$',edit_devhub_event,name = 'edit_devhub_event'),
url(r'^event/(?P<event_id>\d+)/remove/$',remove_devhub_event,name = 'remove_devhub_event'),
url(r'^event/(?P<event_id>\d+)/question/(?P<ques_id>\d+)/edit/$',edit_devhub_event_question,name = 'edit_devhub_event_question'),
url(r'^event/(?P<event_id>\d+)/question/(?P<ques_id>\d+)/remove/$',remove_devhub_event_question,name = 'remove_devhub_event_question'),
url(r'^event/search-event/$',search_devhub_event,name = 'search_devhub_event'),
]
