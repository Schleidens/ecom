from django.db import models
from django.conf import settings

# Create your models here.


class Summary(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    
    def __str__(self):
        return f"{self.customer.username.capitalize()} {self.amount}$ purchase "
    
    