from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model


User = get_user_model()


@receiver(post_save, sender=User)
def post_user_registration(instance: User, created, **kwargs):
    """
    Create new UserProfile for a new registered user
    Parameters
    ----------
    sender
    instance
    created
    kwargs

    Returns
    -------
    None

    Author: Himanshu Shankar (https://himanshus.com)
    """
    from userprofile.models import UserProfile, CategoryMaster

    # Try to get a default category
    try:
        default_category = CategoryMaster.objects.get(is_default=True)
    except CategoryMaster.DoesNotExist:
        default_category = CategoryMaster.objects.all().first()

    # If no category is present, return
    if not default_category:
        return

    if created:
        UserProfile.objects.create(created_by=instance,
                                   category=default_category)
