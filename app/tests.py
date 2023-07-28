from django.test import TestCase, Client, override_settings
from rest_framework import status
from .models import User
from django.urls import reverse
from app.base_url import URL
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

# Create your tests here.
class RegisterAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@mail.com')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

    def test_register_success(self):
        # Define the data for the registration request
        data = {
            'username': 'nazhifhaidar',
            'password': '123haidar',
            'email': 'azusamajitenshi@gmail.com',
            'nama_depan': 'Nazhif',
            'nama_belakang': 'Haidar'
        }
        print(f"token: {self.token.key}")
        url = reverse('register')
        print(url)
        # Send a POST request to the register endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.key}")
        response = self.client.post(url, data=data)
        print(response)
        print(response.data)
        # print(response.data['message'])
        # print(response.data['data'])
        # Verify the response status code and data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User registered successfully.')
        self.assertEqual(response.data['data']['username'], 'nazhifhaidar')

        # Verify that the user was created in the database
        user_exists = User.objects.filter(username='nazhifhaidar').exists()
        self.assertTrue(user_exists)
