from django import forms
from .models import CodehubTopicModel,CodehubTopicCommentModel,UserProfileModel,CodehubCreateEventModel,CodehubEventQuestionModel,BlogModel,CodehubQuestionModel

from django_markdown.widgets import MarkdownWidget

#forms for posting a new topic
class CodehubTopicForm(forms.ModelForm):
    CHOICES = (('None','None'),('Basic', 'Basic'),('Advanced', 'Advanced'),)
    topic_heading = forms.CharField(label = '',max_length = 100,widget = forms.TextInput(attrs = {'placeholder':'Topic heading goes here..'}))
    topic_detail = forms.CharField(label = '',widget=MarkdownWidget(attrs = {'placeholder':'Topic Details goes here..'}))
    # topic_detail = forms.CharField(label = '',widget = forms.Textarea(attrs = {'rows':'2','cols':'32','placeholder':'Enter the details about topic'}),max_length = 200)
    topic_link = forms.URLField(label = '',max_length = 100,required = False,widget = forms.TextInput(attrs = {'placeholder':'Link to topic'}))
    tags = forms.CharField(label = 'Add tags',max_length = 100,required = True,widget = forms.TextInput(attrs = {'placeholder':'Add tags'}))
    topic_type = forms.ChoiceField(choices = CHOICES,required = True)
    file = forms.FileField(label = 'Upload a file:',required=False)
    class Meta:
        model = CodehubTopicModel
        fields = ['topic_heading','topic_detail','topic_link','tags','topic_type','file']



#form for commenting on a topic
class CodehubTopicCommentForm(forms.ModelForm):
    comment_text = forms.CharField(label = '',max_length = 500,widget = forms.Textarea(attrs = {'rows':'3','cols':'40'}))
    class Meta:
        model = CodehubTopicCommentModel
        fields = ['comment_text']



class UserProfileForm(forms.ModelForm):
    CHOICES = (('None','None'),('Programmer','Programmer'),('Developer','Developer'),('Not sure right now:)','Not sure right now:)'),('Both','Both'),)
    user_description = forms.CharField(label = 'A line about yourself(max = 200 characters)',max_length = 200)
    skills = forms.CharField(label = 'Skills you have',max_length = 200)
    user_type_select = forms.ChoiceField(choices = CHOICES, required = True )
    class Meta:
        model = UserProfileModel
        fields = ['user_description','skills','user_type_select']



class CodehubCreateEventForm(forms.ModelForm):
    CHOICES = (('None','None'),('Basic', 'Basic'),('Advanced', 'Advanced'),)
    event_heading = forms.CharField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Event Heading goes here...'}),max_length = 50)
    event_date = forms.DateTimeField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Date of Event(yy-mm-dd hh:mm)'}),required = False)
    event_description = forms.CharField(label = '',widget = forms.Textarea(attrs = {'placeholder':'Event Description goes here','rows':'2','cols':'40'}))
    event_venue = forms.CharField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Event Venue'}),max_length = 100,required = False)
    event_for = forms.ChoiceField(label = 'Event For:',choices = CHOICES,required =True)
    class Meta:
        model = CodehubCreateEventModel
        fields = ['event_heading','event_date','event_venue','event_description','event_for']


class SearchForm(forms.Form):
    search_str = forms.CharField(label = 'Search here:',max_length = 50,required = True)


class CodehubEventQuestionForm(forms.ModelForm):
    question_text = forms.CharField(label = '',max_length = 300,widget = forms.Textarea(attrs = {'rows':'2','cols':'40','placeholder':'Ask here...'}))
    class Meta:
        model = CodehubEventQuestionModel
        fields = ['question_text']


class CodehubQuestionForm(forms.ModelForm):
    CHOICES = (('Basic','Basic'),('Intermediate','Intermediate'),('Advanced','Advanced'))
    question_heading = forms.CharField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Question Heading'}),max_length = 200)
    question_description = forms.CharField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Question Description'}),max_length = 500)
    question_link = forms.CharField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Question Link'}),max_length = 100,required = False)
    question_tags = forms.CharField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Question Tags'}),max_length = 200)
    question_type = forms.ChoiceField(label = '',choices = CHOICES)
    class Meta:
        model = CodehubQuestionModel
        fields = ['question_heading','question_description','question_link','question_tags','question_type']


class BlogForm(forms.ModelForm):
    content = forms.CharField()
    class Meta:
        model = BlogModel
        fields = ['content']
