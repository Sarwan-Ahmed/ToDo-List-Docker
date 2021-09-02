"""Module to define serializers for social auth"""
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from . import google
from .register import register_social_user


class GoogleSocialAuthSerializer(serializers.Serializer):
    """Serialize social auth Google data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        """validate auth token and serialize the data"""
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed('Authetication Failed')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(provider=provider, user_id=user_id, email=email, name=name)
