from django import forms
from .models import CodehubTopicModel,CodehubTopicCommentModel,UserProfileModel

#forms for posting a new topic
class CodehubTopicForm(forms.ModelForm):
    CHOICES = (('Basic', 'Basic'),('Advanced', 'Advanced'),)
    topic_heading = forms.CharField(label = '',max_length = 100,widget = forms.TextInput(attrs = {'placeholder':'Topic heading goes here..'}))
    topic_detail = forms.CharField(label = '',widget = forms.Textarea(attrs = {'rows':'2','cols':'32','placeholder':'Enter the details about topic'}),max_length = 200)
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



class CodehubClassTalkNotifiyForm(forms.ModelForm):
    CHOICES = (('Basic', 'Basic'),('Advanced', 'Advanced'),)
    class_heading = forms.CharField(label = 'Class Heading',max_length = 50)
    class_on = forms.DateField()
    venue = forms.CharField(max_length = 100)
    class_description = forms.CharField(label = 'Class Description')
    class_for = forms.ChoiceField(choices = CHOICES,required =True)



class SearchForm(forms.Form):
    search_str = forms.CharField(label = 'Search here:',max_length = 50,required = True)
