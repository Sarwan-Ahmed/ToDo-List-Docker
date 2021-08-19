import random
from django.contrib.auth import authenticate
from accounts.models import User
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from rest_framework.authtoken.models import Token


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(email=email, password=settings.GOOGLE_CLIENT_SECRET)
            token, created = Token.objects.get_or_create(user=registered_user)
            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'token': token.key}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'username': generate_username(name), 'email': email,
            'password': settings.GOOGLE_CLIENT_SECRET}
        user = User.objects.create_user(**user)
        user.email_verified = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(email=email, password=settings.GOOGLE_CLIENT_SECRET)
        token, created = Token.objects.get_or_create(user=new_user)
        return {
            'email': new_user.email,
            'username': new_user.username,
            'token': token.key
        }