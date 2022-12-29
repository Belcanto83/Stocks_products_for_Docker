from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock
from logistic.filters import StockFilter
from logistic.serializers import ProductSerializer, StockSerializer, StockListSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # параметры фильтрации данных:
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id']
    search_fields = ['title', 'description']
    ordering_fields = ['title']
    # pagination
    pagination_class = LimitOffsetPagination


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    list_serializer_class = StockListSerializer
    # параметры фильтрации данных:
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = StockFilter
    search_fields = ['products__title', 'products__description', 'address']
    # pagination
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        return self.serializer_class
