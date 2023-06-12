from rest_framework.viewsets import ModelViewSet
from API.serialization.categorySerials import CategorySerialization
from rest_framework.parsers import MultiPartParser
from rest_framework import permissions
from API.models import Category
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from lib.pagination import CustomPageNumberPagination
from knox.auth import TokenAuthentication


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass

class CategoryFilter(filters.FilterSet):
    maincat = NumberInFilter(field_name='id', lookup_expr='in', required=False, distinct=True)
    catname = filters.CharFilter(method='filter_cat_name', required=False)
    maincat_name = filters.CharFilter(method='filter_main_cat', required=False)

    class Meta:
        model = Category
        fields = ["id", 'name', 'maincat']

    def filter_cat_name(self,querset,name,value):
        querset = querset.filter(catname__name=value)   
        return querset

    def filter_main_cat(self,querset,name,value):
        querset = querset.filter(maincat_name__maincat=value)   
        return querset

@swagger_auto_schema(tags=['Main Service Updated'])
class CatgoryView(ModelViewSet):
    parser_classes = (MultiPartParser, )
    serializer_class = CategorySerialization
    filter_class = CategoryFilter
    filterset_fields = ['id', 'name', 'maincat']
    pagination_class = CustomPageNumberPagination
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:  # Allow GET request without authentication
            return []
        return super().get_permissions()

    def get_queryset(self):
        return Category.objects.all()