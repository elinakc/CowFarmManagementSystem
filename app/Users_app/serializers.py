from rest_framework import serializers
# from rest_framework.response import Response
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework import serializers
import re

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    roles = serializers.CharField(required=False, default='manager')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password', 'phone_number', 'address', 'roles']
        extra_kwargs = {
            'phone_number': {'required': False},
            'address': {'required': False},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Password does not match"})
        return data 

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            roles=validated_data.get('roles', 'manager'),
            phone_number=validated_data.get('phone_number', ''),
            address=validated_data.get('address', ''),
        )
        return user
    # def validate_email(self, value):
    #     # Define the regex pattern
    #     pattern = r'^[a-zA-Z]+(?:[a-zA-Z]*manager|[a-zA-Z]*admin|[a-zA-Z]*vet)?@gmail\.com$'
    #     if not re.match(pattern, value):
    #         raise serializers.ValidationError("Please enter a valid email address.")
    #     return value
    


class loginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Authenticate the user
        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid login credentials")

        # Add the user to the validated data
        data['user'] = user
        return data
    

    
    