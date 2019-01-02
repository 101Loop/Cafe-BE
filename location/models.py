from django.db import models
from django.utils.text import gettext_lazy as _


class Country(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=254,
                            unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")


class State(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=254,
                            unique=True)
    country = models.ForeignKey(verbose_name=_("Country"), to=Country,
                                on_delete=models.PROTECT)
    gst_code = models.CharField(verbose_name=_("GST Code"), max_length=2,
                                unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _("States")


class City(models.Model):
    name = models.CharField(verbose_name=_("City"), max_length=254)
    state = models.ForeignKey(verbose_name=_("State"), to=State,
                              on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")


class Area(models.Model):
    name = models.CharField(verbose_name=_("Area Name"), max_length=254)
    city = models.ForeignKey(verbose_name=_("City"), to=City,
                             on_delete=models.PROTECT)
    pincode = models.CharField(verbose_name=_("PIN Code"), max_length=6)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Area")
        verbose_name_plural = _("Areas")


class BuildingComplex(models.Model):
    name = models.CharField(verbose_name=_("Building / Society Complex"),
                            max_length=250)
    area = models.ForeignKey(verbose_name=_("Area"), to=Area,
                             on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'area')
        verbose_name = _("Building Complex")
        verbose_name_plural = _("Building Complexes")
