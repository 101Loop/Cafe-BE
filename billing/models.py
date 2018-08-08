from django.db import models
from django.utils.text import gettext_lazy as _

from drfaddons.models import CreateUpdateModel

#
# def number():
#     """
#     A function to create the order number.
#     """
#     no = BillingHeader.objects.count()
#     if no == None:
#         return 10000
#     else:
#         return no + 1


class BillingHeader(CreateUpdateModel):
    """
    A custom BillingHeader model that includes the details of a bill.
    """
    from restaurant.models import Store
    from django.core.validators import RegexValidator

    bill_date = models.DateTimeField(_('Bill Date'))
    due_date = models.DateField(_('Due Date'))

    payment_mode = models.CharField(_('Mode of Payment'), choices=[('C', 'Cash'), ('I', 'Instamojo')], default='I',
                                    max_length=3)
    payment_id = models.TextField(_('Payment ID'), null=True, blank=True)
    payment_done = models.BooleanField(_('Payment Done?'), default=False)

    name = models.CharField(_('Full Name'), max_length=500, null=True, blank=True)
    mobile = models.CharField(_('Mobile Number'), max_length=15, null=True, blank=True)
    email = models.EmailField(_('Email ID'), null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    # TODO: auto generate these two on the basis of regex/pattern
    order_no = models.CharField(_('Order Number'), max_length=20) # default=number)
    bill_no = models.CharField(_('Bill Number'), max_length=20) # validators=[RegexValidator(regex='^[a-zA-Z0-9]*$')])

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


class InstamojoDetails(models.Model):
    """
    A InstamojoDetails model that includes the details of the payment made by the client.
    """
    amount = models.DecimalField(_('Amount'), decimal_places=2, max_digits=10)
    purpose = models.CharField(_('Purpose'), max_length=254)
    redirect_url = models.URLField(_('Redirect URL'))
    allow_repeated_payments = models.BooleanField(_('Allow Repeated Payment'), default=False)

    payment_id = models.CharField(_('Payment ID'), max_length=254, null=True, blank=True)
    payment_raw = models.TextField(_('Payment Raw Response'), null=True, blank=True)
    status = models.CharField(_('Status'), max_length=10)

    payment_request_id = models.TextField(_('Payment Request ID'), null=True, blank=True)
    payment_request_raw = models.TextField(_('Payment Request Raw Response'), null=True, blank=True)
    expires_at = models.CharField(_('Expires at'), max_length=30, blank=True, null=True)

    bill = models.ForeignKey(BillingHeader, null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('Instamojo Detail')
        verbose_name_plural = _('Instamojo Details')
