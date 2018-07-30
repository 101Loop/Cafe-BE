from django.db import models
from django.utils.text import gettext_lazy as _

from drfaddons.models import CreateUpdateModel


class BillingHeader(CreateUpdateModel):
    from restaurant.models import Store

    # def number(self):
    #     no = BillingHeader.objects.count()
    #     if no == None:
    #         return 10000
    #     else:
    #         return no + 1

    bill_date = models.DateTimeField(_('Bill Date'))
    due_date = models.DateField(_('Due Date'))
    name = models.CharField(_('Full Name'), max_length=500, null=True, blank=True)
    mobile = models.CharField(_('Mobile Number'), max_length=15, null=True, blank=True)
    email = models.EmailField(_('Email ID'), null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    # TODO: auto generate these two on the basis of regex/pattern
    order_no = models.CharField(_('Order Number'), max_length=20)
    bill_no = models.CharField(_('Bill Number'), max_length=20)

    @property
    def subtotal(self):
        sum = 0
        items = self.billitem_set.all()
        for item in items:
            sum += item.subtotal_price
        return sum

    @property
    def total(self):
        sum = 0
        items = self.billitem_set.all()
        for item in items:
            sum += item.total_price
        return sum

    @property
    def gst(self):
        return self.total - self.subtotal

    def __str__(self):
        return str(self.bill_no) + ' | ' + str(self.order_no)

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
        return self.item.subtotal*self.quantity
    
    @property
    def total_price(self):
        return self.item.total*self.quantity

    def __str__(self):
        return str(self.billheader) + ' | ' + str(self.item)

    class Meta:
        verbose_name = _('Bill Item')
        verbose_name_plural = _('Bill Items')
