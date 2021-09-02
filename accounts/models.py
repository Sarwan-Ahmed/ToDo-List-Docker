"""Module to create models for accounts"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status


class UserManager(BaseUserManager):
    """Class to manage user creation"""


    def create_user(self, username, email, password=None):
        """Creates local user"""
        if not email:
            raise ValueError('Users must have an email address')

        if not username:
            raise ValueError('Users must have a username')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, email, password):
        """Creates suoer user"""
        if password is None:
            raise ValueError('Password should not be None')

        user = self.create_user(username = username,
                                email = self.normalize_email(email),
                                password = password)

        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


AUTH_PROVIDERS = {'google':'google', 'facebook':'facebook', 'email':'email'}

class User(AbstractBaseUser, PermissionsMixin):
    """Model to define fields of user"""
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email_verified = models.BooleanField(default=False)
    auth_provider = models.CharField(max_length=255, default=AUTH_PROVIDERS.get('email'))
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_email(self):
        """Returns email of user"""
        return self.email

    def get_id(self):
        """Returns user ID"""
        return self.pk


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(instance=None, created=False, **kwargs):
    """Creates auth token on user creation"""
    if created:
        Token.objects.create(user=instance)



@receiver(reset_password_token_created)
def password_reset_token_created(reset_password_token, *args, **kwargs):
    """Creates password reset token and send to user email to reset password"""
    if reset_password_token.user.auth_provider == 'email':

        email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'),
                                                       reset_password_token.key)

        send_mail(subject="Reset API Password",
            message=email_plaintext_message,
            from_email=None,
            recipient_list=[reset_password_token.user.email])
    else:
        return Response({"password reset error":"password can't be reset for OAuth 2 based users"},
                        status=status.HTTP_403_FORBIDDEN)
