from rest_framework.viewsets import ModelViewSet
from API.serialization.maincatserials import MainCatSerialization
from rest_framework.parsers import MultiPartParser
from rest_framework import permissions
from API.models import MainCat
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from lib.pagination import CustomPageNumberPagination
from knox.auth import TokenAuthentication


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass

class MaincatFilter(filters.FilterSet):
    maincat = NumberInFilter(field_name='id', lookup_expr='in', required=False, distinct=True)
    maincat_name = filters.CharFilter(method='filter_ser_name', required=False)

    class Meta:
        model = MainCat
        fields = ["id", 'name']

    def filter_ser_name(self,querset,name,value):
        querset = querset.filter(maincat_name__name=value)   
        return querset

@swagger_auto_schema(tags=['Main Service Updated'])
class MainCatView(ModelViewSet):
    parser_classes = (MultiPartParser, )
    serializer_class = MainCatSerialization
    filter_class = MaincatFilter
    filterset_fields = ['id', 'name']
    pagination_class = CustomPageNumberPagination
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:  # Allow GET request without authentication
            return []
        return super().get_permissions()

    def get_queryset(self):
        return MainCat.objects.all()