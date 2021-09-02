"""Module to define urls for social auth"""
from django.urls import path
from .views import GoogleSocialAuthView


urlpatterns = [
	path('google/', GoogleSocialAuthView.as_view(), name='auth-google'),
]
