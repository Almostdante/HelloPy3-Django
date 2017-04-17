from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.main_movie_list, name='main_movie_list'),
    url(r'^post/(?P<id>[0-9]+)/$', views.movie_page, name='movie_page'),
]
