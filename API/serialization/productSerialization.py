from rest_framework import serializers
from API.models import Product

class ProductSerialization(serializers.ModelSerializer):
    description = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'image', 'description', 'price', 'product_slug', 'category')