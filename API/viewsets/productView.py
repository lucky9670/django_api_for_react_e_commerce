from rest_framework.viewsets import ModelViewSet
from API.serialization.productSerialization import ProductSerialization
from rest_framework.parsers import MultiPartParser
from rest_framework import permissions
from API.models import Product
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from lib.pagination import CustomPageNumberPagination
from knox.auth import TokenAuthentication


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass

class ProductFilter(filters.FilterSet):
    product = NumberInFilter(field_name='id', lookup_expr='in', required=False, distinct=True)
    product_name = filters.CharFilter(method='filter_product_name', required=False)
    category_name = filters.CharFilter(method='filter_cat', required=False)
    class Meta:
        model = Product
        fields = ["id", 'name', 'category']

    def filter_product_name(self,querset,name,value):
        querset = querset.filter(product__name=value)   
        return querset

    def filter_cat(self,querset,name,value):
        querset = querset.filter(category_name__category=value)   
        return querset

@swagger_auto_schema(tags=['Main Service Updated'])
class ProductView(ModelViewSet):
    parser_classes = (MultiPartParser, )
    serializer_class = ProductSerialization
    filter_class = ProductFilter
    filterset_fields = ['id', 'name', 'category']
    pagination_class = CustomPageNumberPagination
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:  # Allow GET request without authentication
            return []
        return super().get_permissions()

    def get_queryset(self):
        return Product.objects.all()