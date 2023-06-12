from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import RegistrionView, index, LoginAPI, Logout, ChangePasswordView
from API.viewsets.maincatview import MainCatView
from API.viewsets.categoryView import CatgoryView
from API.viewsets.productView import ProductView
from rest_framework import routers

schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="API'S",

   ),
   public=True,
)

main_cat_router = routers.DefaultRouter()
main_cat_router.register(r'^maincat', MainCatView, basename='maincat')

cat_router = routers.DefaultRouter()
cat_router.register(r'^category', CatgoryView, basename='maincat')

product_router = routers.DefaultRouter()
product_router.register(r'^product', ProductView, basename='maincat')

urlpatterns = [
   path('', index, name="index"),
   re_path(r'^api/product_mcat/', include(main_cat_router.urls)),
   re_path(r'^api/product_cat/', include(cat_router.urls)),
   re_path(r'^api/main_product/', include(product_router.urls)),

   path('api/swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('api/redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('api/account/register', RegistrionView.as_view(), name='register'),
   path('api/account/login', LoginAPI.as_view(), name='login'),
   path('api/account/logout', Logout.as_view(), name='logout'),
   path('api/account/change_password', ChangePasswordView.as_view(), name='change_password'),
] 