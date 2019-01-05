from django.db import models
from django.utils.text import gettext_lazy as _

from drfaddons.models import CreateUpdateModel


class Employee(CreateUpdateModel):
    """
    Represents employees in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """
    from django.contrib.auth import get_user_model

    name = models.CharField(verbose_name=_("Full Name"), max_length=254)
    user_id = models.OneToOneField(to=get_user_model(),
                                   on_delete=models.PROTECT,
                                   verbose_name=_("User Account"),
                                   related_name="is_employee",
                                   null=True, blank=True)
    designation = models.CharField(verbose_name=_("Designation"),
                                   max_length=10, null=True, blank=True)

    is_active = models.BooleanField(verbose_name=_("Is Active?"),
                                    default=False)
    joined_on = models.DateField(verbose_name=_("Join Date"), null=True,
                                 blank=True)
    left_on = models.DateField(verbose_name=_("Leave Date"), null=True,
                               blank=True)
    salary = models.DecimalField(verbose_name=_("Salary"), default=0,
                                 decimal_places=2, max_digits=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")


class EmployeeDocument(CreateUpdateModel):
    """
    Represents employee's document in the system

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from OfficeCafe.variables import EMPLOYEE_DOCUMENT_CHOICES

    employee = models.ForeignKey(to=Employee, on_delete=models.PROTECT,
                                 verbose_name=_("Employee"))
    doc = models.FileField(null=True, blank=True)
    doc_type = models.CharField(verbose_name=_("Document Type"), max_length=5,
                                choices=EMPLOYEE_DOCUMENT_CHOICES)
    doc_value = models.CharField(verbose_name=_("Document ID"),
                                 max_length=254, null=True, blank=True)
    is_verified = models.BooleanField(verbose_name=_("Is Verified?"),
                                      default=False)
    verified_by = models.ForeignKey(to=Employee, on_delete=models.PROTECT,
                                    related_name="verified_document",
                                    null=True, blank=True)
    verified_on = models.DateField(verbose_name=_("Verified On"), null=True,
                                   blank=True)

    def __str__(self):
        return self.employee.name + "'s " + self.get_doc_type_display()

    class Meta:
        verbose_name = _("Employee's Document")
        verbose_name_plural = _("Employee's Documents")
