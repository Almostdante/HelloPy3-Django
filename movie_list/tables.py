import django_tables2 as tables
from .models import Movie, Torrent

class MovieTable(tables.Table):
#    name = tables.TemplateColumn('<a href="/post/{{record.id}}">{{record.original_name}}</a>')
    poster = tables.TemplateColumn('<img src = "{{record.poster}}" "width" = "10%" >', attrs= { "td" :{"width": "5%", }})

    movie_info = tables.TemplateColumn('<table width = 100% height = 100% border=1">'
                                        '<tr><td><h1><a href="http://www.imdb.com/title/tt{{record.imdb_id}}/">{{record.original_name}}</a></h1></td></tr> '
                                        '<tr><td>{{record.year}}</td></tr>' 
                                        '<tr><td>{{record.genre}}</td></tr>' 
                                        '<tr><td>{{record.director}}</td></tr>' 
                                        '<tr><td>{{record.imdb_rating}}</td></tr>' 
                                        '<tr><td>{{record.plot}}</td></tr>' 
                                     '</table>', attrs= { "td" :{"width":"60%", }})
    torrents = tables.TemplateColumn('<table width=100% height = 100% border=1>'
                                     '<tr><th>Tracker</th><th>Size</th> '
                                     '  {% for torrent in record.get_torrents %}    '
                                     '      <tr><td><a href="{{torrent.link_to_topic}}">{{torrent.tracker}}</a></td>'
                                     '      <td>{{ torrent.torrent_size }}</td></tr>  '
                                     '  {% endfor %} '
                                     '</table>', attrs= { "td" :{"width":"15%", }})
    class Meta:
        model = Movie
        fields = ('poster', 'movie_info')
        attrs = {'class': 'paleblue','width':'90%', 'align': 'center', 'border': 1}

class TorrentTable(tables.Table):
    tracker = tables.TemplateColumn('<a href="{{record.link_to_topic}}">{{record.tracker}}</a>')
    class Meta:
        model = Torrent
        fields = ('tracker', 'torrent_size')
        attrs = {'class': 'paleblue','width':'170%'}
