from django.db import models

from django.conf import settings

from store.models import Product

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username.capitalize()} Cart "
    
    
class CartItem(models.Model):
    cart =  models.ForeignKey(Cart, on_delete=models.CASCADE)
    product =  models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.cart} - {self.product}"
    
    def get_total_price(self):
        total = self.product.price * self.quantity
        
        return total
