from django.db import models
from django.utils.text import gettext_lazy as _
from drfaddons.models import CreateUpdateModel


class Tag(models.Model):
    tag = models.CharField(_('Tag'), max_length=254)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


class Menu(models.Model):
    category = models.CharField(_('Category'), max_length=254, choices=[('V', 'Veg'), ('N', 'Non-Veg'), ('J', 'Jain')])
    name = models.CharField(_('Name'), max_length=254, blank=True, null=True)
    email = models.EmailField(_('EMail Address'))
    mobile = models.CharField(_('Mobile Number'), max_length=150)
    image = models.URLField(_('Image URL'), max_length=254)
    tags = models.ForeignKey(Tag, on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menu')


class Payment(CreateUpdateModel):
    price = models.FloatField(_('Price'), blank=False, null=False)
    date = models.DateField(_('Date'))

    class Meta:
        verbose_name = _('Payment')

