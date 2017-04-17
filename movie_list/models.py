# encoding=utf8

from django.db import models
from django.utils import timezone
import re
from urllib.request import urlopen
import json
from urllib.parse import urlencode


class Movie(models.Model):
    imdb_id = models.IntegerField(default=0)
    original_name = models.CharField(max_length=200, default='test')
    russian_name = models.CharField(max_length=200, default='test')
    director = models.CharField(max_length=200, default='test')
    year = models.IntegerField(default=0)
    imdb_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    imdb_votes = models.IntegerField(default=0)
    metascore = models.IntegerField(default=0)
    watched = models.BooleanField
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    poster = models.URLField(default='')


    def __str__(self):
        return '%s, %s, %s, %s, %s, %s, %s, ' % (self.original_name, self.director, self.year,
                                                 self.imdb_id, self.imdb_rating, self.imdb_votes, self.metascore)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def check_imdb(self):
        if self.imdb_id and (timezone.now() - self.created_date).days > 7:
            url = '{}?{}'.format('http://www.omdbapi.com/', urlencode({'i':self.imdb_id}))
            urlll = urlopen(url).read()
            js = json.loads(urlll)
            if js[u'Response'] == 'True':
                self.director = str(js['Director'])
                if js['imdbRating'] != 'N/A':
                    self.imdb_rating = float(js['imdbRating'])
                    self.imdb_votes = int(js['imdbVotes'].split(',')[0])
                if js['Metascore'].isdigit():
                    self.metascore = int(js['Metascore'])
                self.poster = js['Poster']
                self.save()
        elif not self.imdb_id:
            url = '{}?{}'.format('http://www.omdbapi.com/', urlencode({'t':re.sub(r"\s+", '+', self.original_name), 'y':self.year}))
            urlll = urlopen(url).read()
            js = json.loads(urlll)
            if js[u'Response'] == 'True':
                try:
                    m = Movie.objects.get(imdb_id=int(js['imdbID'][2:]))
                    print (m)
                    self.delete()
                    return m
                except:
                    self.imdb_id = int(js['imdbID'][2:])
                    self.director = str(js['Director'])
                    if js['imdbRating'] != 'N/A':
                        self.imdb_rating = float(js['imdbRating'])
                        self.imdb_votes = int(js['imdbVotes'].split(',')[0])
                    if js['Metascore'].isdigit():
                        self.metascore = int(js['Metascore'])
                    self.poster = js['Poster']
                    self.save()
        return self



class Torrent(models.Model):
    torrent_size = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    link_to_topic = models.URLField(default='')
    link_to_torrent_download = models.URLField(default='')
    movie_id = models.ForeignKey(Movie)
    subtitles = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s, %s, ' % (self.movie_id, self.link_to_topic)