# encoding=utf8
import re
import json
from django.db import models
from django.utils import timezone
from django.shortcuts import get_object_or_404
from urllib.request import urlopen
from urllib.parse import urlencode


class Movie(models.Model):
    imdb_id = models.IntegerField(default=0)
    original_name = models.CharField(max_length=200, default='test')
    russian_name = models.CharField(max_length=200, default='test')
    names = models.CharField(max_length=500, default='test')
    director = models.CharField(max_length=200, default='test')
    year = models.IntegerField(default=0)
    imdb_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    imdb_votes = models.IntegerField(default=0)
    metascore = models.IntegerField(default=0)
    watched = models.BooleanField
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    poster = models.URLField(default='')
    plot = models.CharField(max_length=1000, default='test')
    genre = models.CharField(max_length=500, default='test')


    def __str__(self):
        return '%s, %s, %s, %s, %s, %s, %s, ' % (self.original_name, self.director, self.year,
                                                 self.imdb_id, self.imdb_rating, self.imdb_votes, self.metascore)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def check_imdb(self):
        js = json.decoder.JSONDecoder()
        list_names = js.decode(self.names)
        for name in list_names:
            if re.search('[а-яА-Я]+', name):
                if self.russian_name == 'test':
                    self.russian_name = name.strip('+')
                list_names.remove(name)
        if self.imdb_id:
            url = '{}?{}&plot=full'.format('http://www.omdbapi.com/', urlencode({'i': self.imdb_id.rjust(9, "0"), 'apikey': 'fbe4383c'}))
            url_read = urlopen(url).read().decode('utf8')
            print (url_read)
            print (type(url_read))
            js = json.loads(url_read)
            if js[u'Response'] == 'True':
                self.director = str(js['Director'])
                self.original_name = str(js['Title'])
                if js['imdbRating'] != 'N/A':
                    self.imdb_rating = float(js['imdbRating'])
                    self.imdb_votes = int(js['imdbVotes'].split(',')[0])
                if js['Metascore'].isdigit():
                    self.metascore = int(js['Metascore'])
                self.poster = js['Poster']
                self.plot = str(js['Plot'])
                self.genre = str(js['Genre'])
        else:
            for name in list_names:
                url = '{}?{}'.format('http://www.omdbapi.com/', urlencode({'t': re.sub(r"\s+", '+', name.strip('+')),
                                                                           'y': self.year, 'apikey': 'fbe4383c'}))
                url_read = urlopen(url).read().decode('utf8')
                print (url_read, type(url_read))
                js = json.loads(url_read)
                if js[u'Response'] == 'True':
                    self.imdb_id = int(js['imdbID'][2:])
                    self.director = str(js['Director'])
                    self.original_name = str(js['Title'])
                    if js['imdbRating'] != 'N/A':
                        self.imdb_rating = float(js['imdbRating'])
                        self.imdb_votes = int(js['imdbVotes'].split(',')[0])
                    if js['Metascore'].isdigit():
                        self.metascore = int(js['Metascore'])
                    self.poster = js['Poster']
                    self.plot = str(js['Plot'])
                    self.genre = str(js['Genre'])
                    break
        self.published_date = timezone.now()
        self.save()
        return self

    def get_torrents(self):
        return  Torrent.objects.filter(movie_id = self.id)

    def get_image(self):
        return '<img src="%s" />'% self.poster


class Torrent(models.Model):
    torrent_size = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    link_to_topic = models.URLField(default='')
    link_to_torrent_download = models.URLField(default='')
    movie_id = models.ForeignKey(Movie)
    subtitles = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    torrent_id = models.IntegerField(default=0)
    tracker = models.CharField(max_length=200, default='')

    def __str__(self):
        return '%s, %s, ' % (self.movie_id, self.link_to_topic)
