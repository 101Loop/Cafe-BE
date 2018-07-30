from django.db.models.signals import post_save
from django.dispatch import receiver
from drf_user.models import User


@receiver(post_save, sender=User)
def send_welcome_mail(instance, created, **kwargs):
    from drfaddons.add_ons import send_message
    from django.conf import settings
    user_settings = getattr(settings, 'USER_SETTINGS')

    message = "Welcome to Office Cafe %s. Your account has been created with %s mobile & %s email." % (instance.name,
                                                                                                       instance.mobile,
                                                                                                       instance.email)

    if created:
        if user_settings['REGISTRATION']['SEND_MAIL']:
            send_message(message, user_settings['REGISTRATION']['MAIL_SUBJECT'], [instance.email], [instance.email])
        if user_settings['REGISTRATION']['SEND_SMS']:
            send_message(message, user_settings['REGISTRATION']['SMS_BODY'], [instance.mobile], [instance.email])
    else:
        # TODO: Send update
        print(kwargs)
