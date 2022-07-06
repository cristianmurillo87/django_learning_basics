from math import prod
from urllib import response
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView,\
                                    GenericAPIView
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend


from store.serializers import ProductSerializer, ProductStatSerializer
from store.models import Product

class ProductsPagination(LimitOffsetPagination):
    default_limi = 10
    max_limit = 100

class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # use django-filters to add functionality
    # to the django-rest webpage to filter objects
    filter_backends = (DjangoFilterBackend, SearchFilter, )
    filter_fields = ('id', 'description', )
    pagination_class = ProductsPagination

    def get_queryset(self):
        on_sale = self.request.query_params.get('on_sale', None)
        if on_sale is None:
            return super().get_queryset()
        queryset = Product.objects.all()
        if on_sale.lower() == 'true':
            from django.utils import timezone
            now = timezone.now()
            return queryset.filter(sale_start__lte=now, sale_end__gte=now,)
        return queryset

class ProductCreate(CreateAPIView):
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        try:
            price = request.data.get('price')
            if price is not None and float(price) <= 0.0:
                raise ValidationError({'price': 'Must be above $0.00' })
        except ValueError:
            raise ValidationError({'price': 'A valid number is required'})
        return super().create(request, *args, **kwargs)

class ProductRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'
    serializer_class = ProductSerializer

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete(f'product_data_{product_id}')
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            product = response.data
            cache.set(f'product_data_{product.get("id")}',
            {
                'name': product.get("name"),
                'description': product.get("description"),
                'price': product.get("price"),
            })
        return response

class ProductStats(GenericAPIView):
    lookup_field = 'id'
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request, format=None, id=None):
        obj = self.get_object()
        serializer = ProductStatSerializer({
            'stats': {
                '2019-01-01': [5, 10, 15],
                '2019-01-02': [20, 1, 1]
            }
        })
        return Response(serializer.data)