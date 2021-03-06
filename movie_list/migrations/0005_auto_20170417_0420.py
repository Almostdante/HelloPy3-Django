# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 02:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_list', '0004_torrent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='torrent',
            old_name='Movie_id',
            new_name='movie_id',
        ),
        migrations.RenameField(
            model_name='torrent',
            old_name='Torrent_size',
            new_name='torrent_size',
        ),
        migrations.AddField(
            model_name='torrent',
            name='movie_title',
            field=models.CharField(default='test', max_length=200),
        ),
        migrations.AddField(
            model_name='torrent',
            name='russian_movie_title',
            field=models.CharField(default='test', max_length=200),
        ),
        migrations.AddField(
            model_name='torrent',
            name='year',
            field=models.IntegerField(default=0),
        ),
    ]
