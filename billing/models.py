from django.db import models
from django.utils.text import gettext_lazy as _

from drfaddons.models import CreateUpdateModel


class BillHeader(CreateUpdateModel):
    """
    Represents bill header in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from OfficeCafe.variables import BILL_STATUS_CHOICES, PAYMENT_MODE_CHOICES
    from OfficeCafe.variables import UNPAID, ON_COUNTER, PAYMENT_TYPE_CHOICES
    from OfficeCafe.variables import CASH

    from order.models import Order

    order = models.ForeignKey(to=Order, on_delete=models.PROTECT,
                              verbose_name=_("Order"))
    status = models.CharField(verbose_name=_("Status"), max_length=5,
                              choices=BILL_STATUS_CHOICES, default=UNPAID)
    payment_type = models.CharField(verbose_name=_("Payment Type"),
                                    choices=PAYMENT_TYPE_CHOICES,
                                    default=ON_COUNTER, max_length=5)
    payment_mode = models.CharField(verbose_name=_("Payment Mode"),
                                    choices=PAYMENT_MODE_CHOICES,
                                    default=CASH, max_length=5)

    @property
    def grand_total(self):
        total = 0
        for item in self.billitem_set.all():
            total += item.total
        return round(total, 2)

    def __str__(self):
        return "{order}'s payment".format(order=str(self.order))

    class Meta:
        verbose_name = _("Bill Header")
        verbose_name_plural = _("Bill Headers")


class BillItem(CreateUpdateModel):
    """
    Represents bill items

    Author: Himanshu Shankar
    """

    from order.models import SubOrder

    bill = models.ForeignKey(to=BillHeader, on_delete=models.PROTECT,
                             verbose_name=_("Bill"))
    suborder = models.ForeignKey(to=SubOrder, on_delete=models.PROTECT,
                                 verbose_name=_("Sub Order"))
    price = models.DecimalField(verbose_name=_("Price"), max_digits=10,
                                decimal_places=2)

    @property
    def sub_total(self):
        return self.price * self.suborder.quantity

    @property
    def total_tax(self):
        from django.db.models.aggregates import Sum

        return self.billitemtax_set.aggregate(Sum('value'))['value__sum']

    @property
    def total(self):
        return self.sub_total + self.total_tax

    def __str__(self):
        return str(self.suborder)


class BillItemTax(models.Model):
    """
    Represents taxes on bill items

    Author: Himanshu Shankar (https://himanshus.com)
    """
    name = models.CharField(verbose_name=_("Tax Name"), max_length=15)
    value = models.DecimalField(verbose_name=_("Tax Value"), max_digits=10,
                                decimal_places=2)
    item = models.ForeignKey(to=BillItem, on_delete=models.PROTECT,
                             verbose_name=_("Item"))

    def __str__(self):
        return "{name} - {item}".format(name=self.name, item=str(self.item))

    class Meta:
        verbose_name = _("Bill Item Tax")
        verbose_name_plural = _("Bill Item Taxes")
