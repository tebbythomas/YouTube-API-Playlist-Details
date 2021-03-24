from django.contrib import admin

from playlist.models import Playlist, Video


models = [Playlist, Video]

for model in models:
    admin.site.register(model)
