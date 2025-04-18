from django.apps import AppConfig


class MetricsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'metrics_app'
    verbose_name = 'Métricas de usuarios'

    def ready(self):
        import metrics_app.signals
