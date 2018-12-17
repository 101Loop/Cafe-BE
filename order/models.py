from django.db import models
from django.utils.text import gettext_lazy as _

from drfaddons.models import CreateUpdateModel


class Order(CreateUpdateModel):
    """
    Represents order in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """
    import datetime

    from OfficeCafe.variables import STATUS_CHOICES, NEW

    from outlet.models import Outlet, OutletManager

    name = models.CharField(verbose_name=_("Buyer Name"), max_length=254,
                            null=True, blank=True)
    mobile = models.CharField(verbose_name=_("Mobile"), max_length=15,
                              null=True, blank=True)
    email = models.EmailField(verbose_name=_("Email"), null=True, blank=True)
    outlet = models.ForeignKey(verbose_name=_("Outlet"), to=Outlet,
                               on_delete=models.PROTECT)
    preparation_time = models.DurationField(
        verbose_name=_("Preparation Time"),
        default=datetime.timedelta(minutes=10))

    status = models.CharField(verbose_name=_("Order Status"), max_length=5,
                              choices=STATUS_CHOICES, default=NEW)
    managed_by = models.ForeignKey(verbose_name=_("Outlet Manager"),
                                   to=OutletManager, on_delete=models.PROTECT)

    def __str__(self)->str:
        if self.name:
            return self.name
        elif self.id:
            return str(self.id)
        else:
            return f"{self.get_status_display()} Order"

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class SubOrder(CreateUpdateModel):
    """
    Represents sub orders in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from OfficeCafe.variables import UOM_CHOICES, PLATE

    from product.models import Product

    order = models.ForeignKey(verbose_name=_("Order"), to=Order,
                              on_delete=models.PROTECT)
    item = models.ForeignKey(verbose_name=_("Product"), to=Product,
                             on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"))
    uom = models.CharField(verbose_name=_("Unit of Measurement"),
                           max_length=15, choices=UOM_CHOICES, default=PLATE)

    def __str__(self):
        return self.item.name

    class Meta:
        verbose_name = _("Sub Order")
        verbose_name_plural = _("Sub Orders")
