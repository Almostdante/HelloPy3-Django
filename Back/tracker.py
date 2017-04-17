# This Python file uses the following encoding: utf-8

import bs4
import re
from urllib.request import HTTPCookieProcessor, build_opener
from urllib.parse import urlencode
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FirstSite.settings")
django.setup()

class Tracker:

    def __init__(self, db_id, domain):
        self.ID = db_id
        self.domain = domain
        self.gap = 0
        self.page_size = 50
        self.current_last_time = 0
        self.previous_last_time = 0

    def get_torrents(self):
        int_result = []
        opener = build_opener(HTTPCookieProcessor())
        opener.open(self.login_url, urlencode(self.credentials).encode())
        current_url = self.start_url
        x = True
        while x:
            current_page = opener.open(current_url)
            soup = bs4.BeautifulSoup(current_page, "html.parser")
            topics = soup.findAll(*self.how_to_find_topics)
            for topic in topics:
                torrent_time = int(topic.find(*self.how_to_find_time).u.contents[0])
                self.current_last_time = max(torrent_time, self.current_last_time)
                if torrent_time < self.previous_last_time:
                    x = False
                    break
                try:
                    torrent_size = round(int(topic.find(*self.how_to_find_size).u.contents[0])/2.0**30, 2)
                    torrent_title = topic.find(*self.how_to_find_name_year_id)
                    torrent_movie_year = re.search(self.movie_year_regexp, str(torrent_title)).group(1)
                    torrent_id = str(re.search('\d+', torrent_title['href']).group(0))
                    torrent_link = self.link_to_torrent_url + torrent_id
                    torrent_download_link = self.link_to_download + torrent_id
                    torrent_russian_name = str(torrent_title.contents[0]).split('(')[0].split('/')[0].strip('<b>')
                except:
                    continue
                for title in str(torrent_title.contents[0]).split('(')[0].split('/'):
                    if re.search('[a-zA-Z0-9]+', title) and not (title.startswith('<') or re.search('[а-яА-Я]+', title)):
                       int_result.append({'russian_name': torrent_russian_name, 'torrent_link': torrent_link,
                                           'download_link': torrent_download_link, 'movie': title.strip(),
                                           'year': torrent_movie_year, 'size': torrent_size})
            self.gap += self.page_size
            if self.gap > 200:
                x = False
                break
            next = soup.findAll(self.how_to_find_next_page)
            next_search = re.search(r'search_id=(\w+)', str(next))
            if next_search:
                search_id = next_search.group(1)
                current_url = self.search_url % (search_id, self.gap)
            else:
                x = False
        return int_result


rutracker = Tracker(1, 'rutracker.org')
rutracker.credentials = {'login_username': b'cheshiremajor', 'login_password': b'ZNt,zK.,k.', 'login': 'Вход', }
rutracker.login_url = 'http://%s/forum/login.php' % rutracker.domain
rutracker.start_url = 'http://%s/forum/tracker.php?f=2198,2199,2201,2339,313,930&o=1&tm=14' % rutracker.domain
rutracker.how_to_find_topics = ('tr', {'class': 'tCenter hl-tr'})
rutracker.how_to_find_time = ('td', {'class': 'row4 small nowrap'})
rutracker.how_to_find_size = ('td', {'class': 'row4 small nowrap tor-size'})
rutracker.link_to_torrent_url = 'http://%s/forum/viewtopic.php?t=' % rutracker.domain
rutracker.link_to_download = 'http://dl.%s/forum/dl.php?t=' % rutracker.domain
rutracker.how_to_find_name_year_id = ('a', {'class': ('med tLink hl-tags bold', 'med tLink')})
rutracker.search_url = 'http://rutracker.org/forum/tracker.php?search_id=%s&start=%s'
rutracker.how_to_find_next_page = ('a', {'class': 'pg'})
rutracker.movie_year_regexp = '\[(\d{4})'

nnmclub = Tracker(2, 'nnmclub.to')
nnmclub.credentials = {'username': b'almostdante', 'password': b'Welcome2012', 'login': 'Вход', }
nnmclub.login_url = 'http://%s/forum/login.php' % nnmclub.domain
nnmclub.start_url = 'http://%s/forum/tracker.php?f=954,885,912,227,661&o=1&tm=14' % nnmclub.domain
nnmclub.how_to_find_topics = ('tr', {'class': ('prow1', 'prow2')})
nnmclub.how_to_find_time = ('td', {'title': 'Добавлено'})
nnmclub.how_to_find_size = ('td', {'class': 'gensmall'})
nnmclub.link_to_torrent_url = 'http://%s/forum/viewtopic.php?t=' % nnmclub.domain
nnmclub.link_to_download = 'http://%s/forum/download.php?id=' % nnmclub.domain
nnmclub.how_to_find_name_year_id = ('a', {'class': ('genmed topictitle', 'seedmed topictitle')})
nnmclub.search_url = 'http://nnmclub.to/forum/tracker.php?search_id=%s&start=%s'
nnmclub.how_to_find_next_page = ('span', {'class': 'nav'})
nnmclub.movie_year_regexp = '\((\d{4})\)'

if __name__ == '__main__':
    print(nnmclub.get_torrents())
    print(rutracker.get_torrents())
