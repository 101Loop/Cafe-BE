from django.db import models
from django.utils.text import gettext_lazy as _

from drfaddons.models import CreateUpdateModel


class Comment(CreateUpdateModel):
    """
    Represent comment in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """
    from django.contrib.contenttypes.fields import GenericForeignKey
    from django.contrib.contenttypes.models import ContentType

    comment = models.TextField(verbose_name=_("Comment"))

    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
