from django.apps import AppConfig

class RatingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Ratings'

    def ready(self):
        import Ratings.signals
