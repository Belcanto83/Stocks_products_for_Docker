import django_filters

from logistic.models import Stock


class StockFilter(django_filters.FilterSet):

    product_name = django_filters.rest_framework.CharFilter(
        field_name='products__title',
        lookup_expr='icontains'
    )
    address = django_filters.rest_framework.CharFilter(
        field_name='address',
        lookup_expr='icontains'
    )

    product_id = django_filters.rest_framework.NumberFilter(
        field_name='products',
    )

    class Meta:
        model = Stock
        fields = ['id', 'product_name', 'address', 'product_id']
