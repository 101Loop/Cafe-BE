from django.db import models
from django.utils.text import gettext_lazy as _

from drfaddons.models import CreateUpdateModel


class Discount(CreateUpdateModel):
    """
    Represents possible discounts

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from product.models import Product, Category

    name = models.CharField(verbose_name=_("Discount Name"), max_length=254,
                            unique=True)
    value = models.DecimalField(verbose_name=_("Discount Value"),
                                max_digits=10, decimal_places=2)
    is_percentage = models.BooleanField(verbose_name=_("Is Percentage?"),
                                        default=True)

    max_discount = models.DecimalField(verbose_name=_("Max Discount Value"),
                                       max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField(verbose_name=_("Min Order Amount"),
                                           max_digits=10, decimal_places=2,
                                           default=0.00)

    per_user_limit = models.IntegerField(verbose_name=_("Per user limit"),
                                         default=0)
    per_user_value_limit = models.DecimalField(
        verbose_name=_("Per User Limit (Value)"), decimal_places=2,
        max_digits=10, default=0.00)

    total_count = models.IntegerField(verbose_name=_("Total Limit"), default=0)
    total_value_limit = models.DecimalField(verbose_name=_("Net Value Limit"),
                                            max_digits=10, decimal_places=2,
                                            default=0.00)

    from_date = models.DateField(verbose_name=_("Valid From (Date)"),
                                 null=True, blank=True)
    to_date = models.DateField(verbose_name=_("Valid Till (Date)"),
                               null=True, blank=True)
    from_time = models.TimeField(verbose_name=_("Valid From (Time)"),
                                 null=True, blank=True)
    to_time = models.TimeField(verbose_name=_("Valid Till (Time)"),
                               null=True, blank=True)

    valid_on_categories = models.ManyToManyField(to=Category, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")


class OCPointWallet(CreateUpdateModel):
    """
    Represents wallet of user's that maintains OC's point earned

    Author: Himanshu Shankar (https://himanshus.com)
    """
    from django.contrib.auth import get_user_model

    created_by = models.OneToOneField(verbose_name=_("User"),
                                      to=get_user_model(),
                                      on_delete=models.PROTECT)
    points = models.DecimalField(verbose_name=_("Points"), max_digits=10,
                                 decimal_places=3, default=0)

    def __str__(self):
        return self.created_by.name

    class Meta:
        verbose_name = _("Point")
        verbose_name_plural = _("Points")


class OCPointTransaction(CreateUpdateModel):
    """
    Represents wallet transaction of user

    Author: Himanshu Shankar (https://himanshus.com)
    """
    from transaction.models import OrderPayment

    payment = models.ForeignKey(to=OrderPayment, on_delete=models.PROTECT,
                                verbose_name=_("Order Payment"), null=True,
                                blank=True)

    value = models.DecimalField(verbose_name=_("Value"), max_digits=10,
                                decimal_places=3, default=0)
    is_credit = models.BooleanField(verbose_name=_("Is Credit?"),
                                    default=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        # Check if new transaction is being created and maintain a flag
        new = False
        if self.pk is None:
            new = True

        super(OCPointTransaction, self).save(force_insert=force_insert,
                                             force_update=force_update,
                                             using=using,
                                             update_fields=update_fields
                                             )

        # If a new transaction is being created, update the Wallet
        if new:
            try:
                ocw = OCPointWallet.objects.get(created_by=self.created_by)
            except OCPointWallet.DoesNotExist:
                ocw = OCPointWallet.objects.create(created_by=self.created_by)

            if self.is_credit:
                ocw.points += self.value
            else:
                ocw.points -= self.value
            ocw.save()

    def __str__(self):
        return self.created_by.name

    class Meta:
        verbose_name = _("Point Transaction")
        verbose_name_plural = _("Point Transactions")
