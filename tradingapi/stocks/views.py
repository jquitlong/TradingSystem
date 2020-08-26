from django.db.models import F, Sum
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)

from .models import Stock, StockOrder
from .serializers import StockOrderSerializer, StockSerializer


# Create your views here.
class StockView(viewsets.ModelViewSet):
    model = Stock
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    @action(detail=True, methods=['post'], url_name='place-trade', url_path='place-trade')
    def place_trade(self, request, *args, **kwargs):
        try:
            request_data = self.request.data
            quantity = request_data['quantity']
            instance = self.get_object()

            total = StockOrder.objects.filter(stock=instance, 
            owner=request.user).aggregate(Sum(F('quantity')))['quantity__sum'] 
            if not total:
                total = 0

            if int(quantity) + int(total) < 0:
                return Response(data='You dont have enough stock', 
                status=HTTP_400_BAD_REQUEST)     

            stock_order = StockOrder.objects.create(stock=instance, 
            owner=request.user, quantity=quantity)
            stock_order = StockOrderSerializer(stock_order)
            
            return Response(data=stock_order.data, status=HTTP_200_OK)
        except:
            return Response(data={}, status=HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['get'], url_name='total-invested', url_path='total-invested')
    def total_invested(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            total_invested = StockOrder.objects.filter(stock=instance, owner=request.user
                ).aggregate(Sum(F('quantity')))['quantity__sum'] * instance.price
            return Response({'total_invested': total_invested}, status=HTTP_200_OK)
        except:
            return Response({'total_invested': 0}, status=HTTP_200_OK)

