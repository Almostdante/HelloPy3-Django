# This Python file uses the following encoding: utf-8

import bs4
import re
import os
import django
from urllib.request import HTTPCookieProcessor, build_opener
from urllib.parse import urlencode
from movie_list.models import Torrent
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FirstSite.settings")
django.setup()

def parse_link(link):
    opener = build_opener(HTTPCookieProcessor())
    page = opener.open(link)
    if link.startswith('http://rutr'):
        soup = bs4.BeautifulSoup(page, "html.parser")
    else:
        soup = bs4.BeautifulSoup(page, "html.parser")
    post = str(soup.findAll(['div', 'span'], {'class': ['postbody', 'post_body']}))
    try:
        id = str(re.search(r'(tt(\d{7}))', post).group(0))
    except:
        id = 'tt'
#    sub = True if (
#    re.search(r'титр.{,70}(\w*?(усск|rus|Rus))', post) or re.search(r'(усск|rus|Rus).{,18}(\w*?титр\w*?)',
#                                                                                 post)) else False
    return id


class Tracker:

    def __init__(self, db_id, domain):
        self.ID = db_id
        self.domain = domain
        self.gap = 0
        self.page_size = 50
        self.last_time = Torrent.objects.filter(tracker = domain).latest('created_date').created_date.replace(tzinfo=None)
        self.current_url = ''

    def get_torrents(self):
        int_result = []
        opener = build_opener(HTTPCookieProcessor())
        opener.open(self.login_url, urlencode(self.credentials).encode())
        self.current_url = self.start_url
        while True:
            print(self.current_url)
            current_page = opener.open(self.current_url)
            soup = bs4.BeautifulSoup(current_page, "html.parser")
            topics = soup.findAll(*self.how_to_find_topics)
            for topic in topics:
                torrent_time = int(topic.find(*self.how_to_find_time).u.contents[0])
                if (self.last_time - datetime.fromtimestamp(torrent_time)).total_seconds() > 0:
                    break
                torrent_size = round(int(topic.find(*self.how_to_find_size).u.contents[0])/2.0**30, 2)
                torrent_title = topic.find(*self.how_to_find_name_year_id)
                torrent_year = re.search(self.movie_year_regexp, str(torrent_title)).group(1)
                torrent_id = str(re.search('\d+', torrent_title['href']).group(0))
                torrent_link = self.link_to_torrent_url + torrent_id
                torrent_download_link = self.link_to_download + torrent_id
                torrent_names = str(torrent_title).split('(')[0].split('>')[-1].split(' / ')
                int_result.append({'names': reversed(torrent_names), 'id': torrent_id, 'tracker': self.domain,
                                   'year': torrent_year, 'size': torrent_size, 'torrent_link': torrent_link,
                                   'torrent_download_link': torrent_download_link})
            else:
                if self.gap > 399:
                    break
                self.gap += self.page_size
                next = soup.findAll(self.how_to_find_next_page)
                next_search = re.search(r'search_id=(\w+)', str(next))
                if next_search:
                    search_id = next_search.group(1)
                    self.current_url = self.search_url % (search_id, self.gap)
                else:
                    break
                continue
            break

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
nnmclub.how_to_find_name_year_id = ('a', {'class': ('genmed topictitle', 'seedmed topictitle', 'genmed', 'genmed topicpremod')})
nnmclub.search_url = 'http://nnmclub.to/forum/tracker.php?search_id=%s&start=%s'
nnmclub.how_to_find_next_page = ('span', {'class': 'nav'})
nnmclub.movie_year_regexp = '\((\d{4})\)'

if __name__ == '__main__':
    print(nnmclub.get_torrents())
    print(rutracker.get_torrents())
