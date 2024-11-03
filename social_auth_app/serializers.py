from rest_framework import serializers

from django_gunpermit.settings import GOOGLE_OAUTH2_CLIENT_ID
from . import google
from .register import register_social_user
import os
from rest_framework.exceptions import AuthenticationFailed
from auth_app.serializers import LoggedUserSerializer


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        print(user_data)
        try:
            user_data['sub']  # sub is the unique id of the google user
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != GOOGLE_OAUTH2_CLIENT_ID:  # aud is the audience of the token

            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        try:
            first_name = user_data['given_name']
            last_name = user_data['family_name']
        except KeyError:
            first_name = name
            last_name = ''
        provider = 'google'

        user = register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)

        return LoggedUserSerializer(user).data
