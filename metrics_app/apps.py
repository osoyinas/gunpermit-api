from django.apps import AppConfig


class MetricsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'metrics_app'

    def ready(self):
        import metrics_app.signals
