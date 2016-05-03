from __future__ import unicode_literals
from django_markdown.models import MarkdownField

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from taggit.managers import TaggableManager

from os.path import join as isfile
from django.conf import settings
import os


#this will store the extra profile details of the user
class UserProfileModel(models.Model):
    user = models.ForeignKey(User)
    user_description = MarkdownField()
    skills = TaggableManager()
    user_type_select = models.CharField(max_length = 50,default = 'None')   #developer or programmer
    user_profile_pic = models.FileField(upload_to = 'profile_pics/',blank = True)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.user.username




class CodehubTopicModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    topic_heading = models.CharField(max_length = 100)
    topic_detail = MarkdownField()
    topic_link = models.CharField(max_length = 100,blank = True)
    tags = TaggableManager()
    topic_type = models.CharField(max_length = 10)
    file = models.FileField(upload_to = 'uploads/',blank = True)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.topic_heading

    def delete(self,*args,**kwargs):
        print 'in the delete function of codehub model'
        if self.file:
            file_path = os.path.join(settings.MEDIA_ROOT,self.file.name)
            print file_path
            if os.path.isfile(file_path):
                os.remove(file_path)
        super(CodehubTopicModel,self).delete(*args,**kwargs)




class CodehubTopicCommentModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    topic = models.ForeignKey('CodehubTopicModel')
    comment_text = MarkdownField()
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.topic.topic_heading




class CodehubCreateEventModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    event_heading = models.CharField(max_length = 100)
    event_date = models.DateTimeField(null = True,blank = True)
    event_venue = models.CharField(max_length = 100)
    event_description = MarkdownField()
    event_for  = models.CharField(max_length = 25)#basic or advanced
    tags = TaggableManager()
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.event_heading



class CodehubEventQuestionModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    event = models.ForeignKey(CodehubCreateEventModel)
    question_text = MarkdownField()
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)


class MusicModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    music_name = models.CharField(max_length = 100)
    music_file = models.FileField(upload_to = 'music/')
    music_lang = models.CharField(max_length = 20)
    music_artist = models.CharField(max_length = 30)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.music_name


class CodehubQuestionModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    question_heading = models.CharField(max_length = 200)
    question_description = MarkdownField()
    question_link = models.CharField(max_length = 100,blank = True)
    question_tags = TaggableManager()
    question_type = models.CharField(max_length = 20)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.question_heading

class CodehubQuestionCommentModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    question = models.ForeignKey(CodehubQuestionModel)
    comment_text = MarkdownField()
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.question.question_heading


class BlogPostModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    title = models.CharField(max_length = 200)
    body = MarkdownField()
    tags = TaggableManager()
    image_file = models.FileField(upload_to = 'blog_images/',blank = True)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

    def delete(self,*args,**kwargs):
        print 'In the delete function of the BlogPostModel'
        if self.image_file:
            file_path = os.path.join(settings.MEDIA_ROOT,self.image_file.name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        super(BlogPostModel,self).delete(*args,**kwargs)



class BlogPostCommentModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    blog_post = models.ForeignKey(BlogPostModel)
    comment_text = MarkdownField()
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.comment_text


class CodehubInnovationPostModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    title = models.CharField(max_length = 200)
    description = MarkdownField()
    tags = TaggableManager()
    vote = models.CharField(max_length = 100,default = 0)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title


class CodehubInnovationCommentModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    innovation_post = models.ForeignKey(CodehubInnovationPostModel)
    comment_text = MarkdownField()
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.comment_text


class DevhubQuestionModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    question_heading = models.CharField(max_length = 200)
    question_description = MarkdownField()
    question_link = models.CharField(max_length = 100,blank = True)
    question_tags = TaggableManager()
    question_type = models.CharField(max_length = 20)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.question_heading



class DevhubQuestionAnswerModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    question = models.ForeignKey(DevhubQuestionModel)
    answer_text = MarkdownField()
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)



class DevhubTopicModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    topic_heading = models.CharField(max_length = 100)
    topic_detail = MarkdownField()
    topic_link = models.CharField(max_length = 100,blank = True)
    tags = TaggableManager()
    file = models.FileField(upload_to = 'devhub/',blank = True)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.topic_heading

    def delete(self,*args,**kwargs):
        print 'in the delete function of devhub model'
        if self.file:
            file_path = os.path.join(settings.MEDIA_ROOT,self.file.name)
            print file_path
            if os.path.isfile(file_path):
                os.remove(file_path)
        super(DevhubTopicModel,self).delete(*args,**kwargs)




class DevhubTopicCommentModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    topic = models.ForeignKey(DevhubTopicModel)
    comment_text = MarkdownField()
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.topic.topic_heading



class DevhubProjectModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    project_heading = models.CharField(max_length = 200)
    project_description = MarkdownField()
    project_link = models.CharField(max_length = 100,blank = True)
    tags = TaggableManager()




class FollowUserModel(models.Model):
    # following_user = models.CharField(max_length = 10)                                             #user who is following
    following_user = models.ForeignKey(User,related_name = 'following_user')
    followed_user = models.ForeignKey(User,related_name = 'followed_user')                            #user being followed
    following_user_profile = models.ForeignKey(UserProfileModel,related_name = 'following_user_profile')
    followed_user_profile = models.ForeignKey(UserProfileModel,related_name = 'followed_user_profile')



class ProposeEventModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    event_heading = models.CharField(max_length = 200)
    event_description = MarkdownField()
    tags = TaggableManager()
    event_type = models.CharField(max_length = 30)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)




class ProposeEventVoteModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    event = models.ForeignKey(ProposeEventModel)
    vote = models.CharField(max_length = 10)



class ProposeEventSuggestionModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    sugg_text = models.CharField(max_length = 500)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)



#host_project section starts here
class HostProjectModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    project_name = models.CharField(max_length = 200)
    project_description = MarkdownField()
    skills = TaggableManager()
    project_status = models.CharField(max_length = 15,default = 'active')
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)





class PingHostProjectModel(models.Model):
    user = models.ForeignKey(User)
    user_profile = models.ForeignKey(UserProfileModel)
    hosted_project = models.ForeignKey(HostProjectModel)
    created = models.DateTimeField(auto_now_add = True)





class MesssageModel(models.Model):
    sender = models.ForeignKey(User,related_name = 'sender')
    receiver = models.ForeignKey(User,related_name = 'receiver')
    sender_profile = models.ForeignKey(UserProfileModel,related_name = 'sender_profile')
    receiver_profile = models.ForeignKey(UserProfileModel,related_name = 'receiver_profile')
    message_text = models.CharField(max_length = 500)
