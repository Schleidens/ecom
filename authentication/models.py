from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    address = models.CharField(max_length=50)
    shipping_address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)