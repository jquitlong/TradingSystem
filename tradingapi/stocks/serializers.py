from rest_framework import serializers
from .models import Stock, StockOrder

# Create your serializers here
class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = ['id', 'name', 'price']

class StockOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockOrder
        fields = ['id', 'owner', 'quantity', 'created_time']