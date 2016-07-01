from django.conf.urls import url
from app.theInfo import the_info_main_page,search_query,vote_query_answer,query_details,undo_answer_vote,query_records


urlpatterns = [
    url(r'^$',the_info_main_page,name = 'the_info_main_page'),
    url(r'^search-query/$',search_query,name = 'search_query'),
    url(r'^vote-answer/$',vote_query_answer, name = 'vote_query_answer'),
    url(r'^undo-vote-answer/$',undo_answer_vote, name = 'undo_answer_vote'),
    url(r'^query/(?P<query_id>\d+)/details/$',query_details, name = 'query_details'),
    url(r'^queries/$',query_records,name = 'query_records'),

]
