import os
import sys
import json
import django
from django.utils import timezone
sys.path.append("/home/hello/HelloPy3-Django")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FirstSite.settings")
django.setup()
import Back.tracker
from movie_list.models import Movie, Torrent
import Back.send_update_to_email


me  = 'almostdante@gmail.com'
x = Back.tracker.rutracker.get_torrents()
y = Back.tracker.nnmclub.get_torrents()

today_list = x + y
js = json.decoder.JSONDecoder()


for topic in today_list:
    names_plus = ['+++' + name.strip() + '+++' for name in topic['names']]
    m = 0
    for name in names_plus:
        try:
            m = Movie.objects.get(names__contains=name, year=topic["year"])
            list_names = js.decode(m.names)
            list_names.append(name for name in names_plus if name not in list_names)
            list_names = json.dumps(list_names, ensure_ascii=False)
            m.names = list_names
            m.save()
            if (timezone.now() - m.published_date).days > 7:
                m.check_imdb()
            break
        except:
            pass
    if not m:
        temp = Back.tracker.parse_link(topic['torrent_link'])[2:]
        if temp:
            try:
                m = Movie.objects.get(imdb_rating=temp)
                if (timezone.now() - m.published_date).days > 7:
                    m.check_imdb()
            except:
                m = Movie.objects.create(imdb_id=temp, names=json.dumps(names_plus, ensure_ascii=False),
                                         year=topic["year"])
                m.check_imdb()
        else:
            m = Movie.objects.create(names=json.dumps(names_plus, ensure_ascii=False), year=topic["year"])
            m.check_imdb()
    if m.imdb_rating > 6.9:
        Torrent.objects.create(movie_id=m, torrent_size=topic["size"], torrent_id=topic['id'],
                               tracker=topic['tracker'], link_to_topic=topic["torrent_link"],
                               link_to_torrent_download=topic["torrent_download_link"])
    elif m.imdb_rating == 0:
        print(topic)
        for x in topic['names']:
            print(x)
Back.send_update_to_email.send_update(me)
