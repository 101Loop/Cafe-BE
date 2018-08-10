from django.db import models
from django.utils.text import gettext_lazy as _


class PaymentRequest(models.Model):
    from billing.models import BillingHeader

    id = models.CharField(_('Payment Request ID'), max_length=254, primary_key=True)
    amount = models.DecimalField(_('Amount'), decimal_places=2, max_digits=10)
    purpose = models.CharField(_('Purpose'), max_length=254)
    redirect_url = models.URLField(_('Redirect URL'))
    allow_repeated_payments = models.BooleanField(_('Allow Repeated Payment'), default=False)
    instamojo_raw_response = models.TextField(_('Payment Request Raw Response'), null=True, blank=True)
    longurl = models.URLField(_('Long URL'))
    expires_at = models.CharField(_('Expires at'), max_length=30, blank=True, null=True)
    status = models.CharField(_('Status'), max_length=10)

    bill = models.OneToOneField(BillingHeader, on_delete=models.PROTECT)

    @property
    def paid(self):
        payments = self.payment_set.all().filter(status='C')
        if len(payments) > 0:
            return True
        return False

    @property
    def payment_id(self):
        if self.paid:
            return self.payment_set.get(status='C').id
        return None


class Payment(models.Model):
    """
    A InstamojoDetails model that includes the details of the payment made by the client.
    """
    id = models.CharField(_('Payment ID'), max_length=254, primary_key=True)
    instamojo_raw_response = models.TextField(_('Payment Raw Response'), null=True, blank=True)
    payment_request = models.ForeignKey(PaymentRequest, on_delete=models.PROTECT)
    mac = models.CharField(_('Message Authentication Code'), null=True, blank=True, max_length=154)
    status = models.CharField(_('Status'), choices=[('C', 'Credit'), ('F', 'Failed')], default='F', max_length=3)
    fees = models.DecimalField(_('Fees by Instamojo'), max_digits=10, decimal_places=3, null=True)
    currency = models.CharField(_('Currency'), null=True, blank=True, max_length=50)

    class Meta:
        verbose_name = _('Instamojo Payment')
        verbose_name_plural = _('Instamojo Payment')
