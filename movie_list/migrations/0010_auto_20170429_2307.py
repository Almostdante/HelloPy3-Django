# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-29 21:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_list', '0009_auto_20170423_0146'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.CharField(default='test', max_length=500),
        ),
        migrations.AddField(
            model_name='movie',
            name='plot',
            field=models.CharField(default='test', max_length=1000),
        ),
    ]
