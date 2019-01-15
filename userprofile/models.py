from django.db import models
from django.utils.text import gettext_lazy as _

from drfaddons.models import CreateUpdateModel


class CategoryMaster(CreateUpdateModel):
    """
    Represent's user category in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """
    name = models.CharField(verbose_name=_("Category"), max_length=254,
                            unique=True)
    point = models.DecimalField(verbose_name=_("Point"), max_digits=10,
                                decimal_places=3)
    is_percentage = models.BooleanField(verbose_name=_("Is Percentage?"),
                                        default=True)
    is_default = models.BooleanField(verbose_name=_("Is Default?"),
                                     default=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        # Get all objects that has is_default set to True
        default_objects = CategoryMaster.objects.filter(is_default=True)

        # If the count of such object is 0, set is_default True for
        # current object
        if default_objects.count() == 0:
            self.is_default = True

        # If the count of such object is more than 1, set all default
        # flag for all such object to False and current object's flag
        # to True
        elif default_objects.count() > 1:
            default_objects.update(is_default=False)
            self.is_default = True

        # If only one of the object has default set to True
        else:
            # And current object also has is_default set to True and
            # it is not same as the one returned via query, set other
            # object default to False
            if self.is_default and self.pk and self in default_objects:
                default_objects.update(is_default=False)

        super(CategoryMaster, self).save(force_insert=force_insert,
                                         force_update=force_update,
                                         using=using,
                                         update_fields=update_fields)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class UserProfile(CreateUpdateModel):
    from django.contrib.auth import get_user_model

    created_by = models.OneToOneField(verbose_name=_("User"),
                                      to=get_user_model(),
                                      on_delete=models.PROTECT)
    category = models.ForeignKey(to=CategoryMaster, on_delete=models.PROTECT,
                                 verbose_name=_("User's Category"))
    company = models.CharField(verbose_name=_("Company Name"), null=True,
                               max_length=254, blank=True)
    designation = models.CharField(verbose_name=_("Designation"), null=True,
                                   blank=True, max_length=254)

    def __str__(self):
        return self.created_by.name

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")
