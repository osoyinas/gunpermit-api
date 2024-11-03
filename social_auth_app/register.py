import random
from rest_framework.exceptions import AuthenticationFailed

from decouple import config
from django.contrib.auth import get_user_model


User = get_user_model()


def generate_username(name):

    username = "".join(name.split(" ")).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name, first_name='', last_name=''):
    user = User.objects.filter(email=email).first()

    if user is not None:

        if provider == user.auth_provider:
            return user

        else:
            raise AuthenticationFailed(
                detail=f"Por favor, incia sesion con {user.auth_provider} en lugar de {provider}. Correo: {email}")

    else:
        user = {
            "username": generate_username(name),
            "email": email,
            "password": config("SOCIAL_SECRET"),
        }
        user = User.objects.create_user(**user)
        # user.is_verified = True
        user.auth_provider = provider
        user.save()
        return user
