from django.db import models
from django.utils.text import gettext_lazy as _

from drfaddons.models import CreateUpdateModel

from stock.models import RawMaterialStock, StockCredit


class Outlet(CreateUpdateModel):
    """
    Represents outlets

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from location.models import City, Area

    from business.models import Business

    name = models.CharField(verbose_name=_("Name"), max_length=254,
                            unique=True)
    business = models.ForeignKey(verbose_name=_("Business Owner"),
                                 to=Business, on_delete=models.PROTECT)
    city = models.ForeignKey(verbose_name=_("City"), to=City,
                             on_delete=models.PROTECT)
    unit = models.CharField(verbose_name=_("Unit No"), max_length=254,
                            null=True, blank=True)
    building = models.CharField(verbose_name=_("Building/Complex Name"),
                                max_length=254)
    area = models.ForeignKey(to=Area, verbose_name=_("Area"),
                             on_delete=models.PROTECT)
    pincode = models.CharField(verbose_name=_("Pincode"), max_length=6)

    is_active = models.BooleanField(verbose_name=_("Is Active?"),
                                    default=True)
    phone = models.CharField(verbose_name=_("Outlet Phone"), max_length=15,
                             null=True, blank=True)

    serviceable_area = models.ManyToManyField(
        verbose_name=_("Serviceable Areas"), to=Area, blank=True,
        related_name="serviced_by_outlet")

    @property
    def full_address(self):
        address = ''

        if self.unit:
            address += self.unit

        if self.building:
            address = address + ', ' + self.building

        if self.area:
            address = address + ', ' + self.area.name

        if self.city:
            address = (address + ', ' + self.city.name + ', '
                       + self.city.state.name)

        if self.pincode:
            address = address + ' - ' + self.pincode

        return address

    @property
    def is_instate(self):
        return self.business.state.id == self.city.state.id

    def is_owner(self, user):
        return (user is self.created_by) or (self.business.is_owner(user))

    def has_permission(self, user):
        return (user is self.created_by) or (self.business.has_permission(
            user))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Outlet")
        verbose_name_plural = _("Outlets")


class OutletImage(CreateUpdateModel):
    """
    Represents Images of outlet

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from .utils import outlet_image_upload

    name = models.CharField(verbose_name=_("Image name"), max_length=154)
    outlet = models.ForeignKey(to=Outlet, verbose_name=_("Outlet"),
                               on_delete=models.PROTECT)
    image = models.ImageField(upload_to=outlet_image_upload)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Outlet Image")
        verbose_name_plural = _("Outlet Images")


class OutletManager(CreateUpdateModel):
    """
    Represents outlet managers

    Author: Himanshu Shankar
    """

    from django.contrib.auth import get_user_model

    manager = models.ForeignKey(to=get_user_model(), on_delete=models.PROTECT,
                                related_name=_("managesoutlet"),
                                verbose_name=_("Manager"))
    outlet = models.ForeignKey(to=Outlet, on_delete=models.PROTECT,
                               verbose_name=_("Outlet"))
    is_active = models.BooleanField(verbose_name=_("Is Active?"), default=True)

    def __str__(self):
        return "{manager} manages {outlet}".format(manager=self.manager.name,
                                                   outlet=self.outlet.name)

    class Meta:
        unique_together = ('manager', 'outlet')
        verbose_name = _("Outlet Manager")
        verbose_name_plural = _("Outlet Managers")


class OutletProduct(CreateUpdateModel):
    """
    Represents products in an outlet

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from product.models import Product

    product = models.ForeignKey(to=Product, on_delete=models.PROTECT,
                                verbose_name=_("Product"))
    outlet = models.ForeignKey(to=Outlet, on_delete=models.PROTECT,
                               verbose_name=_("Outlet"))
    stock = models.DecimalField(verbose_name=_("Stock"), max_digits=10,
                                decimal_places=2)
    o_price = models.DecimalField(verbose_name=_("Price"), max_digits=10,
                                  decimal_places=3, null=True, blank=True)

    @property
    def price(self):
        return self.o_price or self.product.price

    @property
    def mrp(self):
        if self.product.is_inclusive:
            return self.price
        else:
            if self.outlet.is_instate:
                return self.price + self.product.total_instate_tax
            else:
                return self.price + self.product.total_interstate_tax

    @property
    def taxations(self):
        taxes = []

        price = self.price

        if self.outlet.is_instate:
            for tax in self.product.instate_tax.all():
                tax_repr = dict()
                tax_repr['tax_name'] = tax.display_name
                tax_repr['tax_percentage'] = tax.percentage
                if self.product.is_inclusive:
                    price = self.price - self.product.total_instate_tax
                tax_repr['tax_value'] = (tax.percentage * price) / 100
                taxes.append(tax_repr)
            taxes.append({'tax_name': 'IGST', 'tax_percentage': 0,
                          'tax_value': 0})
        else:
            for tax in self.product.interstate_tax.all():
                tax_repr = dict()
                tax_repr['tax_name'] = tax.display_name
                tax_repr['tax_percentage'] = tax.percentage
                if self.product.is_inclusive:
                    price = self.price - self.product.total_interstate_tax
                tax_repr['tax_value'] = (tax.percentage * price) / 100
                taxes.append(tax_repr)
            taxes.append({'tax_name': 'CGST', 'tax_percentage': 0,
                          'tax_value': 0})
            taxes.append({'tax_name': 'SGST', 'tax_percentage': 0,
                          'tax_value': 0})

        return taxes

    def __str__(self):
        return "{product} in {outlet}".format(product=self.product.name,
                                              outlet=self.outlet.name)

    class Meta:
        unique_together = ('outlet', 'product')
        verbose_name = _("Outlet Product")
        verbose_name_plural = _("Outlet Products")


class OutletStock(RawMaterialStock):
    outlet = models.ForeignKey(to=Outlet, on_delete=models.PROTECT,
                               verbose_name=_("Outlet"))

    def __str__(self):
        return self.outlet.name + " - " + self.raw_material.name

    class Meta:
        unique_together = ('outlet', 'raw_material')
        verbose_name = _("Outlet Stock")
        verbose_name_plural = _("Outlet Stocks")


class OutletProcurement(StockCredit):
    stock = models.ForeignKey(to=OutletStock, on_delete=models.PROTECT,
                              verbose_name=_("Stock"))

    class Meta:
        verbose_name = _("Outlet Procurement")
        verbose_name_plural = _("Outlet Procurements")


class OutletStockRequest(CreateUpdateModel):
    """
    Represents request for Raw Material in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """
    batch_id = models.PositiveIntegerField(verbose_name=_("Batch Request ID"))

    stock = models.ForeignKey(to=OutletStock,
                              on_delete=models.PROTECT,
                              verbose_name=_("Outlet Stock"))
    quantity = models.DecimalField(verbose_name=_("Quantity"),
                                   decimal_places=3, max_digits=10)
    fulfilled_on = models.DateField(verbose_name=_("Fulfilled On?"),
                                    help_text=_("When was this request "
                                                "fulfilled?"),
                                    null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        from django.utils import timezone

        super(OutletStockRequest, self).save(force_insert=force_insert,
                                             force_update=force_update,
                                             using=using,
                                             update_fields=update_fields)
        if self.fulfilled_on:
            OutletProcurement.objects.create(
                created_by=self.created_by,
                stock=self.stock,
                quantity=self.quantity,
                date=timezone.now()
            )

    def __str__(self):
        return str(self.stock)

    class Meta:
        verbose_name = _("Outlet Stock Request")
        verbose_name_plural = _("Outlet Stock Requests")
