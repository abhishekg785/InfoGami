from django.conf.urls import url
from app.theInfo import get_generic_main_page


urlpatterns = [
    url(r'^$',get_generic_main_page,name = 'get_generic_main_page'),
]
