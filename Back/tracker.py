# This Python file uses the following encoding: utf-8

import bs4
import re
import os
import django
import time
from urllib.request import HTTPCookieProcessor, build_opener, urlopen, Request
from urllib.parse import urlencode
from movie_list.models import Torrent
from datetime import datetime
from socket import timeout
import html5lib
import json
from movie_list.models import Movie


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FirstSite.settings")
django.setup()


def parse_link(link):
    time.sleep(0.5)
    try:
        page = urlopen(link, timeout=15)
    except (TimeoutError, timeout):
        print(link)
        print('Link parse on tracker fucked up!')
        trnt_id = 'tt'
        return trnt_id
    soup = bs4.BeautifulSoup(page, "html5lib")
    post = str(soup.findAll(['div', 'span'], {'class': ['postbody', 'post_body']}))
    try:
        trnt_id = str(re.search(r'(tt(\d{7}))', post).group(0))
    except:
        trnt_id = 'tt'
    return trnt_id


class Tracker:

    def __init__(self, db_id, domain):
        self.ID = db_id
        self.domain = domain
        self.gap = 0
        self.page_size = 50
        self.last_time = Torrent.objects.filter(tracker__startswith=domain[:3]).latest('created_date').created_date.replace(tzinfo=None)
        self.current_url = ''


    def get_torrents(self):
        int_result = []
        opener = build_opener(HTTPCookieProcessor())
        try:
            opener.open(self.login_url, urlencode(self.credentials).encode())
            self.current_url = self.start_url
        except:
            print ('Cannot login to tracker: %s' % self.domain)
            return int_result
        while True:
            time.sleep(1.5)
            print (self.current_url)
            try:
                current_page = opener.open(self.current_url, timeout=15)
            except (TimeoutError, timeout):
                print('Tracker %s seacrh page timeout:' % self.domain)
            soup = bs4.BeautifulSoup(current_page, "html.parser")
            topics = soup.findAll(*self.how_to_find_topics)
            for topic in topics:
                torrent_time = int(topic.find(*self.how_to_find_time).u.contents[0])
                if (self.last_time - datetime.fromtimestamp(torrent_time)).total_seconds() > 180:
                    print ('AAAA', self.last_time, datetime.fromtimestamp(torrent_time))
                    break
                torrent_title = topic.find(*self.how_to_find_name_year_id)
                try:
                    torrent_year = re.search(self.movie_year_regexp, str(torrent_title)).group(1)
                except:
                    print('Error parsing year for %s' % topic)
                    continue
                torrent_size = round(int(topic.find(*self.how_to_find_size).u.contents[0])/2.0**30, 2)
                torrent_id = str(re.search('\d+', torrent_title['href']).group(0))
                torrent_link = self.link_to_torrent_url + torrent_id
                torrent_download_link = self.link_to_download + torrent_id
                torrent_names = str(torrent_title).split('(')[0].split('>')[-1].split(' / ')
                int_result.append({'names': reversed(torrent_names), 'id': torrent_id, 'tracker': self.domain,
                                   'year': torrent_year, 'size': torrent_size, 'torrent_link': torrent_link,
                                   'torrent_download_link': torrent_download_link, 'torrent_movie_id': 0})

            else:
                if self.gap > 399:
                    break
                self.gap += self.page_size
                next_page = soup.findAll(self.how_to_find_next_page)
                next_search = re.search(r'search_id=(\w+)', str(next_page))
                if next_search:
                    search_id = next_search.group(1)
                    self.current_url = self.search_url % (search_id, self.gap)
                else:
                    break
                continue
            break

        return int_result


    def get_torrents_api(self):
        int_result = []
        opener = build_opener(HTTPCookieProcessor())
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15'}
        try:
            req = Request(self.login_url, headers=headers)
            token = json.load(opener.open(req))['token']
            self.current_url = Request(self.start_url % token, headers=headers)
            print (self.current_url)
        except:
            print ('Cannot get API key')
            return int_result
        try:
            current_page = opener.open(self.current_url, timeout=15)
        except:
            print('Tracker %s seacrh page timeout:' % self.domain)
            return int_result
        topics = json.load(current_page)['torrent_results']
        for topic in topics:
            torrent_time = datetime.strptime(topic['pubdate'], '%Y-%m-%d %H:%M:%S %z').replace(tzinfo=None)
            if (self.last_time - torrent_time).total_seconds() > 180:
                break
            temp_id = topic['episode_info']['imdb'][2:]
            newmovie = Movie.objects.get_or_create(imdb_id=temp_id, defaults= {'names': topic['title']})[0]
            if not (newmovie.year and newmovie.original_name and newmovie.imdb_rating):
                newmovie.check_imdb()
            torrent_year = newmovie.year
            torrent_movie_id = newmovie.id
            torrent_size = round(int(topic['size'])/2.0**30, 2)
            torrent_names = topic['title']
            torrent_id = int (topic['info_page'][78:], 16)
            torrent_link = topic['info_page'][:60] + '&app_id=123sd'+ topic['info_page'][60:]
            int_result.append({'names': reversed(torrent_names), 'id': torrent_id, 'tracker': self.domain,
                                   'year': torrent_year, 'size': torrent_size, 'torrent_link': torrent_link,
                                   'torrent_download_link': torrent_link, 'torrent_movie_id': torrent_movie_id})
        return int_result



rutracker = Tracker(1, 'rutracker.org')
rutracker.credentials = {'login_username': b'cheshiremajor', 'login_password': b'ZNt,zK.,k.', 'login': 'Вход', }
rutracker.login_url = 'http://%s/forum/login.php?redirect=tracker.php' % rutracker.domain
rutracker.start_url = 'https://%s/forum/tracker.php?f=2198,2199,2201,2339,313,930&o=1&tm=32' % rutracker.domain
rutracker.how_to_find_topics = ('tr', {'class': 'tCenter hl-tr'})
rutracker.how_to_find_time = ('td', {'class': 'row4 small nowrap'})
rutracker.how_to_find_size = ('td', {'class': 'row4 small nowrap tor-size'})
rutracker.link_to_torrent_url = 'https://%s/forum/viewtopic.php?t=' % rutracker.domain
rutracker.link_to_download = 'https://dl.%s/forum/dl.php?t=' % rutracker.domain
rutracker.how_to_find_name_year_id = ('a', {'class': ('med tLink hl-tags bold', 'med tLink')})
rutracker.search_url = 'https://%s/forum/tracker.php?search_id=' %rutracker.domain + '%s&start=%s'
rutracker.how_to_find_next_page = ('a', {'class': 'pg'})
rutracker.movie_year_regexp = '\[(\d{4})'

nnmclub = Tracker(2, 'nnmclub.to')
nnmclub.credentials = {'username': b'almostdante', 'password': b'Welcome2012', 'login': 'Вход', }
nnmclub.login_url = 'http://%s/forum/login.php' % nnmclub.domain
nnmclub.start_url = 'http://%s/forum/tracker.php?f=954,885,912,227,661&o=1&tm=30' % nnmclub.domain
nnmclub.how_to_find_topics = ('tr', {'class': ('prow1', 'prow2')})
nnmclub.how_to_find_time = ('td', {'title': 'Добавлено'})
nnmclub.how_to_find_size = ('td', {'class': 'gensmall'})
nnmclub.link_to_torrent_url = 'http://%s/forum/viewtopic.php?t=' % nnmclub.domain
nnmclub.link_to_download = 'http://%s/forum/download.php?id=' % nnmclub.domain
nnmclub.how_to_find_name_year_id = ('a', {'class': ('genmed topictitle', 'seedmed topictitle', 'genmed', 'genmed topicpremod')})
nnmclub.search_url = 'http://%s/forum/tracker.php?search_id=' % nnmclub.domain + '%s&start=%s'
nnmclub.how_to_find_next_page = ('span', {'class': 'nav'})
nnmclub.movie_year_regexp = '\((\d{4})[\-\)]'

rarbg_api = Tracker(3, 'https://torrentapi.org/pubapi_v2.php?app_id=123sd')
rarbg_api.credentials = {}
rarbg_api.login_url = '%s&get_token=get_token' % rarbg_api.domain
rarbg_api.start_url = rarbg_api.domain + '&token=%s' + '&mode=search&category=44;52&search_string=201&limit=100&format=json_extended&ranked=0'
rarbg_api.how_to_find_topics = ''
rarbg_api.how_to_find_time = ''
rarbg_api.how_to_find_size = ''
rarbg_api.link_to_torrent_url = ''
rarbg_api.link_to_download = ''
rarbg_api.how_to_find_name_year_id = ''
rarbg_api.search_url = ''
rarbg_api.how_to_find_next_page = ''
rarbg_api.movie_year_regexp = ''


if __name__ == '__main__':
    print(nnmclub.get_torrents())
    print(rarbg_api.get_torrents())
