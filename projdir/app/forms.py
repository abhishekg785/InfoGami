from django import forms
from .models import CodehubInnovationPostModel,BlogPostCommentModel,CodehubTopicModel,CodehubTopicCommentModel,UserProfileModel,CodehubCreateEventModel,CodehubEventQuestionModel,BlogPostModel,CodehubQuestionModel,CodehubQuestionCommentModel,CodehubInnovationCommentModel,DevhubQuestionModel,ProposeEventModel,ProposeEventSuggestionModel,DevhubQuestionAnswerModel,DevhubTopicModel,DevhubTopicCommentModel,HostProjectModel,HostProjectQuestionModel,TheInfoAddQueryModel,TheInfoQueryAnswerModel,GeneralQuestionModel,GeneralQuestionAnswerModel,CreateUserGroupModel,GroupUserCommentModel,DevhubCreateEventModel,DevhubEventQuestionModel
from django_markdown.widgets import MarkdownWidget
from taggit.forms import *

from markitup.widgets import MarkItUpWidget



#forms for posting a new topic
class CodehubTopicForm(forms.ModelForm):
    CHOICES = (('','--Select Type--'),('Basic', 'Basic'),('Advanced', 'Advanced'),)
    topic_heading = forms.CharField(label = '',max_length = 100,widget = forms.TextInput(attrs = {'placeholder':'Topic heading goes here..'}))
    topic_detail = forms.CharField(label = '',widget=MarkItUpWidget(attrs = {'placeholder':'Topic details goes here'}))
    topic_link = forms.URLField(label = '',max_length = 100,required = False,widget = forms.TextInput(attrs = {'placeholder':'Link to topic'}))
    tags = TagField(label = '',widget = TagWidget(attrs = {'placeholder':'Give some Tags(separated by commas)'}))
    topic_type = forms.ChoiceField(label = '',choices = CHOICES,required = True)
    file = forms.FileField(label = 'Upload a file:',required=False)
    class Meta:
        model = CodehubTopicModel
        fields = ['topic_heading','topic_detail','topic_link','tags','topic_type','file']



#form for commenting on a topic
class CodehubTopicCommentForm(forms.ModelForm):
    #comment_text = forms.CharField(label = '',max_length = 500,widget = forms.Textarea(attrs = {'rows':'3','cols':'40'}))
    comment_text = forms.CharField(label = '',widget=MarkItUpWidget(attrs = {'placeholder':'Your comment...','style':'height:15%'}))
    class Meta:
        model = CodehubTopicCommentModel
        fields = ['comment_text']



class UserProfileForm(forms.ModelForm):
    USER_TYPE_CHOICES = (('','--Select Type--'),('Programmer','Programmer'),('Developer/Hacker','Developer/Hacker'), ('Nerd/Geek', 'Nerd/Geek'), ('Entrepreneur', 'Entrepreneur'), ('Not sure right now:)','Not sure right now:)'))
    PROGRAMME_CHOICE = (('','--Select Type--'), ('B-Tech', 'B-Tech'), ('M-Tech', 'M-Tech'), ('MCA', 'MCA'), ('PHD', 'PHD'),)
    # BRANCH_CHOICES = (('', '--Select Branch--'), ('Computer Science', 'Computer Science'), ('Information Technology', 'Information Technology'), ('Electronics', 'Electronics'), ('Electrical Engineering', 'Electrical Engineering'), ('Mechanical', 'Mechanical'), ('Civil Engineering', 'Civil Engineering'), ('Production Engineering', 'Production Engineering'))
    USER_YEAR_CHOICES = (('', '--Select Year--'), ('First Year', 'First Year'), ('Second Year', 'Second Year'), ('Pre-Final', 'Pre-Final'), ('Final Year', 'Final Year'), ('Alumni', 'Alumni'))
    user_description = forms.CharField(label = '', max_length = 300, widget = forms.TextInput(attrs = {'placeholder' : 'A line about yourself (max 300 chars)'}))
    skills = TagField(label = 'Skills (What makes you itch ? )', widget = TagWidget(attrs = {'placeholder':'Enter your skills like python, poetry, c. c++, etc'}))
    user_type_select = forms.ChoiceField(choices = USER_TYPE_CHOICES, required = True )
    programme = forms.ChoiceField(choices = PROGRAMME_CHOICE, required = True)
    branch = forms.CharField(label = 'Branch (Does it matter :p)', widget = forms.TextInput(attrs = {'placeholder' : 'Your Branch'}))
    # branch = forms.ChoiceField(label = 'Branch (Does it matter :p)' , choices = BRANCH_CHOICES, required = True)
    college_year = forms.ChoiceField(label = 'College Year/ Alumni', choices = USER_YEAR_CHOICES, required = True)
    graduation_year = forms.CharField(label = '', max_length = 4, widget = forms.TextInput(attrs = {'placeholder' : 'Graduation Year'}))
    user_profile_pic = forms.FileField(label = 'Profile Pic (Look Smart !)',required = False)
    class Meta:
        model = UserProfileModel
        fields = ['user_description', 'skills', 'user_type_select', 'programme', 'branch', 'college_year', 'graduation_year', 'user_profile_pic']



class CodehubCreateEventForm(forms.ModelForm):
    CHOICES = (('','--Select Type--'),('Basic', 'Basic'),('Advanced', 'Advanced'),)
    event_heading = forms.CharField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Event Heading goes here...'}),max_length = 50)
    event_date = forms.DateTimeField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Date of Event(yy-mm-dd hh:mm)'}),required = False)
    event_description = forms.CharField(label = '',widget=MarkItUpWidget(attrs = {'placeholder':'Event Details goes here...'}))
    event_venue = forms.CharField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Event Venue'}),max_length = 100,required = False)
    event_for = forms.ChoiceField(label = 'Event For:',choices = CHOICES,required =True)
    tags = TagField(label = '',widget = TagWidget(attrs = {'placeholder':'Give some Tags(separated by commas)'}))

    class Meta:
        model = CodehubCreateEventModel
        fields = ['event_heading','event_date','event_venue','event_description','event_for']


class SearchForm(forms.Form):
    search_str = forms.CharField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Search here...'}),max_length = 50,required = True)


class CodehubEventQuestionForm(forms.ModelForm):
    question_text = forms.CharField(label = '',max_length = 300,widget = forms.Textarea(attrs = {'rows':'2','cols':'40','placeholder':'Ask here...'}))
    class Meta:
        model = CodehubEventQuestionModel
        fields = ['question_text']


class CodehubQuestionForm(forms.ModelForm):
    CHOICES = (('','--Select Type--'),('Basic','Basic'),('Intermediate','Intermediate'),('Advanced','Advanced'))
    question_heading = forms.CharField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Question Heading'}),max_length = 200)
    question_description = forms.CharField(label = '',widget=MarkItUpWidget(attrs = {'placeholder':'Question Details goes here...'}))
    question_link = forms.URLField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Question Link'}),max_length = 100,required = False)
    question_tags = TagField(label = '',widget = TagWidget(attrs = {'placeholder':'Enter Tags'}))
    question_type = forms.ChoiceField(label = '',choices = CHOICES)
    class Meta:
        model = CodehubQuestionModel
        fields = ['question_heading','question_description','question_link','question_tags','question_type']


class CodehubQuestionCommentForm(forms.ModelForm):
    comment_text = forms.CharField(label = '',widget = MarkItUpWidget(attrs = {'placeholder':'Enter your answer or suggestions here...','style':'height:10%'}))

    class Meta:
        model = CodehubQuestionCommentModel
        fields = ['comment_text']



class BlogPostForm(forms.ModelForm):
    title = forms.CharField(label = '',max_length = 200,widget = forms.TextInput(attrs = {'placeholder':'Title goes here'}))
    body = forms.CharField(label = '',widget=MarkItUpWidget(attrs = {'placeholder':'Body goes here...'}))
    tags = TagField(label = '',widget = TagWidget(attrs = {'placeholder':'Add tags(comma separated)'}))
    image_file = forms.FileField(label = 'Upload an Image:',required=False)
    class Meta:
        model = BlogPostModel
        fields = ['title','body','tags','image_file']



class BlogPostCommentForm(forms.ModelForm):
    comment_text = forms.CharField(label = '',widget=MarkItUpWidget(attrs = {'placeholder':'Your comment...','style':'height:10%'}))

    class Meta:
        model = BlogPostCommentModel
        fields = ['comment_text']


class CodehubInnovationPostForm(forms.ModelForm):
    title = forms.CharField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Title here'}))
    description = forms.CharField(label = '',widget = MarkItUpWidget(attrs = {'placeholder':'Description here','style':'height:10%'}))
    tags = TagField(label = '',widget = TagWidget(attrs = {'placeholder':'Enter Tags here'}))

    class Meta:
        model = CodehubInnovationPostModel
        fields = ['title','description','tags']


class CodehubInnovationCommentForm(forms.ModelForm):
    comment_text = forms.CharField(label ='',widget = MarkItUpWidget(attrs = {'placeholder':'Comment','style':'height:10%'}))

    class Meta:
        model = CodehubInnovationCommentModel
        fields = ['comment_text']



#devhub starts here
class DevhubQuestionForm(forms.ModelForm):
    CHOICES = (('','--Select Type--'),('Basic','Basic'),('Intermediate','Intermediate'),('Advanced','Advanced'))
    question_heading = forms.CharField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Question Heading'}),max_length = 200)
    question_description = forms.CharField(label = '',widget=MarkItUpWidget(attrs = {'placeholder':'Question Details goes here...'}))
    question_link = forms.URLField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Question Link'}),max_length = 100,required = False)
    question_tags = TagField(label = '',widget = TagWidget(attrs = {'placeholder':'Enter Tags'}))
    question_type = forms.ChoiceField(label = '',choices = CHOICES)
    class Meta:
        model = DevhubQuestionModel
        fields = ['question_heading','question_description','question_link','question_tags','question_type']



class DevhubQuestionAnswerForm(forms.ModelForm):
    answer_text = forms.CharField(label = '',widget = MarkItUpWidget(attrs = {'placeholder':'Enter your answer  here...','style':'height:10%'}))

    class Meta:
        model = DevhubQuestionAnswerModel
        fields = ['answer_text']




class DevhubTopicForm(forms.ModelForm):
    topic_heading = forms.CharField(label = '',max_length = 100,widget = forms.TextInput(attrs = {'placeholder':'Topic heading goes here..'}))
    topic_detail = forms.CharField(label = '',widget=MarkItUpWidget(attrs = {'placeholder':'Topic details goes here','style':''}))
    topic_link = forms.URLField(label = '',max_length = 100,required = False,widget = forms.TextInput(attrs = {'placeholder':'Link to topic'}))
    tags = TagField(label = '',widget = TagWidget(attrs = {'placeholder':'Give some Tags(separated by commas)'}))
    file = forms.FileField(label = 'Upload a file:',required=False)
    class Meta:
        model = DevhubTopicModel
        fields = ['topic_heading','topic_detail','topic_link','tags','file']



class DevhubTopicCommentForm(forms.ModelForm):
    #comment_text = forms.CharField(label = '',max_length = 500,widget = forms.Textarea(attrs = {'rows':'3','cols':'40'}))
    comment_text = forms.CharField(label = '',widget=MarkItUpWidget(attrs = {'placeholder':'Your comment...','style':'height:5%'}))
    class Meta:
        model = DevhubTopicCommentModel
        fields = ['comment_text']


# class DevhubProjectForm(forms.ModelForm):
#     project_heading = forms.CharField(label = '')
#     project_description =
#     project_link =
#     tags =

class ProposeEventForm(forms.ModelForm):
    CHOICES = (('','--Select Type--'),('Coding','Coding'),('Development','Development'),('Graphics','Graphics'),('Electronics','Electronics'))
    event_heading = forms.CharField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Event Heading goes here'}))
    event_description = forms.CharField(label = '',widget = MarkItUpWidget(attrs = {'placeholder':'Event Description goes here'}))
    tags = TagField(label = '',widget = TagWidget(attrs = {'placeholder':'Tags related to event'}))
    event_type = forms.ChoiceField(label = '',choices = CHOICES)

    class Meta:
        model = ProposeEventModel
        fields = ['event_heading','event_description','tags','event_type']




class ProposeEventSuggestionForm(forms.ModelForm):
    sugg_text = forms.CharField(label = '',widget = forms.Textarea(attrs = {'placeholder':'Give suggestions here...','cols':'2','rows':'2'}))
    class Meta:
        model = ProposeEventSuggestionModel
        fields = ['sugg_text']




class HostProjectForm(forms.ModelForm):
    project_name = forms.CharField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Enter the name of your project'}))
    project_description = forms.CharField(label = '',widget = MarkItUpWidget(attrs = {'placeholder':'Project Description goes here'}))
    skills = TagField(label = '',widget = TagWidget(attrs = {'placeholder':'Skills needed for project(comma separated)'}))

    class Meta:
        model = HostProjectModel
        fields = ['project_name','project_description','skills']




class HostProjectQuestionForm(forms.ModelForm):
    question_text = forms.CharField(label = '',widget = forms.Textarea(attrs = {'placeholder':'Ask queries here...','rows':'2'}))

    class Meta:
        model = HostProjectQuestionModel
        fields = ['question_text']




class TheInfoAddQueryForm(forms.ModelForm):
    queryText = forms.CharField(required = True,label = '',max_length = 150,widget = forms.Textarea(attrs = {'placeholder':'Add query for something "best"','rows':'2','id':'addQueryTextId'}))
    queryTags = TagField(required = True,label = '',widget = TagWidget(attrs = {'id':'addQueryTagsId','placeholder':'Enter tags for the query(separated by commas)'}))

    class Meta:
        model = TheInfoAddQueryModel
        fields = ['queryText','queryTags']




class TheInfoQueryAnswerForm(forms.ModelForm):
    answerText = forms.CharField(required = False, label = '',max_length = 500,widget = forms.Textarea(attrs = {'placeholder':'Provide a best answer(optional)','rows':'2','id':'answerText'}))

    class Meta:
        model = TheInfoQueryAnswerModel
        fields = ['answerText']



class GeneralQuestionForm(forms.ModelForm):
    ques_text = forms.CharField(label = '',max_length = 200,widget = MarkItUpWidget(attrs = {'placeholder':'Project Description goes here(max 200 characters)'}))
    ques_tags = TagField(required = True,label = '',widget = TagWidget(attrs = {'placeholder':'Give tags for your question(comma separated)','id':'quesTagField'}))

    class Meta:
        model = GeneralQuestionModel
        fields = ['ques_text','ques_tags']





class GeneralQuestionAnsweForm(forms.ModelForm):
    answer_text = forms.CharField(label = '',max_length = 250,widget = forms.Textarea(attrs = {'placeholder':'Give answer here...(max 250 characters)','rows':3}))
    class Meta:
        fields = ['answer_text']
        model = GeneralQuestionAnswerModel




class CreateUserGroupForm(forms.ModelForm):
    group_name = forms.CharField(label = '',required = True,max_length = 50,widget = forms.TextInput(attrs = {'placeholder':'Group name comes here..'}))
    group_description = forms.CharField(label = '',widget = MarkItUpWidget(attrs = {'placeholder':'Description of the group comes here...'}))
    group_tags = TagField(required = True,label = '',widget = TagWidget(attrs = {'placeholder':'Give tags for the group(comma separated)  eg:for a "python group", mention tags like "python","python lovers"'}))

    class Meta:
        fields = ['group_name','group_description','group_tags']
        model = CreateUserGroupModel



class GroupUserCommentForm(forms.ModelForm):
    comment_text = forms.CharField(label = '',required = True,max_length = 150,widget = forms.Textarea(attrs = {'placeholder':'Comment here...','rows':1.5}))
    class Meta:
        fields = ['comment_text']
        model = GroupUserCommentModel



class DevhubCreateEventForm(forms.ModelForm):
    CHOICES = (('','--Select Type--'),('Basic', 'Basic'),('Advanced', 'Advanced'),)
    event_heading = forms.CharField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Event Heading goes here...'}),max_length = 50)
    event_date = forms.DateTimeField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Date of Event(yy-mm-dd hh:mm)'}),required = False)
    event_description = forms.CharField(label = '',widget=MarkItUpWidget(attrs = {'placeholder':'Event Details goes here...'}))
    event_venue = forms.CharField(label = '',widget = forms.TextInput(attrs = {'placeholder':'Event Venue'}),max_length = 100,required = False)
    event_for = forms.ChoiceField(label = 'Event For:',choices = CHOICES,required =True)
    tags = TagField(label = '',widget = TagWidget(attrs = {'placeholder':'Give some Tags(separated by commas)'}))

    class Meta:
        model = DevhubCreateEventModel
        fields = ['event_heading','event_date','event_venue','event_description','event_for']


class DevhubEventQuestionForm(forms.ModelForm):
    question_text = forms.CharField(label = '',max_length = 300,widget = forms.Textarea(attrs = {'rows':'2','cols':'40','placeholder':'Ask here...'}))
    class Meta:
        model = DevhubEventQuestionModel
        fields = ['question_text']
