from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from transaction.models import OrderPayment


User = get_user_model()


@receiver(post_save, sender=OrderPayment)
def add_points(instance: OrderPayment, created, **kwargs):
    """
    Adds point in the user's wallet as per payment and user's category

    Parameters
    ----------
    instance: OrderPayment
    created: bool
    kwargs: dict

    Returns
    -------

    """
    from currency.models import OCPointTransaction
    from userprofile.models import UserProfile

    # Check if it's a newly created item
    if created:
        up = UserProfile.objects.get(created_by_id=instance.created_by.id)

        value = up.category.point
        if up.category.is_percentage:
            value = value * instance.amount / 100

        OCPointTransaction.objects.create(created_by=instance.created_by,
                                          is_credit=instance.is_credit,
                                          value=value, payment=instance)


@receiver(post_save, sender=User)
def post_user_registration(instance: User, created, **kwargs):
    """
    Create new OCPoint Wallet for a new registered user
    Parameters
    ----------
    instance: User
    created: bool
    kwargs: dict

    Returns
    -------
    None

    Author: Himanshu Shankar (https://himanshus.com)
    """
    from currency.models import OCPointWallet

    if created:
        OCPointWallet.objects.create(created_by=instance)
