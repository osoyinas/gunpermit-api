from django.apps import AppConfig


class TrackingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracking_app'
    def ready(self):
        import tracking_app.signals  # Importa las signals para que se registren