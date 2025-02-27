from django.db import models


# Create your models here.
class users(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=12)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
