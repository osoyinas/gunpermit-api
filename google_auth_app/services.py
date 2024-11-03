import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from typing import Dict, Any
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


def google_get_access_token(code: str, redirect_uri: str) -> str:
    data = {
        'code': code,
        'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
        'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    response = requests.post(settings.GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

    if not response.ok:
        raise ValidationError('Failed to obtain access token from Google.')

    access_token = response.json()['access_token']
    return access_token

def google_get_user_info(access_token: str) -> Dict[str, Any]:
    response = requests.get(
        settings.GOOGLE_USER_INFO_URL,
        params={'access_token': access_token}
    )

    if not response.ok:
        raise ValidationError('Failed to obtain user info from Google.')

    return response.json()


def create_or_get_user(user_data: Dict[str, Any]) -> Dict:
    User = get_user_model()

    user, created = User.objects.get_or_create(
        email=user_data['email'],
        defaults={
            'email': user_data['email'],
            'username': user_data['email'],
            'first_name': user_data.get('given_name', ''),
            'last_name': user_data.get('family_name', '')
        }
    )

    return user