import json

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase, RequestsClient

from .models import Stock, StockOrder


# Create your tests here.
class UserTestCase(APITestCase):
    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        self.first_name = 'Joanna'
        self.last_name = 'Quitlong'
        self.name = 'Hershey'
        self.price = 10
        self.quantity = 12
        self.place_trade_url = 'http://127.0.0.1:8000/api/v1/stock/1/place-trade/'
        self.total_invested_url = 'http://127.0.0.1:8000/api/v1/stock/1/total-invested/'
        self.stock_url = 'http://127.0.0.1:8000/api/v1/stock/'

    def test_create_get_stock(self):
        stock = Stock.objects.create(name=self.name, price=self.price)

        stock = Stock.objects.filter(name=self.name)[0]
        self.assertEqual(stock.name, self.name)
        self.assertEqual(stock.price, self.price)
    
    def test_update_stock(self):
        stock = Stock.objects.create(name=self.name, price=self.price)

        new_name = 'Cadbury'
        new_price = 50

        stock = Stock.objects.filter(name=self.name)[0]
        stock.name = new_name
        stock.price = new_price
        stock.save()

        self.assertEqual(stock.name, new_name)
        self.assertEqual(stock.price, new_price)

    def test_create_get_stock_order(self):
        stock = Stock.objects.create(name=self.name, price=self.price)
        user = User.objects.create(username=self.username, 
            first_name=self.first_name, last_name=self.last_name)
        
        stockOrder = StockOrder.objects.create(stock=stock, owner=user,
            quantity=self.quantity)
        stockOrder = StockOrder.objects.filter(stock=stock, owner=user)[0]
        
        self.assertEqual(stockOrder.stock, stock)
        self.assertEqual(stockOrder.owner, user)
        self.assertEqual(stockOrder.quantity, self.quantity)

    def test_update_stock_order(self):
        stock = Stock.objects.create(name=self.name, price=self.price)
        user = User.objects.create(username=self.username, 
            first_name=self.first_name, last_name=self.last_name)
        
        stockOrder = StockOrder.objects.create(stock=stock, owner=user,
            quantity=self.quantity)
        stockOrder = StockOrder.objects.filter(stock=stock, owner=user)[0]

        new_quantity = 50
        stockOrder.quantity = new_quantity
        stockOrder.save()
        
        self.assertEqual(stockOrder.stock, stock)
        self.assertEqual(stockOrder.owner, user)
        self.assertEqual(stockOrder.quantity, new_quantity)

    def test_place_trade(self):
        stock = Stock.objects.create(name=self.name, price=self.price)
        user = User.objects.create(username=self.username)
        user.set_password(self.password)
        user.save()

        token = Token.objects.create(user=user) 

        client = APIClient()

        client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))
        response = client.post(self.place_trade_url, data={
            "quantity": self.quantity
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_total_invested(self):
        stock = Stock.objects.create(name=self.name, price=self.price)
        user = User.objects.create(username=self.username)
        user.set_password(self.password)
        user.save()

        stockOrder = StockOrder.objects.create(stock=stock, owner=user,
            quantity=self.quantity)

        token = Token.objects.create(user=user) 

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

        response = client.get(self.total_invested_url)
        total = json.loads(response.content)['total_invested']
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(total, self.quantity*self.price)

    def test_create_stock_endpoint(self):
        user = User.objects.create(username=self.username)
        user.set_password(self.password)
        user.save()

        token = Token.objects.create(user=user) 

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

        response = client.post(self.stock_url, data={
            "name": self.name,
            "price": self.price
        })
        name = json.loads(response.content)['name']
        price = json.loads(response.content)['price']
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(name, self.name)      
        self.assertEqual(price, self.price)  

    def test_get_stock_endpoint(self):
        stock = Stock.objects.create(name=self.name, price=self.price)
        user = User.objects.create(username=self.username)
        user.set_password(self.password)
        user.save()

        token = Token.objects.create(user=user) 

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

        response = client.get(self.stock_url +' 1/')
        name = json.loads(response.content)['name']
        price = json.loads(response.content)['price']
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(name, self.name)      
        self.assertEqual(price, self.price) 

    def test_update_stock_endpoint(self):
        stock = Stock.objects.create(name=self.name, price=self.price)
        user = User.objects.create(username=self.username)
        user.set_password(self.password)
        user.save()

        token = Token.objects.create(user=user) 
        new_name = 'Cadbury'
        new_price = 50

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

        response = client.put(self.stock_url + '1/', data={
            "name": new_name,
            "price": new_price
        })
        name = json.loads(response.content)['name']
        price = json.loads(response.content)['price']
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(name, new_name)      
        self.assertEqual(price, new_price)   