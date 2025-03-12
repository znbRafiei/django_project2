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

class Booking(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE)  
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  
    date = models.DateField() 
    time_slot = models.CharField(max_length=20)  
    status = models.CharField(max_length=20, default='pending') 
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Booking: {self.user.email} with {self.doctor.name} on {self.date} at {self.time_slot}"