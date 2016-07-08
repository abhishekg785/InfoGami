from django.conf.urls import url
from app.general_question import ask_general_question,search_general_question,get_general_question_details,edit_general_question,remove_general_question,edit_general_question_answer,remove_general_question_answer,get_all_general_questions

urlpatterns = [
  url(r'ask/$',ask_general_question,name = 'ask_general_question'),
  url(r'search/$',search_general_question,name = 'search_general_question'),
  url(r'question/(?P<ques_id>\d+)/details/$',get_general_question_details,name = 'get_general_question_details'),
  url(r'question/(?P<ques_id>\d+)/edit/$',edit_general_question,name = 'edit_general_question'),
  url(r'question/(?P<ques_id>\d+)/remove/$',remove_general_question,name = 'remove_general_question'),
  url(r'question/(?P<ques_id>\d+)/answer/(?P<ans_id>\d+)/edit/$',edit_general_question_answer,name = 'edit_general_question_answer'),
  url(r'question/(?P<ques_id>\d+)/answer/(?P<ans_id>\d+)/remove/$',remove_general_question_answer,name = 'remove_general_question_answer'),
  url(r'get-all-questions/$',get_all_general_questions,name = 'get_all_general_questions'),
]
