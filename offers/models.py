from django.db import models
from django.utils.text import gettext_lazy as _


class Offer(models.Model):
    twitter = models.TextField(_('Twitter'))
    facebook = models.TextField(_('Facebook'))
    instagram = models.TextField(_('Instagram'))
    date = models.DateField(_('Date'))
    verify = models.BooleanField(_('Verify'))

    class Meta:
        verbose_name = _('Offer')
        verbose_name_plural = _('Offers')

