from django.db import models
from django.utils.text import gettext_lazy as _

from drfaddons.models import CreateUpdateModel


class LeadStatus(CreateUpdateModel):
    """
    Represents all possible lead status in the system.

    Author: Himanshu Shankar (https://himanshus.com)
    """

    name = models.CharField(verbose_name=_("Status"), unique=True,
                            max_length=154)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Statuses")


class Lead(CreateUpdateModel):
    """
    Represents leads in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """
    from django.contrib.contenttypes.fields import GenericRelation

    from comment.models import Comment

    name = models.CharField(verbose_name=_("Name"), max_length=254)
    mobile = models.CharField(verbose_name=_("Mobile"), max_length=15,
                              unique=True)
    email = models.CharField(verbose_name=_("Email"), unique=True,
                             max_length=255)
    reference = models.TextField(verbose_name=_("Referer Details"),
                                 null=True, blank=True)
    status = models.ForeignKey(to=LeadStatus, on_delete=models.PROTECT,
                               verbose_name=_("Lead Status"))

    comment = GenericRelation(Comment)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Lead")
        verbose_name_plural = _("Leads")
