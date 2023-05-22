from django.db import models
from django.conf import settings

from django.utils.text import slugify

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=250,  unique=True)
    slug = models.SlugField(unique=True, editable=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products', blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, editable=False)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        

#model for wishlist
class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} wishlist, item : {self.product.name}"
    

    
    