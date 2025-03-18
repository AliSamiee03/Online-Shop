from rest_framework import serializers
from .models import CustomUser, Address, Staff, Role

class UserSerialzer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone', 'email', 'username', 'password']

    def validate(self, data):
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("This username has already been used.")
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("This email has already been registered.")
        return data


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class StaffSerializer(serialzers.ModelSerializer):
    class Meta:
        model= Staff
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

