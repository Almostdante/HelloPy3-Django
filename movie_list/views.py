from django.shortcuts import render, get_object_or_404
from movie_list.models import Movie, Torrent
from datetime import date
from .tables import MovieTable, TorrentTable
from django_tables2 import RequestConfig
from django.template.loader import render_to_string


# Create your views here.


def main_movie_list(request):
    movie_list = MovieTable(Movie.objects.filter(imdb_rating__gt=6.9).order_by("-created_date"))
    RequestConfig(request).configure(movie_list)

    return render(request, 'movie_list/list.html', {'movies':movie_list})

def movie_page(request, id):
    movie = get_object_or_404(Movie, id=id)
    torrents=TorrentTable(Torrent.objects.filter(movie_id=movie))

    return render(request, 'movie_list/movie_page.html', {'movie':movie, 'torrents':torrents})


def email(request):
    movie_list = MovieTable(Movie.objects.filter(created_date__gte=date.today() , imdb_rating__gt=6.9).order_by("-year"))
    RequestConfig(request).configure(movie_list)

    return render(request, 'movie_list/email.html', {'movies':movie_list})
