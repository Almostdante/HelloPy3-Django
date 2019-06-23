import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FirstSite.settings")
django.setup()
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http.request import HttpRequest
from movie_list import models
from movie_list import tables
from datetime import date
from django_tables2 import RequestConfig



def send_update(recipient):
    to = []
    to.append(recipient)
    request=HttpRequest()
    m= tables.MovieTable(models.Movie.objects.filter(created_date__gte=date.today() , imdb_rating__gt=6.9, year__gt=2016).order_by("-year"))
    RequestConfig(request).configure(m)
    msg_html = render_to_string('movie_list/email.html', context={'movies' :m}, request=request)
    msg_txt = 'txt'
    send_mail(
        'Fresh Movies',
        msg_txt,
        'almostdante@gmail.com',
        to,
        html_message=msg_html,
    )
    return