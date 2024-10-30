from datetime import timedelta
import datetime
from django.http import JsonResponse
from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import update_session_auth_hash
from .serializers import ChangePasswordSerializer
from django_gunpermit.settings import SIMPLE_JWT

ACCESS_TOKEN_LIFETIME = SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']

class LoginView(APIView):
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data
            tokens = serializer.get_tokens(user)
            response = Response(serializer.data, status=status.HTTP_200_OK)
            set_refresh_token_in_cookies(response, tokens['refresh'])
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserView(APIView):
    queryset = get_user_model().objects.all()
    authentication_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = serializer.get_tokens(user)

            response_data = {
                'access': tokens['access'],
            }
            response = Response(response_data, status=status.HTTP_200_OK)
            set_refresh_token_in_cookies(response, tokens['refresh'])
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CookieTokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        if not refresh_token:
            return Response({"detail": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            refresh_token = str(token)

            response_data = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'expires_in': datetime.datetime.now() + ACCESS_TOKEN_LIFETIME,
            }

            response = Response(response_data, status=status.HTTP_200_OK)
            set_refresh_token_in_cookies(response, refresh_token)
            return response
        except TokenError:
            response = Response(
                {"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
            delete_refresh_token_from_cookies(response)
            return response


class LogoutView(APIView):
    def delete(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        if refresh_token:
            response = Response(
                {"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
            delete_refresh_token_from_cookies(response)
            RefreshToken(refresh_token)
            return response
        else:
            return Response({"detail": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.CreateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        refresh_token = request.COOKIES.get('refreshToken')
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.data.get('new_password'))
            response = Response(
                {'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            user.save()
            response = logout_user(response, refresh_token)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        refresh_token = request.COOKIES.get('refreshToken')
        user.delete()
        response = Response(
            {'detail': 'Account deleted successfully.'}, status=status.HTTP_200_OK)
        response = logout_user(response, refresh_token)
        return response


def logout_user(response: Response, refresh_token: str):
    print("Logging out", refresh_token)
    delete_refresh_token_from_cookies(response)
    RefreshToken(refresh_token)
    return response


def set_refresh_token_in_cookies(response: Response, refresh_token: str):
    response.set_cookie(
        'refreshToken', refresh_token, httponly=True, samesite='none', secure=True, max_age=timedelta(days=7))
    return response


def delete_refresh_token_from_cookies(response: Response):
    response.set_cookie('refreshToken', samesite='none',
                        httponly=True, secure=True, max_age=0)
    return response
