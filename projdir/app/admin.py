from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from django_markdown.widgets import AdminMarkdownWidget
from django.db.models import TextField

from .models import CodehubTopicModel,CodehubTopicCommentModel,UserProfileModel,CodehubCreateEventModel,MusicModel,CodehubQuestionModel
# Register your models here.

class TopicAdmin(MarkdownModelAdmin):
    list_display = ("user","topic_heading")
    formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}


admin.site.register(CodehubTopicModel,TopicAdmin)
admin.site.register(CodehubTopicCommentModel)
admin.site.register(UserProfileModel)
admin.site.register(CodehubCreateEventModel,MarkdownModelAdmin)
admin.site.register(MusicModel)
admin.site.register(CodehubQuestionModel)
