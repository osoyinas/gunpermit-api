from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


def createUserMock(
        username: str = 'test',
        email: str = 'test@gmail.com',
        password: str = 'test'):
    return get_user_model().objects.create_user(
        username=username,
        email=email,
        password=password)

def createUserStaffMock(
        username: str = 'test',
        email: str = 'test@gmail.com',
        password: str = 'test'):
    return get_user_model().objects.create_user(
        username=username,
        email=email,
        password=password,
        is_staff=True)


def getAuthenticatedClient(user):
    if not user:
        user = createUserMock()

    client = APIClient(format='json')
    token = RefreshToken.for_user(user)
    client.credentials(
        HTTP_AUTHORIZATION='Bearer ' + str(token.access_token))
    return client


def getClient():
    return APIClient()
