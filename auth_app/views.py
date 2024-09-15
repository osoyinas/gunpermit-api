from datetime import timedelta
import datetime
from django.http import JsonResponse
from rest_framework import generics, permissions
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data
            tokens = serializer.get_tokens(user)

            response = Response(tokens, status=status.HTTP_200_OK)
            set_refresh_token_in_cookies(response, tokens['refresh'])
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserView(APIView):
    queryset = get_user_model().objects.all()

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            tokens = serializer.get_tokens(user)
            response = Response(tokens, status=status.HTTP_200_OK)
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
            new_access_token = str(token.access_token)
            new_refresh_token = str(token)

            response_data = {
                'access': new_access_token,
                'refresh': new_refresh_token
            }

            response = Response(response_data, status=status.HTTP_200_OK)
            set_refresh_token_in_cookies(response, new_refresh_token)
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


class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


def set_refresh_token_in_cookies(response: Response, refresh_token: str):
    response.set_cookie(
        'refreshToken', refresh_token, httponly=True, samesite='none', secure=True, max_age=timedelta(days=7))
    return response


def delete_refresh_token_from_cookies(response: Response):
    response.set_cookie('refreshToken', samesite='none', httponly=True, secure=True, max_age=0)
    return response
