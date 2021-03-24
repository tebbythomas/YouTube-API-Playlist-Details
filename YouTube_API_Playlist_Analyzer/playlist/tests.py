from rest_framework.test import RequestsClient
# from .models import Playlist
import json


client = RequestsClient()
response = client.get('http://127.0.0.1:8000/playlist/PLrtCHHeadkHptUb0gduz9pxLgvtKWznKj')
assert response.status_code == 200
# obj = Playlist.objects.filter(id='PLrtCHHeadkHptUb0gduz9pxLgvtKWznKj').first()
# assert obj.id == 'PLrtCHHeadkHptUb0gduz9pxLgvtKWznKj'
reponse_body = json.loads(response._content)
assert reponse_body['video_count'] == 7

response = client.get('http://127.0.0.1:8000/playlist/abc')
assert response.status_code == 500
reponse_body = json.loads(response._content)
assert reponse_body['detail'] == 'Invalid playlist id entered'

