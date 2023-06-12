from API.models import Category
from rest_framework import serializers

class CategorySerialization(serializers.ModelSerializer):
    description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'image','description', 'maincat')