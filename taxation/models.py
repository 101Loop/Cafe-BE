from django.db import models
from django.utils.text import gettext_lazy as _

from drfaddons.models import CreateUpdateModel


class Tax(CreateUpdateModel):
    """
    Represents Taxes in a system

    Author: Himanshu Shankar (https://himanshus.com)
    """
    name = models.CharField(verbose_name=_("Tax Name"), max_length=254,
                            unique=True)
    display_name = models.CharField(verbose_name=_("Bill Display Name"),
                                    max_length=254)
    percentage = models.DecimalField(verbose_name=_("Percentage"),
                                     max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Tax")
        verbose_name_plural = _("Taxes")
