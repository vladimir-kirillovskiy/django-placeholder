# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-05 16:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apifetch', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='companyname',
            field=models.CharField(default='', max_length=100),
        ),
    ]