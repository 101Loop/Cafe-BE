from django.db import models
from django.utils.text import gettext_lazy as _
from drfaddons.models import CreateUpdateModel


class Tag(models.Model):
    tag = models.CharField(_('Tag'), max_length=254, unique=True)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


class Section(models.Model):
    name = models.CharField(_('Section'), max_length=254, unique=True)
    desc = models.TextField(_('Description'), null=True, blank=True)

    @property
    def items(self):
        return "https://llgm0gfd59.execute-api.ap-south-1.amazonaws.com/dev/api/restaurant/show/item?section=%d" % self.id

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Display Section')
        verbose_name_plural = _('Display Sections')


class Item(CreateUpdateModel):
    """
    A custom Item model that keeps a record of all item details.
    """
    category = models.CharField(_('Category'), max_length=254, choices=[('V', 'Veg'), ('N', 'Non-Veg'), ('J', 'Jain')])
    name = models.CharField(_('Name'), max_length=254, unique=True)
    price = models.DecimalField(_('Item Price'), max_digits=10, decimal_places=3)
    image = models.URLField(_('Image URL'), max_length=254, null=True, blank=True,
                            default='https://officecafe.in/assets/images/logo_whiteback.png')
    tags = models.ManyToManyField(Tag)
    sections = models.ManyToManyField(Section)
    hsn = models.CharField(_('HSN (GST)'), null=True, blank=True, max_length=20)
    desc = models.TextField(_('Description'), null=True, blank=True)
    gst = models.DecimalField(_('GST Percentage'), max_digits=5, decimal_places=2, default=5.00)
    gst_inclusive = models.BooleanField(_('GST Inclusive?'), default=True)
    is_addon = models.BooleanField(_('Is Addon'), default=False)
    addons = models.ManyToManyField('Item')

    @property
    def subtotal(self):
        if self.gst_inclusive:
            subt = self.price/(1+(self.gst/100))
            subt = round(subt, 2)
            return subt
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
    mobile = models.CharField(_('Mobile Number'), max_length=15, null=True, blank=True)
    landline = models.CharField(_('Landline Number'), max_length=20, null=True, blank=True)
    address = models.TextField(_('Address'), null=True, blank=True)
    gst_number = models.TextField(_('GST Number'), null=True, blank=True)
    assigned_to = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='managed_by', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')


class HasItem(CreateUpdateModel):
    """
    This custom HasItem model will show if an item is in stock in a store or not.
    """
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    in_stock = models.BooleanField(_('In Stock'), default=True)


class Cook(CreateUpdateModel):
    """
    A custom Cook model that includes all the details about the cook.
    """
    name = models.CharField(_('Name'), max_length=254)
    profile_pic = models.URLField(_('Profile Picture'), max_length=254, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Cook')
        verbose_name_plural = _('Cook')


class Order(CreateUpdateModel):
    """
    A custom Order model that includes all the details of an order.
    """
    from billing.models import BillingHeader

    items = models.ForeignKey(Item, on_delete=models.PROTECT)
    bill = models.ForeignKey(BillingHeader, on_delete=models.PROTECT)
    mode = models.CharField(_('mode'), max_length=20, choices=[('P ', 'Pick Up'), ('D', 'Deliver'), ('I', 'Instant')])
    address = models.TextField(_('Address'))
    payment = models.CharField(_('Payment'), max_length=254, choices=[('O', 'Online'), ('P', 'Paytm'), ('C', 'Cash')])
    status = models.CharField(_('Status'), max_length=254, choices=[('1', 'Completed'), ('2', 'Cancel'), ('3', 'in_process')])
    feedback = models.CharField(_('Feedback'), max_length=254, null=True, blank=True)
    wait_time = models.CharField(_('Wait Time'), max_length=254, null=True, blank=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
