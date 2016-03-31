from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
topic_type_choices = ('Basic','Advanced')

class CodehubTopicModel(models.Model):
    user = models.ForeignKey(User)
    topic_heading = models.CharField(max_length = 100)
    topic_detail = models.CharField(max_length = 200)
    topic_link = models.CharField(max_length = 100 )
    tags = models.CharField(max_length = 50)
    timeStamp = models.DateTimeField()
    #topic_type = models.CharField(widget = forms.Se)

    def __str__(self):
        return self.topic_heading


class CodehubTopicCommentModel(models.Model):
    user = models.ForeignKey(User)
    topic = models.ForeignKey('CodehubTopicModel')
    comment_text = models.CharField(max_length = 500)
    timeStamp = models.DateTimeField()
