# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-10 11:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0045_auto_20160710_0154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='createusergroupmodel',
            name='group_pic',
        ),
    ]
