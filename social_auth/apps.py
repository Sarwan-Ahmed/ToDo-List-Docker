"""Module to configure social auth apps"""
from django.apps import AppConfig


class SocialAuthConfig(AppConfig):
    """Configuration of social auth"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social_auth'
