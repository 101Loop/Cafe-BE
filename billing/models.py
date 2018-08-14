from django.db import models
from django.utils.text import gettext_lazy as _

from drfaddons.models import CreateUpdateModel


# TODO: Multiple payment adapters such as Instamojo
class BillingHeader(CreateUpdateModel):
    """
    A custom BillingHeader model that includes the details of a bill.
    """
    from restaurant.models import Store

    bill_date = models.DateTimeField(_('Bill Date'), auto_created=True)
    due_date = models.DateField(_('Due Date'))

    payment_mode = models.CharField(_('Mode of Payment'), choices=[('C', 'Cash'), ('I', 'Instamojo')], default='I',
                                    max_length=3)
    paid = models.BooleanField(_('Bill Paid'), default=False)

    name = models.CharField(_('Full Name'), max_length=500)
    mobile = models.CharField(_('Mobile Number'), max_length=15)
    email = models.EmailField(_('Email ID'))

    order_mode = models.CharField(_('Order Mode'), choices=[('R', 'Dine In'), ('P', 'Pick Up'), ('D', 'Delivery')],
                                  max_length=3, default='R')
    address = models.TextField(_('Address'), null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)

    @property
    def payment_id(self):
        pay_id = None
        if self.paid:
            if self.payment_mode == 'I':
                pay_id = self.paymentrequest.id
            else:
                pay_id = 'CASH' + str(self.id)
        return pay_id

    @property
    def subtotal(self):
        sum = 0
        items = self.billitem_set.all()
        for item in items:
            sum += item.subtotal_price
        s = round(sum, 2)
        return s

    @property
    def total(self):
        sum = 0
        items = self.billitem_set.all()
        for item in items:
            sum += item.total_price
        s = round(sum, 2)
        return s

    @property
    def gst(self):
        gst_value = round((self.total - self.subtotal), 2)
        return gst_value

    def __str__(self):
        return str(self.id) + ' | ' + str(self.name)

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
