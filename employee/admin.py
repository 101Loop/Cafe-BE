from django.contrib import admin

from drfaddons.admin import CreateUpdateAdmin

from .models import Employee


class EmployeeDocumentInline(admin.TabularInline):
    from .models import EmployeeDocument

    model = EmployeeDocument
    extra = 0


class EmployeeAdmin(CreateUpdateAdmin):
    inlines = (EmployeeDocumentInline, )


admin.site.register(Employee, EmployeeAdmin)
