from django.db import models
from django.utils.text import gettext_lazy as _

from drfaddons.models import CreateUpdateModel


class Category(CreateUpdateModel):
    """
    Represents product category in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """

    name = models.CharField(verbose_name=_("Category Name"), max_length=254,
                            unique=True)
    sku_prefix = models.CharField(verbose_name=_("SKU Prefix"), max_length=4,
                                  unique=True)
    hsn = models.CharField(verbose_name=_("HSN Code"), max_length=6)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Product(CreateUpdateModel):
    """
    Represents product's in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from taxation.models import Tax

    name = models.CharField(verbose_name=_("Product Name"), max_length=254,
                            unique=True)
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT,
                                 verbose_name=_("Category"))
    price = models.DecimalField(verbose_name=_("Price"), max_digits=10,
                                decimal_places=3)
    interstate_tax = models.ManyToManyField(to=Tax, blank=True,
                                            verbose_name=_("Inter-State Tax"))
    instate_tax = models.ManyToManyField(to=Tax, blank=True,
                                         verbose_name=_("In-State Tax"))
    is_inclusive = models.BooleanField(verbose_name=_("Price inclusive of "
                                                      "Tax?"), default=True)
    sku = models.CharField(verbose_name=_("SKU Code"), max_length=28,
                           unique=True)
    o_hsn = models.CharField(verbose_name=_("Override HSN Code"),
                             max_length=6, null=True, blank=True)

    @property
    def hsn(self)->str:
        """
        Provides hsn code of the product
        Category's HSN if HSN has not been override

        Returns
        -------
        str

        Author: Himanshu Shankar (https://himanshus.com)
        """
        return self.o_hsn or self.category.hsn

    @property
    def sku_code(self)->str:
        """
        Provides full SKU code by adding sku prefix from category

        Returns
        -------
        str

        Author: Himanshu Shankar (https://himanshus.com)
        """
        return self.category.sku_prefix + self.sku

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
