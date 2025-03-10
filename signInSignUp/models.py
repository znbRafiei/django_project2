from django.db import models


# Create your models here.
class users(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=12)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.email


class Doctor(models.Model):
    user = models.ForeignKey("users", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    available_slots = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
