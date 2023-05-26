from django.db import models
from django.conf import settings

from PIL import Image
from io import BytesIO
from django.core.files import File

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
    
    def image_compression(self, *args, **kwargs):
       if self.image:
            # Open the image using Pillow
            image = Image.open(self.image)
            
            #Resize the image to a maximum size of 1024 x 1024 pixels
            image.thumbnail((1024, 1024))
            
            # Compress the image
            if self.image.name.lower().endswith('.jpg') or self.image.name.lower().endswith('.jpeg'):
                format = 'JPEG'
                # Set the JPEG quality level to 80%
            elif self.image.name.lower().endswith('.png'):
                format = 'PNG'
                # Set the PNG compression level to 6 (out of 9)
                image = image.convert('P', palette=Image.ADAPTIVE, colors=256)
                options = {'compress_level': 6}
            else:
                # Unsupported image format
                super(Product, self).save(*args, **kwargs)
                return
            
            output = BytesIO()
            image.save(output, format=format, optimize=True, quality=80, **options if format == 'PNG' else {})
            new_image = File(output, name=self.image.name)

            # Set the image field to the compressed image
            self.image = new_image

            super(Product, self).save(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        self.image_compression()
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
    

    
    