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
