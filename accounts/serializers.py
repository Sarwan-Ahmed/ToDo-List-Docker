from rest_framework import serializers
from .models import User


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'email_verified')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('Username can only contain alphanumeric charachters')
        return attrs


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


#Resend Verification Link serializer
class ResendLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']
