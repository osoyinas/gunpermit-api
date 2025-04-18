from django.apps import AppConfig


class SocialAuthAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social_auth_app'
    verbose_name='Autencicación con terceros'