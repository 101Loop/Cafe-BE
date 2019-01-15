from django.apps import AppConfig


class UserprofileConfig(AppConfig):
    name = 'userprofile'
    verbose_name = "User Profile"

    def ready(self):
        from .signals.handlers import post_user_registration

        super(UserprofileConfig, self).ready()
