from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import LoginView, RegisterUserView, CurrentUserView, LogoutView, CookieTokenRefreshView

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth_login'),
    path('register/', RegisterUserView.as_view(), name='auth_register'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('refresh-token/', CookieTokenRefreshView.as_view(), name='auth_token_refresh'),
    path('me/', CurrentUserView.as_view(), name='me'),
]
