from django.core.management import execute_from_command_line
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from otp.models import Otp


class TestUserAPI(TestCase):
    def setUp(self):
        execute_from_command_line(["manage.py", "add_default_permissions"])
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            is_active=True
        )
        self.client = APIClient()

    def get_access_token(self):
        refresh = RefreshToken.for_user(self.user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def test_create_user(self):
        url = '/api/accounts/users/'
        data = {'email': 'newuser@example.com', 'password': 'newpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_user = User.objects.get(email='newuser@example.com')
        created_otp = Otp.objects.filter(user=new_user).first()
        self.assertIsNotNone(created_otp)

    def test_login_user_email(self):
        url = '/api/accounts/login/'
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        refresh_url = '/api/accounts/login/refresh/'
        access_token = self.get_access_token()['refresh']

        refresh_data = {'refresh': access_token}
        response = self.client.post(refresh_url, refresh_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
