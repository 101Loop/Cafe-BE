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
    """
    A custom Item model that keeps a record of all item details.
    """
    category = models.CharField(_('Category'), max_length=254, choices=[('V', 'Veg'), ('N', 'Non-Veg'), ('J', 'Jain')])
    name = models.CharField(_('Name'), max_length=254, unique=True)
    price = models.DecimalField(_('Item Price'), max_digits=10, decimal_places=3)
    image = models.URLField(_('Image URL'), max_length=254, null=True)
    tags = models.ManyToManyField(Tag)
    hsn = models.CharField(_('HSN (GST)'), null=True, max_length=20)
    desc = models.TextField(_('Description'), null=True)
    gst = models.DecimalField(_('GST Percentage'), max_digits=5, decimal_places=2, default=5.00)
    gst_inclusive = models.BooleanField(_('GST Inclusive?'), default=True)
    is_addon = models.BooleanField(_('Is Addon'), default=False)
    addons = models.ManyToManyField('Item')

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
    """
    A custom LunchPack model that includes all the details of a lunch pack.
    """
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
    """
    A custom Store model that includes all the details of a store.
    """
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
    """
    This custom HasItem will show if an item is in stock in a store or not.
    """
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    in_stock = models.BooleanField(_('In Stock'))


class Cook(CreateUpdateModel):
    """
    A custom Cook model that includes all the details about the cook.
    """
    name = models.CharField(_('Name'), max_length=254)
    profile_pic = models.URLField(_('Profile Picture'), max_length=254, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)


class Order(models.Model):
    from billing.models import BillingHeader

    items = models.ForeignKey(Item, on_delete=models.PROTECT)
    bill = models.ForeignKey(BillingHeader, on_delete=models.PROTECT)
    mode = models.CharField(_('mode'), max_length=20, choices=[('P ', 'Pick Up'), ('D', 'Deliver'), ('I', 'Instant')])
    address = models.TextField(_('Address'))
    payment = models.CharField(_('Payment'), max_length=254, choices=[('O', 'Online'), ('P', 'Paytm'), ('C', 'Cash')])
    status = models.CharField(_('Status'), max_length=254, choices=[('1', 'Completed'), ('2', 'Cancel'), ('3', 'in_process')])
    feedback = models.CharField(_('Feedback'), max_length=254, null=True, blank=True)
    wait_time = models.CharField(_('Wait Time'), max_length=254, null=True, blank=True)


# TODO: Add ingredients for items (Future)
