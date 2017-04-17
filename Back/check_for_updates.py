import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FirstSite.settings")
django.setup()
import Back.tracker
from movie_list.models import Movie, Torrent
from datetime import datetime, timezone
x = Back.tracker.rutracker.get_torrents()
#y = Back.tracker.nnmclub.get_torrents()

today_list = x


for x in today_list:
    try:
        m = Movie.objects.get(original_name=x["movie"], year= x["year"])
    except:
        m = Movie.objects.create(original_name=x["movie"], year= x["year"], russian_name = x["russian_name"])
        m = m.check_imdb()
    if m.imdb_rating > 6.9:
        Torrent.objects.create(movie_id = m, torrent_size = x["size"], link_to_topic = x["torrent_link"],
                               link_to_torrent_download = x["download_link"])
