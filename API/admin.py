from django.contrib import admin
from .models import Registration, MainCat, Category, Product
# Register your models here.

admin.site.register(Registration)
admin.site.register(MainCat)
admin.site.register(Category)
admin.site.register(Product)
