from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0.0)

class StockOrder(models.Model):
    stock = models.ForeignKey(Stock, related_name='stock_order', on_delete=models.PROTECT)
    owner = models.ForeignKey(User, related_name='place_order', on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)