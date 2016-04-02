from django.contrib import admin

from .models import CodehubTopicModel,CodehubTopicCommentModel,UserProfileModel
# Register your models here.
admin.site.register(CodehubTopicModel)
admin.site.register(CodehubTopicCommentModel)
admin.site.register(UserProfileModel)
