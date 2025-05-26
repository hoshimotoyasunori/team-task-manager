from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAPITests(APITestCase):
    def test_user_registration(self):
        url = reverse('user-register')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_jwt_authentication(self):
        user = User.objects.create_user(username='jwtuser', password='jwtpass123')
        url = reverse('token_obtain_pair')
        data = {'username': 'jwtuser', 'password': 'jwtpass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_profile_retrieve(self):
        user = User.objects.create_user(username='profileuser', password='profilepass123')
        url = reverse('user-me')
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'profileuser')
