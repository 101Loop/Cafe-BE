from django.apps import AppConfig


class BillingConfig(AppConfig):
    name = 'billing'

    class Meta:
        verbose_name = 'Billing'

    def ready(self):
        from .signals import handlers
