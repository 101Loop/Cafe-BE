from django.db import models
from django.utils.text import gettext_lazy as _

from drfaddons.models import CreateUpdateModel


class Outlet(CreateUpdateModel):
    """
    Represents outlets

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from location.models import City

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
    area = models.CharField(verbose_name=_("Sector / Area"), max_length=254)
    pincode = models.CharField(verbose_name=_("Pincode"), max_length=6)

    is_active = models.BooleanField(verbose_name=_("Is Active?"),
                                    default=True)
    phone = models.CharField(verbose_name=_("Outlet Phone"), max_length=15,
                             null=True, blank=True)

    @property
    def is_instate(self):
        return self.business.state.id == self.city.state.id

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

    @property
    def mrp(self):
        if self.product.is_inclusive:
            return self.product.price
        else:
            if self.outlet.is_instate:
                return self.product.price + self.product.total_instate_tax
            else:
                return self.product.price + self.product.total_interstate_tax

    def __str__(self):
        return "{product} in {outlet}".format(product=self.product.name,
                                              outlet=self.outlet.name)

    class Meta:
        verbose_name = _("Outlet Product")
        verbose_name_plural = _("Outlet Products")


class OutletCombo(CreateUpdateModel):
    """
    Represents combos in an outlet

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from product.models import ComboProduct

    combo = models.ForeignKey(to=ComboProduct, on_delete=models.PROTECT,
                              verbose_name=_("Combo Product"))
    outlet = models.ForeignKey(to=Outlet, on_delete=models.PROTECT,
                               verbose_name=_("Outlet"))

    @property
    def outlet_product(self):
        return self.outlet.outletproduct_set.filter(
            product__in=self.combo.combo_product.all())

    def clean_fields(self, exclude=None):
        """
        Checks if products in combo are already added in Outlet or not
        Parameters
        ----------
        exclude

        Raises
        -------
        ValidationError
        """

        from django.core.exceptions import ValidationError
        error = {}

        op = set(self.outlet.outletproduct_set.values_list('product',
                                                           flat=True))
        cp = set(self.combo.combo_product.all())

        if len(op-cp) is not 0:
            error['combo'] = _("Cannot add combo {combo} to {outlet}. Not "
                               "all combo's product present in "
                               "outlet.".format(combo=self.combo.name,
                                                outlet=self.outlet.name))
            raise ValidationError(error)
        return super(OutletCombo, self).clean_fields(exclude=exclude)
