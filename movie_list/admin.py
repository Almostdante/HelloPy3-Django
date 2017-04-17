from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Movie, Torrent

admin.site.register(Movie)
admin.site.register(Torrent)
