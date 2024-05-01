from django.contrib.auth.models import Group
from django.core.management import execute_from_command_line
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


class TestUserAPI(TestCase):
    @override_settings(TEST_CASE=True)
    def setUp(self):
        execute_from_command_line(["manage.py", "add_default_permissions"])
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            is_active=True
        )
        admin_group = Group.objects.get(name='Admin')
        admin_group.user_set.add(self.user)
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
        access_token = self.get_access_token()['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check if the user is created
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_patch_user(self):
        user_to_update = User.objects.create_user(
            email='update@example.com',
            password='updatepassword'
        )
        admin_group = Group.objects.get(name='Client')
        admin_group.user_set.add(user_to_update)
        url = f'/api/accounts/users/{user_to_update.id}/'
        data = {'email': 'updateduser@example.com'}
        access_token = self.get_access_token()['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify that the user data has been updated
        updated_user = User.objects.get(id=user_to_update.id)
        self.assertEqual(updated_user.email, 'updateduser@example.com')

    def test_delete_user(self):
        user_to_delete = User.objects.create_user(
            email='delete@example.com',
            password='deletepassword'
        )
        admin_group = Group.objects.get(name='Client')
        admin_group.user_set.add(user_to_delete)
        url = f'/api/accounts/users/{user_to_delete.id}/'
        access_token = self.get_access_token()['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Check if the user is deleted
        self.assertFalse(User.objects.filter(email='delete@example.com').exists())
