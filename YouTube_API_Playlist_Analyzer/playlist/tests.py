# from rest_framework.test import RequestsClient
# # from .models import Playlist
# import json
#
#
# client = RequestsClient()
# response = client.get('http://127.0.0.1:8000/playlist/PLrtCHHeadkHptUb0gduz9pxLgvtKWznKj')
# assert response.status_code == 200
# # obj = Playlist.objects.filter(id='PLrtCHHeadkHptUb0gduz9pxLgvtKWznKj').first()
# # assert obj.id == 'PLrtCHHeadkHptUb0gduz9pxLgvtKWznKj'
# reponse_body = json.loads(response._content)
# assert reponse_body['video_count'] == 7
#
# response = client.get('http://127.0.0.1:8000/playlist/abc')
# assert response.status_code == 500
# reponse_body = json.loads(response._content)
# assert reponse_body['detail'] == 'Invalid playlist id entered'
#

import requests
playlist_id = 'PLrtCHHeadkHptUb0gduz9pxLgvtKWznKj'
from .models import Playlist

def test_get_playlist():
    url = f'http://0.0.0.0:8000/playlist/{playlist_id}'
    response = requests.get(url)
    assert response.status_code == 200
    assert Playlist.objects.filter(id=playlist_id).count() == 1
    url = f'http://0.0.0.0:8000/playlist/abc'
    response = requests.get(url)
    assert response.status_code == 404


test_get_playlist()
