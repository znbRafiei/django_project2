from rest_framework import serializers
from .models import users,Doctor

class userSerialzer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ['email','password']
        

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialty', 'available_slots', 'created_at', 'updated_at','user_id']
