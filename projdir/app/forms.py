from django import forms
from .models import CodehubTopicModel

#forms for posting a new topic
class CodehubTopicForm(forms.ModelForm):
    CHOICES = (('Basic', 'Basic'),('Advanced', 'Advanced'),)
    topic_heading = forms.CharField(label = 'Topic Heading',max_length = 100)
    topic_detail = forms.CharField(label = 'Add Details about Topic',widget = forms.Textarea(attrs = {'rows':'2','cols':'32'}),max_length = 200)
    topic_link = forms.URLField(label = 'Link to the topic',max_length = 100,required = False)
    tags = forms.CharField(label = 'Add tags',max_length = 100,required = True)
    topic_type = forms.ChoiceField(choices = CHOICES,required = True)
    file = forms.FileField(label = 'Upload a file:',required=False)
    class Meta:
        model = CodehubTopicModel
        fields = ['topic_heading','topic_detail','topic_link','tags','topic_type','file']

#form for commenting on a topic
class CodehubTopicCommentForm(forms.Form):
    comment_text = forms.CharField(label = '',max_length = 500,widget = forms.Textarea(attrs = {'rows':'3','cols':'40'}))
