from django.apps import AppConfig
from . import update_user_settings


class DRFUserConfig(AppConfig):
    name = 'drf_user'
    verbose_name = "Django REST Framework - User"

    update_user_settings()

    def ready(self):
        from .signals import handlers
