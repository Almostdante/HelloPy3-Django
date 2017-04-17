# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-16 20:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_list', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='director',
            field=models.CharField(default='test', max_length=200),
        ),
        migrations.AddField(
            model_name='movie',
            name='imdb_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='imdb_rating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=2),
        ),
        migrations.AddField(
            model_name='movie',
            name='imdb_votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='metascore',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='original_name',
            field=models.CharField(default='test', max_length=200),
        ),
        migrations.AddField(
            model_name='movie',
            name='russian_name',
            field=models.CharField(default='test', max_length=200),
        ),
        migrations.AddField(
            model_name='movie',
            name='year',
            field=models.IntegerField(default=0),
        ),
    ]
