from django.shortcuts import render, get_object_or_404
from .forms import YearForm
from movie_list.models import Movie, Torrent
from datetime import date
from .tables import MovieTable, TorrentTable
from django_tables2 import RequestConfig
from django.template.loader import render_to_string


# Create your views here.


def main_movie_list(request):
    if 'Year' in request.GET:
        movie_list = MovieTable(Movie.objects.filter(imdb_rating__gt=6.9).filter(year__gt=int(request.GET['Year'])-1).order_by("-created_date"))
    elif 'Name' in request.GET:
        movie_list = MovieTable(Movie.objects.filter(imdb_rating__gt=6.9).filter(names__contains=request.GET['Name']).order_by("-created_date"))
    else:
        movie_list = MovieTable(Movie.objects.filter(imdb_rating__gt=6.9).order_by("-created_date"))
    RequestConfig(request, paginate={"per_page": 100}).configure(movie_list)
    form = YearForm()

    return render(request, 'movie_list/list.html', {'movies':movie_list, 'form': form})

def movie_page(request, id):
    movie = get_object_or_404(Movie, id=id)
    torrents=TorrentTable(Torrent.objects.filter(movie_id=movie))

    return render(request, 'movie_list/movie_page.html', {'movie':movie, 'torrents':torrents})


def email(request):
    movie_list = MovieTable(Movie.objects.filter(created_date__gte=date.today() , imdb_rating__gt=6.9).order_by("-year"))
    RequestConfig(request).configure(movie_list)

    return render(request, 'movie_list/email.html', {'movies':movie_list})
