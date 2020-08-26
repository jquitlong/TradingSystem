from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, RequestsClient


# Create your tests here.
class UserTestCase(APITestCase):
    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        self.first_name = 'Joanna'
        self.last_name = 'Quitlong'
        self.signin_url = 'http://127.0.0.1:8000/api/v1/signin'

    def test_login(self):
        user = User.objects.create(username=self.username)
        user.set_password(self.password)
        user.save()

        client = RequestsClient()
        response = client.post(self.signin_url, json={
            "username": self.username,
            "password": self.password
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_get_user(self):
        user = User.objects.create(username=self.username, 
            first_name=self.first_name, last_name=self.last_name)
        user.set_password(self.password)
        user.save()

        user = User.objects.filter(username=self.username)[0]
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)

    def test_update_user(self):
        user = User.objects.create(username=self.username, 
            first_name=self.first_name, last_name=self.last_name)
        user.set_password(self.password)
        user.save()

        new_username = 'newusername'
        new_first_name = 'newfirstname'
        new_last_name = 'newlastname'

        user = User.objects.filter(username=self.username)[0]
        user.username = new_username
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.save()

        self.assertEqual(user.username, new_username)
        self.assertEqual(user.first_name, new_first_name)
        self.assertEqual(user.last_name, new_last_name)
