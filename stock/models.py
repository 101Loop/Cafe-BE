from django.db import models
from django.utils.text import gettext_lazy as _

from drfaddons.models import CreateUpdateModel


class UnitOfMeasurementMaster(CreateUpdateModel):
    """
    Represents unit of measurement in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """
    name = models.CharField(verbose_name=_("Unit of Measurement"),
                            max_length=254, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Unit of Measurement")
        verbose_name_plural = _("Unit of Measurements")


class RawMaterialMaster(CreateUpdateModel):
    """
    Represents raw materials in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """
    name = models.CharField(verbose_name=_("Raw Material"), max_length=254,
                            unique=True)
    uom = models.ForeignKey(verbose_name=_("Unit of Measurement"),
                            to=UnitOfMeasurementMaster,
                            on_delete=models.PROTECT)

    unit_quantity = models.DecimalField(
        verbose_name=_("Per Unit"), max_digits=10, decimal_places=3, null=True,
        blank=True, help_text=_("If raw material is packaged, what's per "
                                "unit quantity? Eg: Per Bottle: 1 Litre"))
    unit_uom = models.ForeignKey(
        verbose_name=_("Unit's UOM"), to=UnitOfMeasurementMaster, null=True,
        on_delete=models.PROTECT, related_name="rawmaterialunitmaster",
        blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Raw Material")
        verbose_name_plural = _("Raw Materials")


class RawMaterialPurchase(CreateUpdateModel):
    """
    Represents raw material purchases

    Author: Himanshu Shankar (https://himanshus.com)
    """
    from business.models import Business

    raw_material = models.ForeignKey(to=RawMaterialMaster,
                                     on_delete=models.PROTECT,
                                     verbose_name=_("Raw Material"))
    quantity = models.DecimalField(verbose_name=_("Number in Stock"))
    total_amount = models.DecimalField(verbose_name="_")
    owner = models.ForeignKey(to=Business, on_delete=models.PROTECT,
                              verbose_name=_("Business Owner"))

    def __str__(self):
        return self.raw_material.name + " - " + self.owner.name

    class Meta:
        verbose_name = _("Raw Material Purchase")
        verbose_name_plural = _("Raw Material Purchases")
