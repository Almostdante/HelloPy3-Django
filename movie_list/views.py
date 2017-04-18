from django.shortcuts import render, get_object_or_404
from movie_list.models import Movie, Torrent

# Create your views here.


def main_movie_list(request):
    movie_list1 = Movie.objects.filter(imdb_rating__gt=6.9)
    return render(request, 'movie_list/list.html', {'movies': movie_list1})

def movie_page(request, id):
    movie = get_object_or_404(Movie, id=id)
    torrents=(Torrent.objects.filter(movie_id=movie))
    return render(request, 'movie_list/movie_page.html', {'movie':movie, 'torrents':torrents})
