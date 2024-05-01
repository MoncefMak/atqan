from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from otp.models import Otp


class TestUserAPI(TestCase):
    def setUp(self):
        self.otp_code = 'A2B4C6'
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.otp = Otp.objects.create(
            user=self.user,
            otp_code=self.otp_code
        )
        self.client = APIClient()

    def test_verify_otp(self):
        response = self.client.post('/api/otp/verify-otp/', {'otp_code': self.otp_code})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User activated successfully')
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertFalse(Otp.objects.get(otp_code=self.otp_code).is_active)

    def invalid_otp(self):
        response = self.client.post('/api/otp/verify-otp/', {'otp_code': 'invalid_otp'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid OTP', response.data['error'])

    def already_used(self):
        self.otp.is_active = False
        self.otp.save()
        response = self.client.post('/api/otp/verify-otp/', {'otp_code': self.otp_code})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid OTP', response.data['error'])
