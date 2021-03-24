from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import PlaylistSerializer, VideoSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Playlist, Video
from dynamic_rest.viewsets import DynamicModelViewSet
from googleapiclient.discovery import build
import json
import google_auth_oauthlib.flow
from google.auth.transport.requests import Request
import pickle
from dotenv import load_dotenv
import os
from rest_framework.exceptions import APIException

load_dotenv()

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_API_KEY = 'AIzaSyBLLTTMYPMROMDrEbtRX6kZFuWW615GyVQ'

youtube_obj = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


class PlaylistViewSet(DynamicModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    model = Playlist
    serializer_class = PlaylistSerializer
    queryset = Playlist.objects.all()

    @staticmethod
    def cal_duration(duration_string):
        multiplier_dict = {"S": 1, "M": 60, "H": 3600}
        curr_multiplier = 1
        curr_exponent = 0
        duration_in_secs = 0
        for char in reversed(duration_string):
            if char in multiplier_dict:
                curr_multiplier = multiplier_dict[char]
                curr_exponent = 0
            if char not in multiplier_dict:
                duration_in_secs += 10**curr_exponent * curr_multiplier * int(char)
                curr_exponent += 1
        return duration_in_secs

    def get_vid_details(self, video_id):
        vid_details = dict()
        request = youtube_obj.videos().list(
            part="snippet, contentDetails, statistics",
            id=video_id
        )
        vid_response = request.execute()
        if len(vid_response["items"]) > 0:
            vid_details['title'] = vid_response["items"][0]["snippet"]["title"]
            vid_details['duration'] = self.cal_duration(vid_response["items"][0]["contentDetails"]["duration"][2:])
            vid_details['likes'] = int(vid_response["items"][0]["statistics"]["likeCount"])
            vid_details['dislikes'] = int(vid_response["items"][0]["statistics"]["dislikeCount"])
            vid_details['view_count'] = int(vid_response["items"][0]["statistics"]["viewCount"])
        return vid_details

    @staticmethod
    def get_vid_ids_from_playlist(playlist_id):
        vid_ids = list()
        next_page_token = ""
        # Accessing each of the videos of the plylist - 1 page at a time
        # Each page contains the details of 50 videos
        while next_page_token is not "NA":
            request = youtube_obj.playlistItems().list(
                part="contentDetails",
                maxResults="50",
                pageToken=next_page_token,
                playlistId=playlist_id
            )
            response = request.execute()
            # print("\n\nPlaylist json response:")
            # print(json.dumps(response, indent=4))
            vid_items = response["items"]
            for vid_item in vid_items:
                vid_ids.append(vid_item["contentDetails"]["videoId"])
            if "nextPageToken" in response:
                next_page_token = response["nextPageToken"]
            else:
                next_page_token = "NA"
                break
        return vid_ids

    @staticmethod
    def basic_playlist_details(playlist_id):
        basic_details = dict()
        request = youtube_obj.playlists().list(
            part="snippet, contentDetails",
            id=playlist_id
        )
        response = request.execute()
        if len(response["items"]) > 0:
            basic_details["thumbnail_url"] = response["items"][0]["snippet"]["thumbnails"]["default"]["url"]
            basic_details["title"] = response["items"][0]["snippet"]["title"]
            basic_details["channel_title"] = response["items"][0]["snippet"]["channelTitle"]
            basic_details["video_count"] = response["items"][0]["contentDetails"]["itemCount"]
        else:
            raise APIException("Invalid playlist id entered")
        return basic_details

    def retrieve(self, request, pk=None, *args, **kwargs):
        # request = youtube_obj.playlists().list(
        #     part="snippet, status, id, player, localizations, contentDetails",
        #     id=pk
        # )
        output = dict()
        retrieved_playlist_obj = Playlist.objects.filter(id=pk).first()
        basic_playlist_details = self.basic_playlist_details(pk)
        if not retrieved_playlist_obj or retrieved_playlist_obj.video_count != basic_playlist_details['video_count']:
            if retrieved_playlist_obj:
                retrieved_playlist_obj.delete()
            playlist_obj = Playlist(id=pk, title=basic_playlist_details['title'],
                                    channel_title=basic_playlist_details['channel_title'],
                                    thumbnail_url=basic_playlist_details['thumbnail_url'],
                                    video_count=basic_playlist_details['video_count'])
            playlist_obj.save()
            output = basic_playlist_details
            video_ids = self.get_vid_ids_from_playlist(pk)
            video_details = dict()
            playlist_view_count = 0
            playlist_duration_count = 0
            for video_id in video_ids:
                video_details[video_id] = self.get_vid_details(video_id)
                video_obj = Video(id=video_id,
                                  playlist=playlist_obj,
                                  title=video_details[video_id]['title'],
                                  view_count=video_details[video_id]['view_count'],
                                  duration=video_details[video_id]['duration'],
                                  likes=video_details[video_id]['likes'],
                                  dislikes=video_details[video_id]['dislikes'])
                playlist_view_count += int(video_details[video_id]['view_count'])
                playlist_duration_count += int(video_details[video_id]['duration'])
                video_obj.save()
            playlist_obj.view_count = playlist_view_count
            playlist_obj.total_duration = playlist_duration_count
            playlist_obj.save()
            output['view_count'] = playlist_obj.view_count
            output['total_duration'] = playlist_obj.total_duration
            output['video_details'] = video_details
        else:
            output['thumbnail_url'] = retrieved_playlist_obj.thumbnail_url
            output['title'] = retrieved_playlist_obj.title
            output['channel_title'] = retrieved_playlist_obj.channel_title
            output['video_count'] = retrieved_playlist_obj.video_count
            output['view_count'] = retrieved_playlist_obj.view_count
            output['total_duration'] = retrieved_playlist_obj.total_duration
            videos = dict()
            for vid_obj in Video.objects.filter(playlist=retrieved_playlist_obj):
                videos[vid_obj.id] = dict()
                videos[vid_obj.id]['title'] = vid_obj.title
                videos[vid_obj.id]['duration'] = vid_obj.duration
                videos[vid_obj.id]['likes'] = vid_obj.likes
                videos[vid_obj.id]['dislikes'] = vid_obj.dislikes
                videos[vid_obj.id]['view_count'] = vid_obj.view_count
            output['video_details'] = videos
        return Response(output)


class VideoViewSet(DynamicModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    model = Video
    serializer_class = VideoSerializer
    queryset = Video.objects.all()

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Video.objects.all()
        retrieved_video = get_object_or_404(queryset, pk=pk)
        serializer = VideoSerializer(retrieved_video)
        return Response(serializer.data)
