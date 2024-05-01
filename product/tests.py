from django.contrib.auth.models import Group
from django.core.management import execute_from_command_line
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from product.models import Product


# Create your tests here.
class TestUserAPI(TestCase):
    def setUp(self):
        execute_from_command_line(["manage.py", "add_default_permissions"])
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            is_active=True
        )
        admin_group = Group.objects.get(name='Client')
        admin_group.user_set.add(self.user)
        self.client = APIClient()

    def get_access_token(self):
        refresh = RefreshToken.for_user(self.user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def test_create_product_authenticated(self):
        access_token = self.get_access_token()['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        product_data = {
            'name': 'Test Product',
            'price': 9.99
        }
        response = self.client.post('/api/product/create/', data=product_data)
        self.assertEqual(response.status_code, 201)
        print(Product.objects.filter(name='Test Product', price=9.99).first().created_by)
        self.assertTrue(Product.objects.filter(name='Test Product', price=9.99).exists())


    def test_create_product_unauthenticated(self):
        product_data = {
            'name': 'Test Product',
            'price': 9.99
        }
        response = self.client.post('/api/product/create/', data=product_data)
        self.assertEqual(response.status_code, 401)
        self.assertFalse(Product.objects.filter(name='Test Product', price=9.99).exists())
