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


class RawMaterialStock(CreateUpdateModel):
    """
    Represents stock of raw material in a warehouse

    Author: Himanshu Shankar (https://himanshus.com)
    """
    from warehouse.models import Warehouse

    warehouse = models.ForeignKey(to=Warehouse, on_delete=models.PROTECT,
                                  verbose_name=_("Warehouse"))
    raw_material = models.ForeignKey(to=RawMaterialMaster,
                                     on_delete=models.PROTECT,
                                     verbose_name=_("Raw Material"))
    quantity = models.DecimalField(verbose_name=_("Quantity"),
                                   decimal_places=3, max_digits=10)

    @property
    def stock(self):
        return "{quant} {uom}".format(quant=str(self.quantity),
                                      uom=self.raw_material.uom.name)

    def __str__(self):
        return self.raw_material.name + " in " + self.warehouse.name

    class Meta:
        unique_together = ('warehouse', 'raw_material')
        verbose_name = _("Raw Material Stock in Warehouse")
        verbose_name_plural = _("Raw Materials Stock in Warehouse")


class StockCredit(CreateUpdateModel):
    """
    Represents all stock transactions in happening in the warehouse

    Author: Himanshu Shankar (https://himanshus.com)
    """
    stock = models.ForeignKey(to=RawMaterialStock, on_delete=models.PROTECT,
                              verbose_name=_("Stock"))
    quantity = models.DecimalField(verbose_name=_("Quantity"),
                                   decimal_places=3, max_digits=10)
    date = models.DateField(verbose_name=_("Date of Input"))

    mfg_date = models.DateField(verbose_name=_("Manufacturing Date"),
                                null=True, blank=True)
    exp_date = models.DateField(verbose_name=_("Expiry Date"), null=True,
                                blank=True)
    mfg_batch = models.CharField(verbose_name=_("Manufacturing Batch Number"),
                                 null=True, blank=True, max_length=254)
    other = models.TextField(verbose_name=_("Other details"), null=True,
                             blank=True)



    def __str__(self):
        return str(self.stock)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(StockCredit, self).save(force_insert=force_insert,
                                      force_update=force_update,
                                      using=using,
                                      update_fields=update_fields)

        # Update stock
        self.stock.quantity += self.quantity
        self.stock.save()

    class Meta:
        verbose_name = _("Raw Material Input")
        verbose_name_plural = _("Raw Material Inputs")
