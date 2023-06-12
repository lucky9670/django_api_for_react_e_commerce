from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Registration(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    """
        Inherits from default User of Django and extends the fields.
        The following fields are part of Django User Model:
        | id
        | password
        | last_login
        | is_superuser
        | username
        | first_name
        | last_name
        | email
        | is_staff
        | is_active
        | date_joined
        """
    name=models.CharField(max_length=100,null=True,blank=True)
    mobile_number = models.CharField(max_length=20, null=True,blank=True)
    date_of_birth = models.DateField(max_length=8,null=True,blank=True)
    email = models.EmailField(unique=True, null=False, db_index=True, error_messages={
        'unique': "Email already exists"
    })
  
    def __str__(self):
        return self.email

class MainCat(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="maincat/")
    description = models.CharField(max_length=500, null=False, blank=False)

class Category(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='category/')
    descciption = models.CharField(max_length=500, null=False, blank=False)
    maincat = models.ForeignKey(MainCat, related_name="category", on_delete=models.CASCADE)

class Product(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to="product/")
    description = models.TextField()
    price = models.CharField(max_length=50)
    product_slug = models.SlugField()
    category = models.ForeignKey(Category, related_name="product", on_delete=models.CASCADE)