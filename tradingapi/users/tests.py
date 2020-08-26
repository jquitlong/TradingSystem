import json

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase, RequestsClient


# Create your tests here.
class UserTestCase(APITestCase):
    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        self.first_name = 'Joanna'
        self.last_name = 'Quitlong'
        self.signin_url = 'http://127.0.0.1:8000/api/v1/signin'
        self.user_url = 'http://127.0.0.1:8000/api/v1/account/'

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

    def test_create_user_endpoint(self):
        user = User.objects.create(username=self.username,
            first_name=self.first_name, last_name=self.last_name)
        user.set_password(self.password)
        user.save()

        token = Token.objects.create(user=user) 
        created_username = 'user_sample'
        created_password = 'password'
        created_first_name = 'first_name'
        created_last_name = 'last_name'

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

        response = client.post(self.user_url, data={
            "username": created_username,
            "password": created_password,
            "last_name": created_last_name,
            "first_name": created_first_name
        })

        username = json.loads(response.content)['username']
        last_name = json.loads(response.content)['last_name']
        first_name = json.loads(response.content)['first_name']
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(username, created_username)      
        self.assertEqual(last_name, created_last_name)  
        self.assertEqual(first_name, created_first_name)

    def test_update_user_endpoint(self):
        user = User.objects.create(username=self.username,
            first_name=self.first_name, last_name=self.last_name)
        user.set_password(self.password)
        user.save()

        token = Token.objects.create(user=user) 

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

        response = client.get(self.user_url + '1/')

        username = json.loads(response.content)['username']
        last_name = json.loads(response.content)['last_name']
        first_name = json.loads(response.content)['first_name']
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(username, self.username)      
        self.assertEqual(last_name, self.last_name)  
        self.assertEqual(first_name, self.first_name)

    def test_update_user_endpoint(self):
        user = User.objects.create(username=self.username,
            first_name=self.first_name, last_name=self.last_name)
        user.set_password(self.password)
        user.save()

        token = Token.objects.create(user=user) 
        new_username = 'user_sample'
        new_password = 'password'
        new_first_name = 'first_name'
        new_last_name = 'last_name'

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

        response = client.put(self.user_url + '1/', data={
            "username": new_username,
            "password": new_password,
            "last_name": new_last_name,
            "first_name": new_first_name
        })

        username = json.loads(response.content)['username']
        last_name = json.loads(response.content)['last_name']
        first_name = json.loads(response.content)['first_name']
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(username, new_username)      
        self.assertEqual(last_name, new_last_name)  
        self.assertEqual(first_name, new_first_name)

