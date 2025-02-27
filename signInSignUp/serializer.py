from rest_framework import serializers
from .models import users

class userSerialzer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ['email','password']
