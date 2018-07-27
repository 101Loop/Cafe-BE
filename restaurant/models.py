from django.db import models
from django.utils.text import gettext_lazy as _
from drfaddons.models import CreateUpdateModel


class Tag(models.Model):
    tag = models.CharField(_('Tag'), max_length=254)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


class Item(CreateUpdateModel):
    category = models.CharField(_('Category'), max_length=254, choices=[('V', 'Veg'), ('N', 'Non-Veg'), ('J', 'Jain')])
    name = models.CharField(_('Name'), max_length=254, unique=True)
    price = models.DecimalField(_('Item Price'), max_digits=10, decimal_places=3)
    image = models.URLField(_('Image URL'), max_length=254, null=True)
    tags = models.ManyToManyField(Tag)
    hsn = models.CharField(_('HSN (GST)'), null=True, max_length=20)
    desc = models.TextField(_('Description'), null=True)
    gst = models.DecimalField(_('GST Percentage'), max_digits=5, decimal_places=2, default=5.00)
    gst_inclusive = models.BooleanField(_('GST Inclusive?'), default=True)

    @property
    def subtotal(self):
        if self.gst_inclusive:
            return self.price/(1+(self.gst/100))
        else:
            return self.price

    @property
    def total(self):
        if self.gst_inclusive:
            return self.price
        else:
            return self.price*(1 + (self.gst/100))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')


class LunchPack(CreateUpdateModel):
    name = models.CharField(_('Name'), max_length=254, unique=True)
    price = models.DecimalField(_('Item Price'), max_digits=10, decimal_places=3)
    category = models.CharField(_('Category'), max_length=254, choices=[('V', 'Veg'), ('N', 'Non-Veg'), ('J', 'Jain')])
    items = models.ManyToManyField(Item)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Lunch Pack')
        verbose_name_plural = _('Lunch Packs')


class Store(CreateUpdateModel):
    from django.contrib.auth import get_user_model

    name = models.CharField(_('Store Name'), max_length=254, unique=True)
    mobile = models.CharField(_('Mobile Number'), max_length=15, null=True)
    landline = models.CharField(_('Landline Number'), max_length=20, null=True)
    address = models.TextField(_('Address'), null=True)
    gst_number = models.TextField(_('GST Number'), null=True)
    assigned_to = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='managed_by', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')


class HasItem(CreateUpdateModel):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    in_stock = models.BooleanField(_('In Stock'))


# TODO: Create a class for hasItem: item, store, in_stock Done
# TODO: Add ingredients for items (Future)
