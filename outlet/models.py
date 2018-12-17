from django.db import models
from django.utils.text import gettext_lazy as _

from drfaddons.models import CreateUpdateModel


class Outlet(CreateUpdateModel):
    """
    Represents outlets

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from location.models import City

    name = models.CharField(verbose_name=_("Name"), max_length=254,
                            unique=True)
    city = models.ForeignKey(verbose_name=_("City"), to=City,
                             on_delete=models.PROTECT)
    unit = models.CharField(verbose_name=_("Unit No"), max_length=254,
                            null=True, blank=True)
    building = models.CharField(verbose_name=_("Building/Complex Name"),
                                max_length=254)
    area = models.CharField(verbose_name=_("Sector / Area"), max_length=254)
    pincode = models.CharField(verbose_name=_("Pincode"), max_length=6)

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
        return f"{self.manager.name} manages {self.outlet.name}"

    class Meta:
        verbose_name = _("Outlet Manager")
        verbose_name_plural = _("Outlet Managers")
