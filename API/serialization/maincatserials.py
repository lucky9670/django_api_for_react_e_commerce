from rest_framework import serializers
from API.models import MainCat

class MainCatSerialization(serializers.ModelSerializer):
    name = serializers.CharField(required=True, allow_blank=False)
    image = serializers.ImageField()
    description = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = MainCat
        fields = ('id', 'name', 'image', 'description')