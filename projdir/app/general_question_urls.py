from django.conf.urls import url
from app.general_question import ask_general_question,search_general_question,get_general_question_details

urlpatterns = [
  url(r'ask/$',ask_general_question,name = 'ask_general_question'),
  url(r'search/$',search_general_question,name = 'search_general_question'),
  url(r'question/(?P<ques_id>\d+)/details/$',get_general_question_details,name = 'get_general_question_details'),
]
