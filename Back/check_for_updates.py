import os
import sys
import json
import django
sys.path.append("/home/hello/HelloPy3-Django")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FirstSite.settings")
django.setup()
import Back.send_update_to_email
from Back.tracker import rutracker, nnmclub, rarbg_api, parse_link
from django.utils import timezone
from movie_list.models import Movie, Torrent



me = 'almostdante@gmail.com'
x = rutracker.get_torrents()
print (len(x))
y = nnmclub.get_torrents()
print (len(y))
z = rarbg_api.get_torrents_api()
print (len(z))
today_list = x + y + z
js = json.decoder.JSONDecoder()

for topic in today_list:
    if not topic['torrent_movie_id']:
        names_plus = ['+++' + name.strip() + '+++' for name in topic['names']]
        m = 0
        for name in names_plus:
            try:
                m = Movie.objects.get(names__contains=name, year=topic["year"])
                list_names = js.decode(m.names)
                list_names = list_names+[name for name in names_plus if name not in list_names]
                list_names = json.dumps(list_names, ensure_ascii=False)
                m.names = list_names
                m.save()
                if (timezone.now() - m.published_date).days > 7:
                    m.check_imdb()
                break
            except Movie.DoesNotExist:
                pass
        if not m:
            temp = parse_link(topic['torrent_link'])[2:]
            m = Movie.objects.get_or_create(imdb_id=temp, defaults= {'names': json.dumps(names_plus, ensure_ascii=False), 'year': topic["year"]})[0]
            m.check_imdb()
    else:
        m = Movie.objects.get(id = topic['torrent_movie_id'])
    if m.imdb_rating > 6.9:
        Torrent.objects.create(movie_id=m, torrent_size=topic["size"], torrent_id=topic['id'],
                               tracker=topic['tracker'], link_to_topic=topic["torrent_link"],
                               link_to_torrent_download=topic["torrent_download_link"])
    elif m.imdb_rating == 0:
        print(topic)
Back.send_update_to_email.send_update(me)
