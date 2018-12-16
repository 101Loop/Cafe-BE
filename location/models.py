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
