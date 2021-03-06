# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-28 20:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0032_theinfoaddquerymodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='theinfoaddquerymodel',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='theinfoaddquerymodel',
            name='user_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.UserProfileModel'),
        ),
    ]
