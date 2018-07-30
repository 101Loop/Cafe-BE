from django.apps import AppConfig


class BillingConfig(AppConfig):
    name = 'billing'
    verbose_name = 'Billing'

    def ready(self):
        from .signals import handlers
