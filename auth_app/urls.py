from django.urls import path
from .views import ChangePasswordView, LoginView, RegisterUserView, CurrentUserView, LogoutView, DeleteAccountView, CookieTokenRefreshView
from django.urls import path, include

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth_login'),
    path('register/', RegisterUserView.as_view(), name='auth_register'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('refresh-token/', CookieTokenRefreshView.as_view(),
         name='auth_token_refresh'),
    path('me/', CurrentUserView.as_view(), name='me'),
    path('me/delete/', DeleteAccountView.as_view(), name='change_password'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('password-reset/', include('django_rest_passwordreset.urls',
         namespace='password_reset')),
]
