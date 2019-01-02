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
    from OfficeCafe.variables import DELIVERY_TYPE_CHOICES, PICKED_UP

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
                                   to=OutletManager, on_delete=models.PROTECT,
                                   null=True, blank=True)

    delivery_type = models.CharField(verbose_name=_("Delivery Type"),
                                     choices=DELIVERY_TYPE_CHOICES,
                                     max_length=5, default=PICKED_UP)

    @property
    def payment_done(self)->bool:
        from django.db.models.aggregates import Sum

        payments = self.orderpayment_set.filter(is_credit=True).aggregate(
            Sum('amount'))['amount__sum']
        if payments:
            return payments == self.total
        else:
            return self.total == 0

    @property
    def total(self):
        total = 0

        for so in self.suborder_set.all():
            total += so.sub_total
        return round(total, 2)

    def __str__(self)->str:
        if self.name:
            return self.name
        elif self.id:
            return str(self.id)
        else:
            return "{status} Order".format(status=self.get_status_display())

    class Meta:
        ordering = ['-create_date', ]
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class SubOrder(CreateUpdateModel):
    """
    Represents sub orders in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from product.models import Product

    order = models.ForeignKey(verbose_name=_("Order"), to=Order,
                              on_delete=models.PROTECT)
    item = models.ForeignKey(verbose_name=_("Product"), to=Product,
                             on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"))

    @property
    def product(self):
        return self.order.outlet.outletproduct_set.get(product=self.item)

    @property
    def sub_total(self):
        op = self.order.outlet.outletproduct_set.get(product=self.item)
        return self.quantity * op.mrp

    def __str__(self):
        return self.item.name

    class Meta:
        verbose_name = _("Sub Order")
        verbose_name_plural = _("Sub Orders")


class Delivery(CreateUpdateModel):
    """
    Represents deliveries happening in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from location.models import Area, BuildingComplex

    order = models.OneToOneField(to=Order, on_delete=models.PROTECT,
                                 verbose_name=_("Order"))
    amount = models.DecimalField(verbose_name=_("Delivery Amount"),
                                 default=0, max_digits=10, decimal_places=3)

    area = models.ForeignKey(to=Area, on_delete=models.PROTECT,
                             verbose_name=_("Area"))
    build = models.ForeignKey(to=BuildingComplex, on_delete=models.PROTECT,
                              verbose_name=_("Building Complex"), null=True,
                              blank=True)
    unit_no = models.CharField(verbose_name=_("Unit Number / Floor"),
                               max_length=100)
    address_line2 = models.CharField(verbose_name=_("Address Line 2"),
                                     max_length=200, null=True, blank=True)

    @property
    def full_address(self):
        address = str(self.unit_no)
        if self.build:
            address += ", {}".format(self.build.name)
        address += ", {}".format(self.area.name)
        address += ", {}".format(self.area.city.name)
        address += ", {}".format(self.area.city.state.name)
        address += ", {}".format(self.area.city.state.country.name)
        address += " - {}".format(self.area.pincode)
        return address

    def __str__(self):
        return self.order.name

    class Meta:
        verbose_name = _("Delivery")
        verbose_name_plural = _("Deliveries")
