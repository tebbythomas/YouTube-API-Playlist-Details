from rest_framework import serializers
from dynamic_rest.serializers import DynamicModelSerializer, DynamicRelationField
from .models import Playlist, Video


class PlaylistSerializer(DynamicModelSerializer):

    class Meta:
        model = Playlist
        fields = ("id", "title", "channel_title", "thumbnail_url", "view_count", "video_count", "total_duration")


class VideoSerializer(DynamicModelSerializer):
    class Meta:
        model = Video
        fields = ("id", "playlist", "title", "view_count", "duration", "likes", "dislikes")

    plalist = DynamicRelationField('PlaylistSerializer', embed=False)
