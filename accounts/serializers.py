"""Module to define serializers for accounts models"""
from rest_framework import serializers
from .models import User



class UserSerializer(serializers.ModelSerializer):
    """Serialize user data"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'email_verified')



class RegisterSerializer(serializers.ModelSerializer):
    """Serialize user register data"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


    def validate(self, attrs):
        """Validate user data while registering"""
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('Username can only contain alphanumeric charachters')
        return attrs


    def create(self, validated_data):
        """Create user after data validation"""
        return User.objects.create_user(**validated_data)



class ResendLinkSerializer(serializers.ModelSerializer):
    """Serislize resend link data"""
    class Meta:
        model = User
        fields = ['email']
