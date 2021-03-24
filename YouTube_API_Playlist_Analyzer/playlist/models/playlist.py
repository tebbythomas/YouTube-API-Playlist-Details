from django.db import models


class Playlist(models.Model):
    id = models.CharField(primary_key=True, max_length=100, unique=True, null=False, blank=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    channel_title = models.CharField(max_length=100, null=False, blank=False)
    thumbnail_url = models.CharField(max_length=100, null=True, blank=True)
    view_count = models.IntegerField(null=True, blank=True)
    video_count = models.IntegerField(null=True, blank=True)
    total_duration = models.IntegerField(null=True, blank=True)
    # most_viewed_video_id = models.CharField(max_length=100, null=True, blank=True)
    # most_viewed_video_title = models.CharField(max_length=100, null=True, blank=True)
    # most_viewed_video_view_count = models.CharField(max_length=100, null=True, blank=True)
    # least_viewed_video_id = models.CharField(max_length=100, null=True, blank=True)
    # least_viewed_video_title = models.CharField(max_length=100, null=True, blank=True)
    # least_viewed_video_view_count = models.CharField(max_length=100, null=True, blank=True)


class Video(models.Model):
    id = models.CharField(primary_key=True, max_length=100, unique=True, null=False, blank=False)
    playlist = models.ForeignKey(to='Playlist', related_name='videos', on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    view_count = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    likes = models.IntegerField(null=True, blank=True)
    dislikes = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = (('id', 'playlist'),)


