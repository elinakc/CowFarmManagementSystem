from django.apps import AppConfig


class AnalyticsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.analytics_app'
    
    def ready(self):
        import app.analytics_app.signals 
