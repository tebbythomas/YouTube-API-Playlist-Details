from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework.routers import DefaultRouter
from rest_framework import status
from . import views
from .models import Playlist

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'playlist', views.PlaylistViewSet)
# The API URLs are now determined automatically by the router.


class PlaylistTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('', include(router.urls))
    ]

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        playlist_id = 'PLrtCHHeadkHptUb0gduz9pxLgvtKWznKj'
        url = reverse('playlist-detail', kwargs={"pk": playlist_id})
        response = self.client.get(url,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Playlist.objects.filter(id=playlist_id).count(), 0)
