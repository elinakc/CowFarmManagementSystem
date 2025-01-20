from http.client import responses

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import  APIClient
from app.Users_app.models import CustomUser
from rest_framework import status
from .models import CustomUser




# Create your tests here.

def test_create_user(self):
    url = reverse('customer-list')
    data ={
        'username':'new user',
        'email':'newuser@example.com',
        'password':'newness123',
        'roles':'vets',

    }
    response = self.client.post(url, data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(CustomUser.objects.count(),2)


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data ={
            'username':'tester',
            'email':'test@exmaple.com',
            'password':'test pass123',
            'roles':'manager'


            }
        self.user = CustomUser.objects.create_user(**self.user_data)
    def test_login_user(self):
        url = reverse('login')
        data ={
            'username':'text@example.com',
            'password':'test pass123'
        }

        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)

    def test_logout_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('logout')
        response =self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)