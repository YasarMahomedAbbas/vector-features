from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class FeatureAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a simple payload to test post endpoint.
        self.feature_payload ={
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [15, 32]
            },
            "properties": {
                "name": "Test Feature"
            }
        }
    def test_unauthenticated_user_can_list_features(self):
        response = self.client.get('/features/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_cannot_create_feature(self):
        response = self.client.post('/features/', self.feature_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_feature(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/features/', self.feature_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
