from django import forms
from .models import CodehubTopicModel

#forms for posting a new topic
class CodehubTopicForm(forms.Form):
    topic_heading = forms.CharField(label = 'Topic Heading',max_length = 100)
    topic_detail = forms.CharField(label = 'Add Details about Topic',widget = forms.Textarea(attrs = {'rows':'2','cols':'32'}),max_length = 200)
    topic_link = forms.URLField(label = 'Link to the topic',max_length = 100,required = False)
    tags = forms.CharField(label = 'Add tags',max_length = 100,required = True)
