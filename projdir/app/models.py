from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CodehubTopicModel(models.Model):
    user = models.ForeignKey(User)
    topic_heading = models.CharField(max_length = 100)
    topic_detail = models.CharField(max_length = 200)
    topic_link = models.CharField(max_length = 100 )
    tags = models.CharField(max_length = 50)
    timeStamp = models.DateTimeField()
    topic_type = models.CharField(max_length = 10)
    file = models.FileField(upload_to = 'uploads/')

    def __str__(self):
        return self.topic_heading


class CodehubTopicCommentModel(models.Model):
    user = models.ForeignKey(User)
    topic = models.ForeignKey('CodehubTopicModel')
    comment_text = models.CharField(max_length = 500)
    timeStamp = models.DateTimeField()

    def __str__(self):
        return self.topic.topic_heading


#this will store the extra profile details of the user
class UserProfileModel(models.Model):
    user = models.ForeignKey(User)
    user_description = models.CharField(max_length = 200)
    skills = models.CharField(max_length = 200)
    user_type_select = models.CharField(max_length = 50,default = 'None')   #developer or programmer
    timeStamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.user.username


class CodehubCreateEventModel(models.Model):
    user = models.ForeignKey(User)
    event_heading = models.CharField(max_length = 100)
    event_date = models.DateTimeField(null = True)
    event_venue = models.CharField(max_length = 100)
    event_description = models.CharField(max_length = 200)
    event_for  = models.CharField(max_length = 25)#basic or advanced
    timeStamp = models.DateTimeField()

    def __str__(self):
        return self.event_heading
