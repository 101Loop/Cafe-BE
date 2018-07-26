from django.db import models
from django.utils.text import gettext_lazy as _

from drfaddons.models import CreateUpdateModel


class BillingHeader(CreateUpdateModel):
    from restaurant.models import Store

    bill_date = models.DateTimeField(_('Bill Date'))
    due_date = models.DateField(_('Due Date'))
    name = models.CharField(_('Full Name'), max_length=500, null=True)
    mobile = models.CharField(_('Mobile Number'), max_length=15, null=True)
    email = models.EmailField(_('Email ID'), null=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    # TODO: auto generate these two on the basis of regex/pattern
    order_no = models.CharField(_('Order Number'), max_length=20)
    bill_no = models.CharField(_('Bill Number'), max_length=20)

    @property
    def subtotal(self):
        items = self.billitem.all()
        if len(items) > 0:
            from django.db.models import Sum

            return items.aggregate(Sum('subtotal_price'))
        else:
            return 0

    @property
    def total(self):
        items = self.billitem.all()
        if len(items) > 0:
            from django.db.models import Sum

            return items.aggregate(Sum('total_price'))
        else:
            return 0

    @property
    def gst(self):
        return self.total - self.subtotal

    def __str__(self):
        return 'Bill No - ' + str(self.bill_no) + 'And Order No - ' + str(self.order_no)

    class Meta:
        verbose_name = _('Billing Header')
        verbose_name_plural = _('Billing Headers')


class BillItem(models.Model):
    from restaurant.models import Item

    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.IntegerField(_('Quantity'))
    billheader = models.ForeignKey(BillingHeader, on_delete=models.PROTECT)

    @property
    def subtotal_price(self):
        return self.item.item_price*self.quantity
    
    @property
    def total_price(self):
        return self.item.total_price*self.quantity

    def __str__(self):
        return self.item

    class Meta:
        verbose_name = _('Bill Item')
        verbose_name_plural = _('Bill Items')
