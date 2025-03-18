from rest_framework import serializers
from .models import CustomUser

class UserSerialzer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone', 'email', 'username', 'password']


